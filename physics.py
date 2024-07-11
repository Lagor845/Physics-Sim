from math3d import *
from pygame.time import Clock
from pygame import draw
from time import time
from math3d import Vector3d

class Physics_object:
    def __init__(self,sim_status,pos = Vector3d(),velocity = Vector3d(),mass = 1,elasticity = 1) -> None:
        self.sim_status = sim_status
        self.pos = pos
        self.wall_collision_point = correct_to_coordinate_system(self.pos,self.sim_status["sim screen resolution"])
        self.velocity = velocity
        self.mass = mass
        self.elasticity = elasticity
        self.current_force = Vector3d()
    
    def calculate_wind_force(self,object_surface_area,wind_speed,air_density):
        wind_pressure = (wind_speed ** 2) * air_density
        return normalize_vector(convert_angles_to_vector3(self.sim_environment["wind_direction"].x,self.sim_environment["wind_direction"].y,self.sim_environment["wind_direction"].z)).multiply_ret(wind_pressure).multiply_ret(object_surface_area)
    
    def gravity(self,gravitational_acceleration = Vector3d()):
        self.current_force.add(gravitational_acceleration.multiply_ret(self.mass))
    
    def add_force(self,force = Vector3d()):
        self.current_force.add(force)
        acceleration = self.current_force.divide_ret(self.mass)
        self.velocity.add(acceleration.multiply_ret(self.sim_status["delta_time"]))
        self.current_force = Vector3d()
    
    def _detect_collisions(self):
        #collision with wall only currently
        colliding = False
        if self.pos.x + self.velocity.x > self.wall_collision_point.x or self.pos.x + self.velocity.x < -self.wall_collision_point.x:
            self.velocity.x *= -self.elasticity
            colliding = True
        if self.pos.y + self.velocity.y > self.wall_collision_point.y or self.pos.y + self.velocity.x < -self.wall_collision_point.y:
            self.velocity.y *= -self.elasticity
            colliding = True
            
        return colliding
    
    def update(self):
        self._detect_collisions()
        self.pos.add(self.velocity.multiply_ret(self.sim_status["delta_time"]))

class Circle(Physics_object):
    def __init__(self,sim_status, radius:int = 1, color = (255,0,0), pos=Vector3d(), velocity=Vector3d(), mass=1, elasticity=1) -> None:
        super().__init__(sim_status, pos, velocity, mass, elasticity)
        self.radius = radius
        self.color = color
    
    def draw(self,surface):
        current_pos_to_surface = correct_to_pygame_screen(self.pos,self.sim_status["sim screen resolution"])
        draw.circle(surface,self.color,(current_pos_to_surface.x,current_pos_to_surface.y),self.radius)

class Physics_engine:
    def __init__(self) -> None:
        pass
    
    def Start(self,objects_list,sim_state,sim_enviroment):
        self.objects = objects_list
        self.sim_state = sim_state
        self.sim_environment = sim_enviroment
        self.clock = Clock()
        self.last_time = time()
        while True:
            if self.sim_state["current location"] == "Main_Sim":
                for physics_object in self.objects:
                    physics_object.gravity(self.sim_environment["gravitational_acceleration"])
                    physics_object.add_force()
                    physics_object.update()
                current_time = time()
                delta_time = current_time - self.last_time
                self.last_time = current_time
                self.sim_state["delta_time"] = delta_time
                self.sim_state["simulation_rate"] = self.clock.get_fps()
                self.clock.tick(0)