from display import Display
from physics import Physics_engine,Circle
from multiprocessing import Process,freeze_support,Manager,cpu_count
from math3d import Vector3d

class Sim:
    def __init__(self) -> None:
        """The central nervous system of the simulator.
        It connects up the display to the physics engine and runs the main loop.
        """
        self.display = Display(self)
        self.engine = Physics_engine()
        
        self.process_manager = Manager()
        self.objects = self.process_manager.list()
        self.sim_status = self.process_manager.dict()
        self.sim_enviroment = self.process_manager.dict()
        
        self.sim_status["running"] = True
        self.sim_status["current location"] = "Main_Sim"
        self.sim_status["cpu count"] = cpu_count()-2
        self.sim_status["sim screen resolution"] = self.display.object_display_surface.get_size()
        self.sim_status["simulation_rate"] = 0
        self.sim_status["delta_time"] = 0
        
        self.sim_enviroment["gravitational_acceleration"] = Vector3d(0,-9.81,0)
        self.sim_enviroment["wind_speed"] = 0
        self.sim_enviroment["wind_direction"] = Vector3d(0,0,0)
        self.sim_enviroment["air_density"] = 0.635
        
        #Uses Process to use a second core to process the physics.
        #I feed in all of the created Manager() items above into it.
        
        self.physics_process = Process(target=self.engine.Start,args=(self.objects,self.sim_status,self.sim_enviroment))
    
    def Create_object(self):
        """Creates a new object to simulate and display
        """
        #This adds a new object to the shared memory between the engine and the display.
        self.objects.append(Circle(self.sim_status,10,(255,0,0),Vector3d(),Vector3d(),1,1))
    
    def Run(self):
        """Starts the Sim
        """
        self.physics_process.start()
        self.Create_object()
        while self.sim_status["running"]:
            if self.sim_status["current location"] == "Main_Menu":
                #Function is located in display.py in Display class
                self.display.main_menu()
        
            elif self.sim_status["current location"] == "Main_Sim":
                #Function is located in display.py in Display class
                self.display.main_sim()
            
            if not self.physics_process.is_alive():
                self.sim_status["running"] = False
                print("Physics process has crashed!")

if __name__ == "__main__":
    freeze_support()
    app = Sim()
    app.Run()