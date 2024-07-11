import pygame

class Screen_surface:
    def __init__(self,display,width,height,pos,color,refresh) -> None:
        """Simplfies the creation of pygame surfaces. Pygame is required for this to work.

        Args:
            display (Display): Use the self instantiator in the Display class
            width (int): Desired width for surface
            height (int): Desired height for surface
            pos ([int,int]): The position on the screen of the surface
            color ((int,int,int)): Fill color for the Surface
            refresh (bool): The surfaces updates everytime you use the draw function
        """
        self.display = display
        self.surface = pygame.Surface([width,height],pygame.HWSURFACE)
        self.rect = self.surface.get_rect()
        self.pos = pos
        self.real_rect = pygame.Rect(self.pos[0],self.pos[1],self.rect.width,self.rect.height)
        self.color = color
        self.render_objects = {}
        self.refresh = refresh
        self.focused = False
        self.hidden_settings = {}
        self.hidden_settings["Use_background_image"] = True
        self.hidden_settings["Image_surface"] = None
        self.hidden_settings["Fps_counter"] = False
        self.hidden_settings["Sim_frame_counter"] = False
        
        self._fps_font = pygame.font.Font('freesansbold.ttf', 20)
    
    def resize(self):
        pass
    
    def get_size(self):
        return self.surface.get_size()
    
    def check_objects_for_text_input(self,text):
        if self.focused:
            for object_name in self.render_objects.values():
                if object_name.allow_text_input:
                    object_name.text_input(text)
    
    def check_objects_for_click(self,mouse_pos):
        for object_name in self.render_objects.values():
            if object_name.clickable:
                object_name.check_if_clicked(mouse_pos,self.pos)
                
    def _render_sim_time_counter(self):
        text = self._fps_font.render(f"{round(self.display.sim.sim_status["simulation_rate"])}",True,(255,255,255))
        text_rect = text.get_rect()
        text_rect.center = [self.rect.width / 30,self.rect.height / 15]
        self.surface.blit(text,text_rect)
    
    def _render_fps_counter(self):
        text = self._fps_font.render(f"{round(self.display.clock.get_fps())}",True,(255,255,255))
        text_rect = text.get_rect()
        text_rect.center = [self.rect.width / 30,self.rect.height / 25]
        self.surface.blit(text,text_rect)
    
    def draw_from_list(self,draw_list):
        if self.refresh:
            if self.hidden_settings["Use_background_image"]:
                if self.hidden_settings["Image_surface"] != None:
                    self.surface.blit(self.hidden_settings["Image_surface"],[0,0])
                else:
                    self.surface.fill(self.color)
            else:
                self.surface.fill(self.color)
        for item in draw_list:
            item.draw()
        if self.hidden_settings["Fps_counter"]:
            self._render_fps_counter()
        if self.hidden_settings["Sim_frame_counter"]:
            self._render_sim_time_counter()
        self.display.screen.blit(self.surface,self.pos)
        if self.refresh:
            pygame.display.update(self.real_rect)
    
    def draw(self):
        if self.refresh:
            if self.hidden_settings["Use_background_image"]:
                if self.hidden_settings["Image_surface"] != None:
                    self.surface.blit(self.hidden_settings["Image_surface"],[0,0])
                else:
                    self.surface.fill(self.color)
            else:
                self.surface.fill(self.color)
        for object_name in self.render_objects.values():
            object_name.draw()
        if self.hidden_settings["Fps_counter"]:
            self._render_fps_counter()
        self.display.screen.blit(self.surface,self.pos)
        if self.refresh:
            pygame.display.update(self.real_rect)

