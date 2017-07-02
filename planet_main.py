from PIL import ImageDraw, Image, ImageFont
import numpy as np
import imageio
import math, random
import time, datetime
import colorsys as cs
import planet_support as ps

t = time.time()

class Planet:

    def __init__(self, diameter):
        self._diameter = diameter
        self.define_base_nodes()
        self.define_base_edges()
        self.define_base_faces()

    def define_base_nodes(self):
        raise NotImplementedError()

    def define_base_edges(self):
        raise NotImplementedError()

    def define_base_faces(self):
        raise NotImplementedError()

    def rotate(self, dimension, degrees):
        cosTheta = math.cos(math.radians(degrees))
        sinTheta = math.sin(math.radians(degrees))
        if dimension in ['x', 'X']:
            for node in self._nodes:
                y = node[1]
                z = node[2]
                node[1] = cosTheta * y - sinTheta * z
                node[2] = sinTheta * y + cosTheta * z
        elif dimension in ['y', 'Y']:
            for node in self._nodes:
                x = node[0]
                z = node[2]
                node[0] = cosTheta * x - sinTheta * z
                node[2] = sinTheta * x + cosTheta * z
        elif dimension in ['z', 'Z']:
            for node in self._nodes:
                x = node[0]
                y = node[1]
                node[0] = cosTheta * x - sinTheta * y
                node[1] = sinTheta * x + cosTheta * y
    

    def draw_shape(self, canvasSize):
        xcentre, ycentre = canvasSize
        xc = xcentre/2
        yc = ycentre/2
        image = Image.new("RGBA", canvasSize, color=(0, 0, 0, 255))
        draw = ImageDraw.Draw(image)
        nodesize = 1
        
        for edge in self._edges:
            n1num, n2num = edge
            n1 = self._nodes[n1num]
            n2 = self._nodes[n2num]
            mid = ps.get_middle_point(n1, n2)
            if mid[2] > 0:
                height = math.sqrt(mid[0]**2 + mid[1]**2 + mid[2]**2)
                if height < self._diameter/2:
                    draw.line((n1[0] + xc, n1[1] + yc, n2[0] + xc, n2[1] + yc), width=nodesize, fill=(0, 0, 200, 255))
                else:
                    draw.line((n1[0] + xc, n1[1] + yc, n2[0] + xc, n2[1] + yc), width=nodesize, fill=(0, 200, 0, 255))

        draw_faces = []

        for face in self._faces:
            n1num, n2num, n3num = ps.get_nodes(self._edges[face[0]], self._edges[face[1]], self._edges[face[2]])
            n1 = self._nodes[n1num]
            n2 = self._nodes[n2num]
            n3 = self._nodes[n3num]
            mid = ps.get_middle_point(n1, n2, n3)
            zcoord = mid[2]
            biome = face[3]
            draw_faces.append((zcoord, n1, n2, n3, biome))
            
        draw_faces = sorted(draw_faces)

        for face in draw_faces:

            biome = face[4]
            fillcolor = self._biomes[biome]
            draw.polygon([(face[1][0]+xc, face[1][1]+yc),(face[2][0]+xc, face[2][1]+yc),(face[3][0]+xc, face[3][1]+yc)], fill=fillcolor)
            edge_color = (255, 255, 255, 255)

        return image

    def gen_gif(self, canvasSize, angles, filename = 'movie.gif'):
        images = []
        for i in range(385):
            self.rotate('x', 0.25)
            self.rotate('y', 0.75)
            self.rotate('z', 0.5)
            image = self.draw_shape(canvasSize)
            if i % 50 == 49:
                print('Finished for image no#', i+1)
            else:
                print('Finished for image no#', i+1)
            image = np.asarray(image)
            images.append(image)
        return images

