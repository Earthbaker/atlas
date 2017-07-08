from PIL import ImageDraw, Image, ImageFont
import numpy as np
import imageio
import math, random
import time, datetime
import planet_support as ps
import planet_types as pt

class Planet(object):

    def __init__(self, planet_type, seed, complexity):
        self._planet = planet_type
        self._diameter = self._planet.get_diameter()
        self.define_base_nodes()
        self.define_base_edges()
        self.define_base_faces()
        self.complexify(complexity)
        random.seed(seed)
        self.gen_terrain()
        self.assign_biomes()
        self._cloud_faces = []
        self.gen_clouds()
        

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

    def define_base_nodes(self):
        d = self._diameter
        a = d / math.sqrt(11 + 2*math.sqrt(5))
        phi = a * (1 + math.sqrt(5))/2
        self._nodes = []
        self._nodes.append(ps.change_distance([0, -a, -phi], self._diameter))
        self._nodes.append(ps.change_distance([0, -a, phi], self._diameter))
        self._nodes.append(ps.change_distance([0, a, -phi], self._diameter))
        self._nodes.append(ps.change_distance([0, a, phi], self._diameter))
        self._nodes.append(ps.change_distance([-a, -phi, 0], self._diameter))
        self._nodes.append(ps.change_distance([-a, phi, 0], self._diameter))
        self._nodes.append(ps.change_distance([a, -phi, 0], self._diameter))
        self._nodes.append(ps.change_distance([a, phi, 0], self._diameter))
        self._nodes.append(ps.change_distance([-phi, 0, -a], self._diameter))
        self._nodes.append(ps.change_distance([phi, 0, -a], self._diameter))
        self._nodes.append(ps.change_distance([-phi, 0, a], self._diameter))
        self._nodes.append(ps.change_distance([phi, 0, a], self._diameter))

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

    def complexify(self, complexity):
            
        for x in range(complexity):

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
                
            self._nodes = new_nodes
            self._edges = new_edges
            self._faces = new_faces
            

    def assign_biomes(self):
        
        moisture_noise_hash = hash(random.random())
        
        for face in self._faces:
            
            nodes = ps.get_nodes(self._edges[face[0]], self._edges[face[1]], self._edges[face[2]])
            
            node1, node2, node3 = self._nodes[nodes[0]], self._nodes[nodes[1]], self._nodes[nodes[2]]
            
            mid = ps.get_middle_point(node1, node2, node3)

            height = math.sqrt(mid[0]**2 + mid[1]**2 + mid[2]**2)

            tml = self._planet.get_moisture_levels()
            tel = self._planet.get_elevation_levels()
            mw = self._planet.get_moisture_width()

            min_height = self._planet.get_min_height()
            height_range = self._planet.get_height_range()
            
            moisture_level = ps.perlin(mid, mw, tml, moisture_noise_hash)
            
            if moisture_level > 0.55*tml:
                moisture_level = moisture_level*(2 - moisture_level/tml)
            elif moisture_level < 0.45*tml:
                moisture_level = tml - (tml-moisture_level)*(1 + moisture_level/tml)
                
            moisture_level = math.ceil(moisture_level)
            elevation_level = math.ceil(tel*(height-min_height)/height_range)
            
            biome_color = self._planet.get_biome_color(elevation_level, moisture_level)
            
            face.append(biome_color)
        

    def gen_terrain(self):

        terrain_large_noise_hash = hash(random.random())
        terrain_med_noise_hash = hash(random.random())
        terrain_small_noise_hash = hash(random.random())

        nodes_length = len(self._nodes)
        
        largenoisewidth, mednoisewidth, smallnoisewidth = self._planet.get_terrain_width()
        lnd, mnd, snd = self._planet.get_terrain_noise()

        amplitude = self._planet.get_terrain_amplitude()
        
        max_height = self._planet.get_max_height()
        min_height = self._planet.get_min_height()
        height_range = self._planet.get_height_range()

        max_island_number, min_island_number = self._planet.get_island_number_range()
        max_island_size, min_island_size = self._planet.get_island_size_range()
        
        island_total = random.randrange(min_island_number, max_island_number + 1)
        rmarray = []
        for i in range(island_total):
            island_size = random.random()*(max_island_size - min_island_size) + min_island_size
            rmarray.append([self._nodes[random.randrange(nodes_length)], island_size])
        
        new_nodes = []
        for node in self._nodes:

            min_dist_ratio = 0

            for rm in rmarray:
                island_size = rm[1]
                dist_from_mountain = math.sqrt((node[0]-rm[0][0])**2 + (node[1]-rm[0][1])**2 + (node[2]-rm[0][2])**2)
                dist_ratio = 1 - dist_from_mountain/island_size
                if dist_ratio > min_dist_ratio:
                    min_dist_ratio = dist_ratio

            

            large_noise = ps.perlin(node, largenoisewidth, amplitude, terrain_large_noise_hash)
            med_noise = ps.perlin(node, mednoisewidth, amplitude, terrain_med_noise_hash)
            small_noise = ps.perlin(node, smallnoisewidth, amplitude, terrain_small_noise_hash)

            noise = (lnd*large_noise + mnd*med_noise + snd*small_noise)
            actual_noise = noise - amplitude*(lnd + mnd + snd)*(1-min_dist_ratio)
            if actual_noise < 0:
                actual_noise = 0
            multiplier = 1 + actual_noise

            new_nodes.append(ps.change_distance(node, self._diameter, multiplier))
                
        self._nodes = new_nodes

    def gen_clouds(self):
        cloud_color = self._planet.get_cloud_color()
        self._cloud_faces = []
        if cloud_color == None:
            pass
        cloud_hash = hash(random.random())
        cloud_cutoff = self._planet.get_cloud_cutoff()
        cloud_noise_width = self._planet.get_cloud_width()
        cloud_height = self._planet.get_cloud_height()
        for face in self._faces:
            node1, node2, node3 = ps.get_nodes(self._edges[face[0]], self._edges[face[1]], self._edges[face[2]])
            n1, n2, n3 = self._nodes[node1], self._nodes[node2], self._nodes[node3]
            middle_node = ps.get_middle_point(n1, n2, n3)
            cloud_noise = ps.perlin(middle_node, cloud_noise_width, 1, cloud_hash)
            if cloud_noise > cloud_cutoff:
                new_cloud = [node1, node2, node3, cloud_color]
                self._cloud_faces.append(new_cloud)
            
        