class TextInput:
    def __init__(self,display,surface,x,y,width,height,font_color,max_character_count) -> None:
        self.display = display
        self.surface = surface
        self.selected = False
        self.top_x = x
        self.top_y = y
        self.width = width
        self.height = height
        self.font_size = height
        self.font_color = font_color
        self.max_character_count = max_character_count
        self.surface_pos = None
        self.clickable = True
        self.allow_text_input = True
        
        self.rect = pygame.Rect(self.top_x,self.top_y,self.width,self.height)
        self.rect.center = [self.top_x,self.top_y]
        
        if self.rect.bottom < self.surface.get_height() and self.rect.top > 0:
            self.onscreen = True
        else:
            self.onscreen = False
        
        self.hidden_settings = {}
        self.hidden_settings["border"] = False
        self.hidden_settings["border_color"] = (0,0,0)
        self.hidden_settings["border_width"] = 1
        self.hidden_settings["background"] = False
        self.hidden_settings["background_color"] = (0,0,0)
        self.hidden_settings["data_type"] = False
        self.hidden_settings["data_type_default"] = "str"
        self.hidden_settings["selected_color"] = pygame.Color('lightskyblue3')
        
        self.text = ""
        self.font = pygame.font.Font('freesansbold.ttf', self.font_size)
        
        self.active = False
        
        self.changed = True
    
    def move(self,x_movement,y_movement):
        self.top_x += x_movement
        self.top_y += y_movement
        
        self.rect = pygame.Rect(0,0,self.width,self.height)
        
        self.rect.center = [self.top_x,self.top_y]
        
        self.changed = True
    
    def text_input(self,text):
        if self.active:
            if text == "back":
                self.text = self.text[:-1]
            
            elif text == "escape":
                self.active = False
            
            elif text == "enter":
                self.active = False
            
            elif not len(self.text) >= self.max_character_count:
                if self.hidden_settings["data_type"] == "int":
                    try:
                        float(text)
                        self.text += text
                    except:
                        pass
                else:
                    self.text += text
                
                self.changed = True
    
    def clicked(self):
        self.active = True
        self.changed = True
    
    def check_if_clicked(self,mouse_pos,surface_pos):
        good_spot = True

        if (mouse_pos[0] < surface_pos[0] + self.top_x + (self.width/2)) and (mouse_pos[0] > surface_pos[0] + self.top_x - (self.width/2)):
            pass
        else:
            good_spot = False

        if (mouse_pos[1] < surface_pos[1] + self.top_y + (self.height/2)) and (mouse_pos[1] > surface_pos[1] + self.top_y - (self.height/2)):
            pass
        else:
            good_spot = False

        if good_spot == True:
            self.clicked()
        else:
            self.unclicked()

    def unclicked(self):
        self.active = False
        self.changed = True
    
    def surface_resize(self):
        if self.rect.top < self.surface.get_height() and self.rect.bottom > 0:
            self.onscreen = True
        else:
            self.onscreen = False
        
        if self.rect.left < self.surface.get_width() and self.rect.right > 0:
            self.onscreen = True
        else:
            self.onscreen = False
        
        self.changed = True
    
    def draw(self):
        if self.onscreen:
            if self.hidden_settings["border"]:
                pygame.draw.rect(self.surface,self.hidden_settings["border_color"], self.rect,width=self.hidden_settings["border_width"])

            if self.active:
                text = self.font.render(f"{self.text}", True, self.font_color, self.hidden_settings["selected_color"])

            else:
                if self.hidden_settings["background"]:
                    text = self.font.render(f"{self.text}", True, self.font_color, self.hidden_settings["background_color"])

                else:
                    text = self.font.render(f"{self.text}", True, self.font_color)

            self.surface.blit(text,self.rect)

            self.changed = False

class Text:
    def __init__(self,surface,text,font_size,text_color,x_pos,y_pos,width,height) -> None:
        self.surface = surface
        self.text = text
        self.font = pygame.font.Font('freesansbold.ttf', font_size)
        self.font_size = font_size
        self.text_color = text_color
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.width = width
        self.height = height
        self.rect = pygame.Rect(0,0,self.width,self.height)
        self.rect.center = self.x_pos,self.y_pos
        self.changed = True
        self.clickable = False
        self.allow_text_input = False
        
        if self.rect.bottom < self.surface.get_height() and self.rect.top > 0:
            self.onscreen = True
        else:
            self.onscreen = False
        
        self.hidden_settings = {}
        self.hidden_settings["border"] = False
        self.hidden_settings["border_color"] = (0,0,0)
        self.hidden_settings["border_width"] = 1
        self.hidden_settings["background"] = False
        self.hidden_settings["background_color"] = (0,0,0)
    
    def surface_resize(self):
        if self.rect.top < self.surface.get_height() and self.rect.bottom > 0:
            self.onscreen = True
        else:
            self.onscreen = False
        
        if self.rect.left < self.surface.get_width() and self.rect.right > 0:
            self.onscreen = True
        else:
            self.onscreen = False
        
        self.changed = True
    
    def move(self,x_movement,y_movement):
        self.top_x += x_movement
        self.top_y += y_movement
        
        self.rect = pygame.Rect(0,0,self.width,self.height)
        
        self.rect.center = [self.top_x,self.top_y]
        
        self.changed = True
    
    def draw(self):
        if self.onscreen:
            self.changed = True
            if self.changed == True:
                if self.hidden_settings["border"]:
                    pygame.draw.rect(self.surface,self.hidden_settings["border_color"], self.rect,width=self.hidden_settings["border_width"])

                else:
                    if self.hidden_settings["background"]:
                        text = self.font.render(f"{self.text}", True, self.text_color, self.hidden_settings["background_color"])

                    else:
                        text = self.font.render(f"{self.text}", True, self.text_color)
                
                self.surface.blit(text,self.rect)
                    
                self.changed = False