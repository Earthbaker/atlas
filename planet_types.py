class BodySetting(object):

    def __init__(self, diameter):
        self._diameter = diameter

    def get_biome_color(self, elevation, moisture):
        return self._biome_dict[self._biome_assignments.get((elevation, moisture), self._biome_other)]

    def get_terrain_noise(self):
        return (self._large_noise_weight, self._medium_noise_weight, self._small_noise_weight)

    def get_moisture_width(self):
        return self._moisture_noise_width

    def get_terrain_amplitude(self):
        return self._amplitude

    def get_terrain_width(self):
        return (self._large_noise_width, self._medium_noise_width, self._small_noise_width)

    def get_island_number_range(self):
        return (self._max_island_number, self._min_island_number)

    def get_island_size_range(self):
        return (self._max_island_size, self._min_island_size)

    def get_max_height(self):
        return self._max_height

    def get_min_height(self):
        return self._min_height

    def get_height_range(self):
        return self._height_range

    def get_moisture_levels(self):
        return self._total_moisture_levels

    def get_elevation_levels(self):
        return self._total_elevation_levels

    def get_diameter(self):
        return self._diameter

    def get_cloud_color(self):
        return self._cloud_color

    def get_cloud_height(self):
        return self._cloud_height

    def get_cloud_width(self):
        return self._cloud_noise_width

    def get_cloud_cutoff(self):
        return self._cloud_noise_cutoff


class PlanetSetting(BodySetting):

    def __init__(self, diameter):
        super().__init__(diameter)


class MoonSetting(BodySetting):

    def __init__(self, diameter, orbiting_body):
        super().__init__(diameter)
        self._orbiting_body = orbiting_body

    def get_orbiting_body(self):
        return self._orbiting_body
    


