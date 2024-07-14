import math

class Vector3d:
    def __init__(self,x = 0.0,y = 0.0,z = 0.0) -> None:
        self.x = x
        self.y = y
        self.z = z
    
    def add(self,vector3):
        self.x += vector3.x
        self.y += vector3.y
        self.z += vector3.z
    
    def subtract(self,vector3):
        self.x -= vector3.x
        self.y -= vector3.y
        self.z -= vector3.z
        
    def multiply(self,num):
        self.x *= num
        self.y *= num
        self.z *= num
    
    def divide(self,num):
        self.x /= num
        self.y /= num
        self.z /= num
    
    def add_ret(self,vector3):
        return Vector3d(self.x + vector3.x,self.y + vector3.y,self.z + vector3.z)
    
    def subtract_ret(self,vector3):
        return Vector3d(self.x - vector3.x,self.y - vector3.y,self.z - vector3.z)
        
    def multiply_ret(self,num):
        return Vector3d(self.x * num,self.y * num,self.z * num)
    
    def divide_ret(self,num):
        if num != 0:
            return Vector3d(self.x / num,self.y / num,self.z / num)
        return Vector3d(0,0,0)
    
    def return_values_in_string(self):
        return f"{self.x},{self.y},{self.z}"
    
def normalize_vector(vector3d):
    normalizing_value = ((vector3d.x ** 2) + (vector3d.y ** 2) + (vector3d.z ** 2)) ** 2
    return Vector3d(vector3d.x / normalizing_value,vector3d.y / normalizing_value,vector3d.z / normalizing_value)

def convert_angles_to_vector3(x_angle = 0,y_angle = 0,z_angle = 0):
    x_angle = math.cos(math.radians(x_angle))
    y_angle = math.sin(math.radians(y_angle))
    z_angle = math.cos(math.radians(z_angle))
    return Vector3d(x_angle,y_angle,z_angle)

def correct_to_pygame_screen(pos:Vector3d,screen_size):
    return Vector3d((pos.x - screen_size[0]/2) * -1,(pos.y - screen_size[1]/2) * -1)

def correct_to_coordinate_system(pos:Vector3d,screen_size):
    return Vector3d((pos.x + screen_size[0]/2) * -1,(pos.y + screen_size[1]/2) * -1)