from display import Display
from physics import Physics_engine
from multiprocessing import Process,freeze_support,Manager,cpu_count
from math3d import Vector3d

class Sim:
    def __init__(self) -> None:
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
        
        self.sim_enviroment["gravitational_acceleration"] = Vector3d(0,9.81,0)
        self.sim_enviroment["wind_speed"] = 0
        self.sim_enviroment["wind_direction"] = Vector3d(0,0,0)
        self.sim_enviroment["air_density"] = 0.635
        
        self.physics_process = Process(target=self.engine.Start,args=(self.objects,self.sim_status,self.sim_enviroment))
    
    def Run(self):
        """Start the Sim
        """
        self.physics_process.start()
        
        while self.sim_status["running"]:
            if self.sim_status["current location"] == "Main_Menu":
                self.display.main_menu()
        
            elif self.sim_status["current location"] == "Main_Sim":
                self.display.main_sim()

if __name__ == "__main__":
    freeze_support()
    app = Sim()
    app.Run()