class TerrestrialOceans(PlanetSetting):

    def __init__(self, diameter):

        super().__init__(diameter)
        
        self._planet_type = 'TERRESTRIAL OCEANS'

        #Terrain_generation
        self._max_island_number = 14
        self._min_island_number = 7
        self._max_island_size = (2/3) * self._diameter
        self._min_island_size = (1/5) * self._diameter

        #Terrain_noise_generation
        self._large_noise_weight = 1
        self._medium_noise_weight = 0.9
        self._small_noise_weight = 0.5
        self._large_noise_width = (1/5) * self._diameter
        self._medium_noise_width = (1/10) * self._diameter
        self._small_noise_width = (1/20) * self._diameter
        self._max_height = 0.58*self._diameter
        self._min_height = 0.5*self._diameter
        self._height_range = self._max_height - self._min_height
        self._amplitude = self._height_range/(0.5*self._diameter*(self._large_noise_weight + self._medium_noise_weight + self._small_noise_weight))

        #Moisture_noise_generation
        self._moisture_noise_width = (1/5)*self._diameter

        #Biomes
        self._total_moisture_levels = 6
        self._total_elevation_levels = 4
        
        #Biome colors
        self._biome_dict = {}
        self._biome_dict['SNOW'] = (248, 248, 248, 255)
        self._biome_dict['TUNDRA'] = (221, 221, 187, 255)
        self._biome_dict['BARE'] = (187, 187, 187, 255)
        self._biome_dict['SCORCHED'] = (153, 153, 153, 255)
        self._biome_dict['TAIGA'] = (204, 212, 187, 255)
        self._biome_dict['SHRUBLAND'] = (196, 204, 187, 255)
        self._biome_dict['TEMPERATE DESERT'] = (228, 232, 202, 255)
        self._biome_dict['TEMPERATE RAIN FOREST'] = (164, 196, 168, 255)
        self._biome_dict['TEMPERATE DECIDUOUS FOREST'] = (180, 196, 169, 255)
        self._biome_dict['GRASSLAND'] = (196, 212, 170, 255)
        self._biome_dict['TROPICAL RAIN FOREST'] = (156, 187, 169, 255)
        self._biome_dict['TROPICAL SEASONAL FOREST'] = (169, 204, 164, 255)
        self._biome_dict['SUBTROPICAL DESERT'] = (233, 221, 199, 255)
        self._biome_dict['OCEAN'] = (63, 156, 255, 255)
        # Elevation level, moisture_level --> Biome
        self._biome_assignments = {}
        self._biome_assignments[(4, 6)] = 'SNOW'
        self._biome_assignments[(4, 5)] = 'SNOW'
        self._biome_assignments[(4, 4)] = 'SNOW'
        self._biome_assignments[(4, 3)] = 'TUNDRA'
        self._biome_assignments[(4, 2)] = 'BARE'
        self._biome_assignments[(4, 1)] = 'SCORCHED'
        self._biome_assignments[(3, 6)] = 'TAIGA'
        self._biome_assignments[(3, 5)] = 'TAIGA'
        self._biome_assignments[(3, 4)] = 'SHRUBLAND'
        self._biome_assignments[(3, 3)] = 'SHRUBLAND'
        self._biome_assignments[(3, 2)] = 'TEMPERATE DESERT'
        self._biome_assignments[(3, 1)] = 'TEMPERATE DESERT'
        self._biome_assignments[(2, 6)] = 'TEMPERATE RAIN FOREST'
        self._biome_assignments[(2, 5)] = 'TEMPERATE DECIDUOUS FOREST'
        self._biome_assignments[(2, 4)] = 'TEMPERATE DECIDUOUS FOREST'
        self._biome_assignments[(2, 3)] = 'GRASSLAND'
        self._biome_assignments[(2, 2)] = 'GRASSLAND'
        self._biome_assignments[(2, 1)] = 'TEMPERATE DESERT'
        self._biome_assignments[(1, 6)] = 'TROPICAL RAIN FOREST'
        self._biome_assignments[(1, 5)] = 'TROPICAL RAIN FOREST'
        self._biome_assignments[(1, 4)] = 'TROPICAL SEASONAL FOREST'
        self._biome_assignments[(1, 3)] = 'TROPICAL SEASONAL FOREST'
        self._biome_assignments[(1, 2)] = 'GRASSLAND'
        self._biome_assignments[(1, 1)] = 'SUBTROPICAL DESERT'
        self._biome_other = 'OCEAN'

        #Axis & Rotation Speed
        self._axis = 2 #Placeholder for when I figure this shit out eventually
        self._rotational_speed = 2 #Another placeholder

        #Clouds
        self._cloud_color = (255, 255, 255, 185)
        self._cloud_height = self._max_height * 0.95
        self._cloud_noise_width = (1/5) * self._diameter
        self._cloud_noise_cutoff = 0.5


