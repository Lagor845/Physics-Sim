from math3d import *
from pygame.time import Clock

class Physics_object:
    def __init__(self,pos = Vector3d,velocity = Vector3d,mass = float) -> None:
        self.pos = pos
        self.velocity = velocity
        self.mass = mass
    
    def add_force(self,force = Vector3d):
        acceleration = force.divide_ret(self.mass)
        self.velocity.add(acceleration)
    
    def _detect_collisions(self):
        self.pos
    
    def update(self):
        if not self._detect_collisions:
            self.pos += self.velocity

class Circle(Physics_object):
    def __init__(self,velocity,mass) -> None:
        super().__init__(velocity,mass)

class Physics_engine:
    def __init__(self) -> None:
        pass
    
    def calculate_wind_force(self,object_surface_area):
        wind_pressure = (self.sim_environment["wind_speed"] ** 2) * self.sim_environment["air_density"]
        return normalize_vector(convert_angles_to_vector3(self.sim_environment["wind_direction"].x,self.sim_environment["wind_direction"].y,self.sim_environment["wind_direction"].z)).multiply_ret(wind_pressure).multiply_ret(object_surface_area)
    
    def calculate_gravitational_force(self,object_mass):
        return Vector3d(self.sim_environment["gravitational_acceleration"].x,self.sim_environment["gravitational_acceleration"].y,self.sim_environment["gravitational_acceleration"].z).multiply_ret(object_mass)
    
    def Start(self,objects_list,sim_state,sim_enviroment):
        self.objects = objects_list
        self.sim_state = sim_state
        self.sim_environment = sim_enviroment
        self.clock = Clock()
        while True:
            if self.sim_state["current location"] == "Main_Sim":
                for physics_object in self.objects:
                    physics_object.update()
                self.sim_state["simulation_rate"] = self.clock.get_fps()
                self.clock.tick(0)