class GifCanvas:

    def __init__(self, canvas_size, background_color):
        self._canvas_width, self._canvas_height = canvas_size
        self._canvas_size = canvas_size
        self._background_color = background_color
        self._gif_images = []
        self._bodies = {}
        self.gen_base_canvas(100, 1, 1)

    def set_lighting(self, light_vector):
        self._light_vector = light_vector

    def gen_base_canvas(self, star_number, star_min_size, star_max_size):
        self._base_canvas = Image.new("RGBA", self._canvas_size, color=self._background_color)
        base_canvas_draw = ImageDraw.Draw(self._base_canvas)

        greenwhite_star = (204, 255, 204, 255)
        blue_star = (153, 204, 255, 255)
        white_star = (255, 255, 255, 255)
        yellowwhite_star = (255, 255, 153, 255)
        yellow_star = (255, 232, 131, 255)
        orange_star = (254, 204, 177, 255)
        orangered_star = (255, 153, 102, 255)
        red_star = (255, 204, 203, 255)
        colors = []
        colors.append(greenwhite_star)
        colors.append(blue_star)
        colors.append(white_star)
        colors.append(yellowwhite_star)
        colors.append(yellow_star)
        colors.append(orange_star)
        colors.append(orangered_star)
        colors.append(red_star)

        for i in range(int(self._canvas_width*self._canvas_height/1000)):
            star_color = colors[random.randrange(8)]
            xcentre = random.randrange(self._canvas_width)
            ycentre = random.randrange(self._canvas_height)
            star_size = random.randrange(star_min_size, star_max_size+1)
            coordinates = [xcentre-math.ceil(star_size/2), ycentre-math.ceil(star_size/2), xcentre+math.ceil(star_size/2), ycentre+math.ceil(star_size/2)]
            base_canvas_draw.ellipse(coordinates, fill=star_color)
        
        

    def draw_image(self):
        self._canvas = self._base_canvas.copy()
        canvas_draw = ImageDraw.Draw(self._canvas)

        draw_faces = []
        for body, position in self._bodies.items():
            
            for face in body._faces:
                n1num, n2num, n3num = ps.get_nodes(body._edges[face[0]], body._edges[face[1]], body._edges[face[2]])
                n1 = body._nodes[n1num]
                n2 = body._nodes[n2num]
                n3 = body._nodes[n3num]
                
                mid = ps.get_middle_point(n1, n2, n3)
                zcoord = mid[2]
                
                color = ps.lighting(n1, n2, n3, face[3], self._light_vector)
                
                if self._bodies.get(position[0], None) != None:
                    draw_faces.append((zcoord+position[1][2], n1, n2, n3, color, position[1][:2]))
                else:
                    draw_faces.append((zcoord, n1, n2, n3, color, position))

            draw_faces = sorted(draw_faces)
            
            for face in draw_faces:
                xc, yc = face[5]
                fillcolor = face[4]
                canvas_draw.polygon([(face[1][0]+xc, face[1][1]+yc),(face[2][0]+xc, face[2][1]+yc),(face[3][0]+xc, face[3][1]+yc)], fill=fillcolor)

            draw_faces = []

            for face in body._cloud_faces:
                n1, n2, n3, color = body._nodes[face[0]], body._nodes[face[1]], body._nodes[face[2]], face[3]
                cloud_height = body._planet.get_cloud_height()
                newn1 = ps.change_distance(n1, 2*cloud_height)
                newn2 = ps.change_distance(n2, 2*cloud_height)
                newn3 = ps.change_distance(n3, 2*cloud_height)
                mid = ps.get_middle_point(newn1, newn2, newn3)
                zcoord = mid[2]
                color = ps.lighting(n1, n2, n3, color, self._light_vector)
                
                if self._bodies.get(position[0], None) != None:
                    draw_faces.append((zcoord+position[1][2], newn1, newn2, newn3, color, position[1][:2]))
                else:
                    draw_faces.append((zcoord, newn1, newn2, newn3, color, position))

            draw_faces = sorted(draw_faces)

            temp_image = Image.new("RGBA", self._canvas_size, color=0)
            temp_draw = ImageDraw.Draw(temp_image)
            for face in draw_faces:
                if face[0] > 0:
                    xc, yc = face[5]
                    fillcolor = face[4]
                    temp_draw.polygon([(face[1][0]+xc, face[1][1]+yc),(face[2][0]+xc, face[2][1]+yc),(face[3][0]+xc, face[3][1]+yc)], fill=fillcolor)
            self._canvas = Image.alpha_composite(self._canvas, temp_image)

        return self._canvas

    def add_body(self, body, position='centre'):
        if position == 'centre':
            self._bodies[body] = (self._canvas_width/2, self._canvas_height/2)
        elif self._bodies.get(position[0], None) != None:
            self._bodies[body] = [position[0], [self._bodies[position[0]][0]-position[1], self._bodies[position[0]][1], 0]]
        else:
            self._bodies[body] = position

    def remove_body(self, body):
        del self._bodies[body]
        
    def make_gif(self, fps=60, filepath='movie.gif'):
        self._gif_images = []
        for i in range(385):
            for body, position in self._bodies.items():
                body.rotate('x', 0.25)
                body.rotate('y', 0.75)
                body.rotate('z', 0.5)
                if self._bodies.get(position[0], None) != None:
                    position_node = position[1]
                    new_position = ps.rotate_node(position_node, 'y', 360/385, list(self._bodies[position[0]]) + [0])
                    position[1] = new_position
                image = self.draw_image()
                image = np.asarray(image)
                self._gif_images.append(image)
            print('Image', i+1, 'completed.')
                
        self.save_gif(fps, filepath)


    def save_gif(self, fps=60, filepath='movie.mp4'):
        if self._gif_images != []:
            imageio.mimsave(filepath, self._gif_images, fps=fps)
            print('Gif saved!')

    


def main():

    background_color = (0, 0, 0, 255)
    canvas_size = (750, 750)

    planet_type = pt.TerrestrialOceans(450)

    seed = str(input('Please enter a seed: '))
    complexity = int(input('Please enter a complexity: '))
    planet = Planet(planet_type, seed, complexity)
    
    gifcanvas = GifCanvas(canvas_size, background_color)
    gifcanvas.add_body(planet, 'centre')
    light_vector = [0, 0, 1]
    gifcanvas.set_lighting(light_vector)
    gifcanvas.make_gif()
    
if __name__ == "__main__":
    main()