class TerrestrialIronOxide(PlanetSetting):

    def __init__(self, diameter):

        super().__init__(diameter)
        
        self._planet_type = 'TERRESTRIAL OCEANS'

        #Terrain_generation
        self._max_island_number = 18
        self._min_island_number = 11
        self._max_island_size = (2/3) * self._diameter
        self._min_island_size = (1/5) * self._diameter

        #Terrain_noise_generation
        self._large_noise_weight = 1
        self._medium_noise_weight = 0.4
        self._small_noise_weight = 0.1
        self._large_noise_width = (1/5) * self._diameter
        self._medium_noise_width = (1/10) * self._diameter
        self._small_noise_width = (1/20) * self._diameter
        self._max_height = 0.56*self._diameter
        self._min_height = 0.5*self._diameter
        self._height_range = self._max_height - self._min_height
        self._amplitude = self._height_range/(0.5*self._diameter*(self._large_noise_weight + self._medium_noise_weight + self._small_noise_weight))

        #Moisture_noise_generation
        self._moisture_noise_width = (1/5)*self._diameter

        #Biomes
        self._total_moisture_levels = 4
        self._total_elevation_levels = 3
        
        #Biome colors
        self._biome_dict = {}
        self._biome_dict['SOOT'] = (130, 107, 70, 255)
        self._biome_dict['HIGH IRON'] = (138, 94, 69, 255)
        self._biome_dict['MEDIUM IRON'] = (197, 127, 91, 255)
        self._biome_dict['LOW IRON'] = (203, 145, 124, 255)
        self._biome_dict['ICE'] = (224, 255, 255, 255)
        self._biome_dict['SNOW'] = (255, 255, 255, 255)
        self._biome_dict['BASE TERRAIN'] = (168, 121, 103, 255)
        # Elevation level, moisture_level --> Biome
        self._biome_assignments = {}
        self._biome_assignments[(3, 4)] = 'ICE'
        self._biome_assignments[(3, 3)] = 'SNOW'
        self._biome_assignments[(3, 2)] = 'HIGH IRON'
        self._biome_assignments[(3, 1)] = 'MEDIUM IRON'
        self._biome_assignments[(2, 4)] = 'HIGH IRON'
        self._biome_assignments[(2, 3)] = 'MEDIUM IRON'
        self._biome_assignments[(2, 2)] = 'LOW IRON'
        self._biome_assignments[(2, 1)] = 'LOW IRON'
        self._biome_assignments[(1, 4)] = 'MEDIUM IRON'
        self._biome_assignments[(1, 3)] = 'MEDIUM IRON'
        self._biome_assignments[(1, 2)] = 'LOW IRON'
        self._biome_assignments[(1, 1)] = 'SOOT'
        self._biome_other = 'BASE TERRAIN'

        #Axis & Rotation Speed
        self._axis = 2 #Placeholder for when I figure this shit out eventually
        self._rotational_speed = 2 #Another placeholder

        self._cloud_color = None
        self._cloud_height = None
        self._cloud_noise_width = None
        self._cloud_noise_cutoff = None



class ClassicMoon(MoonSetting):

    def __init__(self, diameter, orbiting_body):

        super().__init__(diameter, orbiting_body)
        
        self._planet_type = 'CLASSIC MOON'

        #Terrain_generation
        self._max_island_number = 35
        self._min_island_number = 30
        self._max_island_size = (3/5) * self._diameter
        self._min_island_size = (1/10) * self._diameter

        #Terrain_noise_generation
        self._large_noise_weight = 1
        self._medium_noise_weight = 0.4
        self._small_noise_weight = 0.3
        self._large_noise_width = (1/5) * self._diameter
        self._medium_noise_width = (1/10) * self._diameter
        self._small_noise_width = (1/20) * self._diameter
        self._max_height = 0.51*self._diameter
        self._min_height = 0.5*self._diameter
        self._height_range = self._max_height - self._min_height
        self._amplitude = self._height_range/(0.5*self._diameter*(self._large_noise_weight + self._medium_noise_weight + self._small_noise_weight))

        #Moisture_noise_generation
        self._moisture_noise_width = (1/3)*self._diameter

        #Biomes
        self._total_moisture_levels = 2
        self._total_elevation_levels = 2
        
        #Biome colors
        self._biome_dict = {}
        self._biome_dict['GREY1'] = (200, 200, 200, 255)
        self._biome_dict['GREY2'] = (180, 180, 180, 255)
        self._biome_dict['GREY3'] = (187, 180, 160, 255)
        self._biome_dict['GREY4'] = (153, 153, 153, 255)
        self._biome_dict['GREY5'] = (204, 212, 187, 255)
        # Elevation level, moisture_level --> Biome
        self._biome_assignments = {}
        self._biome_assignments[(2, 2)] = 'GREY1'
        self._biome_assignments[(1, 2)] = 'GREY2'
        self._biome_assignments[(2, 1)] = 'GREY3'
        self._biome_assignments[(1, 1)] = 'GREY4'
        self._biome_other = 'GREY5'

        #Axis & Rotation Speed
        self._axis = 2 #Placeholder for when I figure this shit out eventually
        self._rotational_speed = 2 #Another placeholder

        self._cloud_color = None
        self._cloud_height = None
        self._cloud_noise_width = None
        self._cloud_noise_cutoff = None