class Earthlike(Planet):

    def __init__(self, diameter, seed):
        super().__init__(diameter)
        random.seed(seed)
        self._noise_hash_large = hash(random.random())
        self._noise_hash_med = hash(random.random())
        self._noise_hash_small = hash(random.random())
        self._moisture_hash = hash(random.random())

        self._biomes = {}
        self._biomes['SNOW'] = (248, 248, 248)
        self._biomes['TUNDRA'] = (221, 221, 187, 255)
        self._biomes['BARE'] = (187, 187, 187, 255)
        self._biomes['SCORCHED'] = (153, 153, 153, 255)
        self._biomes['TAIGA'] = (204, 212, 187, 255)
        self._biomes['SHRUBLAND'] = (196, 204, 187, 255)
        self._biomes['TEMPERATE DESERT'] = (228, 232, 202, 255)
        self._biomes['TEMPERATE RAIN FOREST'] = (164, 196, 168, 255)
        self._biomes['TEMPERATE DECIDUOUS FOREST'] = (180, 196, 169, 255)
        self._biomes['GRASSLAND'] = (196, 212, 170, 255)
        self._biomes['TROPICAL RAIN FOREST'] = (156, 187, 169, 255)
        self._biomes['TROPICAL SEASONAL FOREST'] = (169, 204, 164, 255)
        self._biomes['SUBTROPICAL DESERT'] = (233, 221, 199, 255)
        self._biomes['OCEAN'] = (63, 156, 255, 255)
        

    def define_base_nodes(self):
        d = self._diameter
        a = d / math.sqrt(11 + 2*math.sqrt(5))
        phi = a * (1 + math.sqrt(5))/2
        self._nodes = []
        self._nodes.append([0, -a, -phi])
        self._nodes.append([0, -a, phi])
        self._nodes.append([0, a, -phi])
        self._nodes.append([0, a, phi])
        self._nodes.append([-a, -phi, 0])
        self._nodes.append([-a, phi, 0])
        self._nodes.append([a, -phi, 0])
        self._nodes.append([a, phi, 0])
        self._nodes.append([-phi, 0, -a])
        self._nodes.append([phi, 0, -a])
        self._nodes.append([-phi, 0, a])
        self._nodes.append([phi, 0, a])

    def define_base_edges(self):
        self._edges = []
        self._edges.append({0, 2}) #0
        self._edges.append({1, 3}) #1
        self._edges.append({4, 6}) #2
        self._edges.append({5, 7}) #3
        self._edges.append({8, 10}) #4
        self._edges.append({9, 11}) #5
        self._edges.append({0, 4}) #6
        self._edges.append({0, 6}) #7
        self._edges.append({1, 4}) #8
        self._edges.append({1, 6}) #9
        self._edges.append({2, 5}) #10
        self._edges.append({2, 7}) #11
        self._edges.append({3, 5}) #12
        self._edges.append({3, 7}) #13
        self._edges.append({0, 8}) #14
        self._edges.append({0, 9}) #15
        self._edges.append({1, 10}) #16
        self._edges.append({1, 11}) #17
        self._edges.append({2, 8}) #18
        self._edges.append({2, 9}) #19
        self._edges.append({3, 10}) #20
        self._edges.append({3, 11}) #21
        self._edges.append({6, 9}) #22
        self._edges.append({6, 11}) #23
        self._edges.append({7, 9}) #24
        self._edges.append({7, 11}) #25
        self._edges.append({4, 8}) #26
        self._edges.append({4, 10}) #27
        self._edges.append({5, 8}) #28
        self._edges.append({5, 10}) #29

    def define_base_faces(self):
        self._faces = []
        for i in range(len(self._edges)):
            for j in range(i+1, len(self._edges)):
                for k in range(j+1, len(self._edges)):
                    edge1 = self._edges[i]
                    edge2 = self._edges[j]
                    edge3 = self._edges[k]
                    if ps.check_edges(edge1, edge2, edge3):
                        self._faces.append([i, j, k])

    def complexify(self, comp, variance=True):
        
        new_nodes = []
        for node in self._nodes:
            new_nodes.append(ps.change_distance(node, self._diameter))
        self._nodes = new_nodes
        
        for x in range(comp):

            new_faces = []
            new_edges = []
            new_nodes = self._nodes

            nodelength = len(self._nodes)
            edgelength = len(self._edges)
            facelength = len(self._faces)

            for i in range(edgelength):
                node1num, node2num = self._edges[i]
                node1, node2 = self._nodes[node1num], self._nodes[node2num]
                midnode = ps.get_middle_point(node1, node2)

                new_nodes.append(ps.change_distance(midnode, self._diameter))
                    
                new_edges.extend([{node1num, nodelength + i}, {node2num, nodelength + i}])
            
            
            for i in range(facelength):
                
                face = self._faces[i]
                edgenum = [face[0], face[1], face[2]]
                edge1, edge2, edge3 = self._edges[edgenum[0]], self._edges[edgenum[1]], self._edges[edgenum[2]]
                node1num, node2num, node3num = ps.get_nodes(edge1, edge2, edge3)
                node1, node2, node3 = self._nodes[node1num], self._nodes[node2num], self._nodes[node3num]
                
                node12 = new_nodes[nodelength + edgenum[0]]
                node13 = new_nodes[nodelength + edgenum[1]]
                node23 = new_nodes[nodelength + edgenum[2]]

                new_edges.append({nodelength + edgenum[0], nodelength + edgenum[1]})
                new_edges.append({nodelength + edgenum[0], nodelength + edgenum[2]})
                new_edges.append({nodelength + edgenum[1], nodelength + edgenum[2]})

                edgecheck = [new_edges[edgenum[0]*2], new_edges[edgenum[0]*2+1]]
                edgecheck.extend([new_edges[edgenum[1]*2], new_edges[edgenum[1]*2+1]])
                edgecheck.extend([new_edges[edgenum[2]*2], new_edges[edgenum[2]*2+1]])
                edgecheck.append(new_edges[2*edgelength+i*3])
                edgecheck.append(new_edges[2*edgelength+i*3+1])
                edgecheck.append(new_edges[2*edgelength+i*3+2])
                
                for a in range(len(edgecheck)):
                    for b in range(a+1, len(edgecheck)):
                        for c in range(b+1, len(edgecheck)):
                            edge1 = edgecheck[a]
                            edge2 = edgecheck[b]
                            edge3 = edgecheck[c]
                            if ps.check_edges(edge1, edge2, edge3):
                                if a < 6:
                                    f = edgenum[(a//2)]*2+(a%2)
                                else:
                                    f = 2*edgelength + i*3 + (a - 6)
                                if b < 6:
                                    g = edgenum[(b//2)]*2+(b%2)
                                else:
                                    g = 2*edgelength + i*3 + (b - 6)
                                if c < 6:
                                    h = edgenum[(c//2)]*2+(c%2)
                                else:
                                    h = 2*edgelength + i*3 + (c - 6)
                                
                                new_faces.append([f, g, h])

            print('Complexity Level', x+1, 'completed.')
                
            self._nodes = new_nodes
            self._edges = new_edges
            self._faces = new_faces


        if variance:
            self.gen_terrain(comp)

        self.assign_colors(self._moisture_hash)

    def assign_colors(self, random_hash):
        for face in self._faces:
            nodes = ps.get_nodes(self._edges[face[0]], self._edges[face[1]], self._edges[face[2]])
            node1, node2, node3 = self._nodes[nodes[0]], self._nodes[nodes[1]], self._nodes[nodes[2]]
            mid = ps.get_middle_point(node1, node2, node3)
            node1height = math.sqrt(node1[0]**2 + node1[1]**2 + node1[2]**2)
            node2height = math.sqrt(node2[0]**2 + node2[1]**2 + node2[2]**2)
            node3height = math.sqrt(node3[0]**2 + node3[1]**2 + node3[2]**2)
            height = math.sqrt(mid[0]**2 + mid[1]**2 + mid[2]**2)
            moisture_level = ps.perlin(mid, self._diameter/5, 6, random_hash)
            if moisture_level > 3.25:
                moisture_level = moisture_level*(2 - moisture_level/6)
            elif moisture_level < 2.75:
                moisture_level = 6 - (6-moisture_level)*(1 + moisture_level/6)
            moisture_level = math.ceil(moisture_level)
            elevation_level = math.ceil(4*(height-self._min_height)/self._height_range)
            
            if (elevation_level, moisture_level) in [(4, 6), (4, 5), (4, 4)]:
                biome = 'SNOW'
            elif (elevation_level, moisture_level) in [(4, 3)]:
                biome = 'TUNDRA'
            elif (elevation_level, moisture_level) in [(4, 2)]:
                biome = 'BARE'
            elif (elevation_level, moisture_level) in [(4, 1)]:
                biome = 'SCORCHED'
            elif (elevation_level, moisture_level) in [(3, 6), (3, 5)]:
                biome = 'TAIGA'
            elif (elevation_level, moisture_level) in [(3, 4), (3, 3)]:
                biome = 'SHRUBLAND'
            elif (elevation_level, moisture_level) in [(3, 2), (3, 1), (2, 1)]:
                biome = 'TEMPERATE DESERT'
            elif (elevation_level, moisture_level) in [(2, 6)]:
                biome = 'TEMPERATE RAIN FOREST'
            elif (elevation_level, moisture_level) in [(2, 5), (2, 4)]:
                biome = 'TEMPERATE DECIDUOUS FOREST'
            elif (elevation_level, moisture_level) in [(2, 3), (2, 2), (1, 2)]:
                biome = 'GRASSLAND'
            elif (elevation_level, moisture_level) in [(1, 6), (1, 5)]:
                biome = 'TROPICAL RAIN FOREST'
            elif (elevation_level, moisture_level) in [(1, 4), (1, 3)]:
                biome = 'TROPICAL SEASONAL FOREST'
            elif (elevation_level, moisture_level) in [(1, 1)]:
                biome = 'SUBTROPICAL DESERT'
            else:
                biome = 'OCEAN'
            

            face.append(biome)
        

    def gen_terrain(self, comp):
        nodes_length = len(self._nodes)

        initial_angle = math.atan(2/(1 + math.sqrt(5)))
        angle = initial_angle / (2**comp)
        edge_length = self._diameter*math.sin(angle)
        periodlarge = self._diameter/5
        periodmed = self._diameter/10
        periodsmall = self._diameter/20
        

        large_noise_dist = 1
        lnd = large_noise_dist
        med_noise_dist = 0.9
        mnd = med_noise_dist
        small_noise_dist = 0.5
        snd = small_noise_dist

        amplitude = 0.18
        
        self._max_height = (1+amplitude*(lnd + mnd + snd))*0.5*self._diameter
        self._min_height = 0.5*self._diameter
        
        self._height_range = amplitude*self._diameter



        max_island_number = 14
        min_island_number = 7

        max_island_size = 2*self._diameter/3
        min_island_size = self._diameter/10
        
        island_number = random.randrange(min_island_number, max_island_number + 1)
        
        rmarray = []
        for i in range(island_number):
            island_size = random.random()*(max_island_size - min_island_size) + min_island_size
            rmarray.append([self._nodes[random.randrange(nodes_length)], island_size])
        
        new_nodes = []

        for node in self._nodes:

            min_dist_ratio = 1
            current_max_island_size = min_island_size
            island_size_multiplier = 1

            total_islands = 0

            for rm in rmarray:
                island_size = rm[1]
                dist_from_mountain = math.sqrt((node[0]-rm[0][0])**2 + (node[1]-rm[0][1])**2 + (node[2]-rm[0][2])**2)
                dist_ratio = dist_from_mountain/island_size
                if dist_ratio > 1:
                    dist_ratio = 1
                if dist_ratio < min_dist_ratio:
                    min_dist_ratio = dist_ratio
                if dist_ratio < 1:
                    total_islands += 1
                if island_size > current_max_island_size and dist_ratio < 1:
                    if total_islands == 1:
                        island_size_multiplier = island_size/max_island_size
                    else:
                        current_max_island_size = island_size
                        island_size_multiplier = current_max_island_size/max_island_size
                

            large_noise = ps.perlin(node, periodlarge, amplitude, self._noise_hash_large)
            med_noise = ps.perlin(node, periodmed, amplitude, self._noise_hash_med)
            small_noise = ps.perlin(node, periodsmall, amplitude, self._noise_hash_small)

            noise = (lnd*large_noise + mnd*med_noise + snd*small_noise)
            actual_noise = noise - amplitude*(lnd + mnd + snd)*(min_dist_ratio)
            if actual_noise < 0:
                actual_noise = 0
            multiplier = 1 + actual_noise*island_size_multiplier

            new_nodes.append(ps.change_distance(node, self._diameter, multiplier))
                
            
        self._nodes = new_nodes
        

class Gif_Canvas:

    def __init__():
        pass



def main():

    seed = 'planet sim 2017'
    new_t = time.time() - t
    print('Process started at ', new_t, 'seconds.')
    shape = Earthlike(375, seed)
    new_t = time.time() - t
    print('Shape finished after ', new_t, 'seconds.')
    shape.complexify(3)
    new_t = time.time() - t
    print('Complexity finished after ', new_t, 'seconds.')
    images = shape.gen_gif((600, 600), ['x'])
    new_t = time.time() - t
    print('Movie.gif created after ', new_t, 'seconds.')
    imageio.mimsave('movie.gif', images, fps=60)
    new_t = time.time() - t
    print('Gif saved after ', new_t, 'seconds.')

if __name__ == "__main__":
    main()
