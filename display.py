from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
from display_features import *

class Display:
    def __init__(self,sim) -> None:
        """Used to display and edit objects and enviroment variables

        Args:
            sim (Main Sim Class): Allows for backtracking to get the sim objects
        """
        self.sim = sim
        pygame.init()
        self.screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN,pygame.DOUBLEBUF | pygame.HWSURFACE)
        self.clock = pygame.time.Clock()
        
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()
        self.options_area = self.screen_height - ((self.screen_height / 4) * 3)
        
        #My self made Screen_surface classes that make creating an managing Surfaces easier!
        self.object_display_surface = Screen_surface(self,self.screen_width - self.options_area,self.screen_height - self.options_area + (self.screen_height / 20),[0,0],(0,0,0),True)
        self.side_display_surface = Screen_surface(self,self.options_area,self.screen_height - self.options_area + (self.screen_height / 20),[self.object_display_surface.get_size()[0],0],(0,0,255),True)
        self.bottom_display_surface = Screen_surface(self,self.screen_width,self.options_area + (self.screen_height / 20),self.object_display_surface.rect.bottomleft,(0,255,0),True)
        
        self.object_display_surface.hidden_settings["Fps_counter"] = True
        self.object_display_surface.hidden_settings["Sim_frame_counter"] = True
        
        self.side_display_surface.hidden_settings["Use_background_image"] = True
        self.side_display_surface.hidden_settings["Image_surface"] = self._create_display_gradient(self.side_display_surface.surface.get_width(),self.side_display_surface.surface.get_height())
        
        self.bottom_display_surface.hidden_settings["Use_background_image"] = True
        self.bottom_display_surface.hidden_settings["Image_surface"] = self._create_display_gradient(self.bottom_display_surface.surface.get_width(),self.bottom_display_surface.surface.get_height())
        
        print(40 / self.side_display_surface.get_size()[1])
        self.side_display_surface.render_objects["Windspeed_text"] = Text(self.side_display_surface.surface,"Windspeed",10,(0,0,0),self.side_display_surface.get_size()[0] / 2,self.side_display_surface.get_size()[1] / 3,self.side_display_surface.get_size()[0] * 0.4583,self.side_display_surface.get_size()[1] * 0.03472)
        
        self.side_display_surface.render_objects["Windspeed_slider"] = TextInput(self,self.side_display_surface.surface,self.side_display_surface.get_size()[0] / 2,self.side_display_surface.get_size()[1] / 2,165,40,(0,0,0),5)
        self.side_display_surface.render_objects["Windspeed_slider"].text = ""
        self.side_display_surface.render_objects["Windspeed_slider"].hidden_settings["background"] = True
        self.side_display_surface.render_objects["Windspeed_slider"].hidden_settings["background_color"] = (0,0,0)



    def _main_menu_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    mouse_pos = pygame.mouse.get_pos()
            
            if event.type == pygame.MOUSEBUTTONUP:
                pass
    
    def _main_menu_render(self):
        pygame.display.flip()
        self.clock.tick(60)
    
    def main_menu(self):
        """Renders and get input for the Main Menu
        """
        self._main_menu_input()
        self._main_menu_render()



    def _main_sim_object_display(self):
        self.object_display_surface.draw_from_list(self.sim.objects)
    
    def _main_sim_side_display(self):
        self.side_display_surface.draw()
    
    def _main_sim_bottom_display(self):
        self.bottom_display_surface.draw()
    
    def _create_display_gradient(self,width,height):
        side_display_gradient = pygame.Surface((2,2))
        pygame.draw.line(side_display_gradient, (25,25,25), (0,0), (0,1))
        pygame.draw.line(side_display_gradient, (0,0,0), (1,0), (1,1))
        return pygame.transform.smoothscale(side_display_gradient, (width,height))



    def _main_sim_render(self):
        self._main_sim_object_display()
        self._main_sim_side_display()
        self._main_sim_bottom_display()
        self.clock.tick(0)
    
    def _main_sim_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.side_display_surface.real_rect.collidepoint(mouse_pos[0],mouse_pos[1]):
                        self.side_display_surface.focused = True
                        self.side_display_surface.check_objects_for_click(mouse_pos)
            
            if event.type == pygame.MOUSEBUTTONUP:
                pass
            
            if event.type == pygame.KEYDOWN:
                if self.side_display_surface.focused:
                    if event.key == pygame.K_BACKSPACE:
                        self.side_display_surface.check_objects_for_text_input("back")
                    elif event.key == pygame.K_ESCAPE:
                        self.side_display_surface.check_objects_for_text_input("escape")
                    elif event.key == pygame.K_RETURN:
                        self.side_display_surface.check_objects_for_text_input("enter")
                    else:
                        self.side_display_surface.check_objects_for_text_input(event.unicode)
    
    def main_sim(self):
        """Renders and get input for the Sim
        """
        self._main_sim_input()
        self._main_sim_render()