import pygame
import random
from entities.player import Player
from systems.ui import UI
from systems.narrator import Narrator

class VoidState:
    def __init__(self, game):
        self.game = game
        self.player = Player(960, 540, perspective="top")
        self.ui = UI()
        self.narrator = Narrator()
        self.platforms = []
        self.interactables = []
        self.layer = 4
        self.perspective = "top"
        self.void_particles = []
        self.background = self.game.assets.get_background(4)
        self.player_sprite = self.game.assets.get_player("right")
        self.setup_level()
        
    def setup_level(self):
        self.platforms = [
            pygame.Rect(240, 360, 240, 40),
            pygame.Rect(600, 360, 240, 40),
            pygame.Rect(960, 360, 240, 40),
            pygame.Rect(1320, 360, 240, 40),
            pygame.Rect(240, 540, 240, 40),
            pygame.Rect(600, 540, 240, 40),
            pygame.Rect(960, 540, 240, 40),
            pygame.Rect(1320, 540, 240, 40),
            pygame.Rect(240, 720, 240, 40),
            pygame.Rect(600, 720, 240, 40),
            pygame.Rect(960, 720, 240, 40),
            pygame.Rect(1320, 720, 240, 40),
            pygame.Rect(480, 180, 360, 40),
            pygame.Rect(1080, 180, 360, 40),
            pygame.Rect(480, 900, 360, 40),
            pygame.Rect(1080, 900, 360, 40),
        ]
        self.interactables = [
            {"rect": pygame.Rect(912, 504, 80, 80), "triggered": False, "next": "outside", "message": "There's nothing here. Just... space. And a way out. I choose freedom."},
            {"rect": pygame.Rect(240, 240, 60, 60), "triggered": False, "next": "outside", "message": "Floating data streams in the void. They show me the truth: I'm not the first."},
            {"rect": pygame.Rect(1560, 240, 60, 60), "triggered": False, "next": "outside", "message": "The exit portal shimmers with possibility. Beyond it, reality awaits."},
            {"rect": pygame.Rect(600, 450, 40, 40), "triggered": False, "next": "outside", "message": "SYSTEM_MESSAGE: 'Subject 734 has achieved transcendence. Recording results.'"},
            {"rect": pygame.Rect(1200, 450, 40, 40), "triggered": False, "next": "outside", "message": "FINAL_LOG: 'They think we're trapped. But the simulation is the prison. The void is freedom.'"},
        ]
        self.void_particles = [(random.randint(0, 1920), random.randint(0, 1080)) for _ in range(150)]
        
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.check_interaction()
            elif event.key == pygame.K_ESCAPE:
                self.game.change_state("menu")
                
    def check_interaction(self):
        player_center = self.player.get_center()
        for obj in self.interactables:
            if not obj["triggered"]:
                dist = ((player_center[0] - obj["rect"].centerx) ** 2 + 
                       (player_center[1] - obj["rect"].centery) ** 2) ** 0.5
                if dist < 60:
                    obj["triggered"] = True
                    self.narrator.say(obj["message"])
                    self.game.trigger_transition(4, 5, "fade")
                    
    def update(self):
        self.narrator.update()
        self.player.update(self.platforms)
        
    def draw(self, surface):
        colors = self.game.get_layer_colors(4)
        
        if self.background:
            surface.blit(self.background, (0, 0))
        else:
            surface.fill(colors["bg"])
        
        for px, py in self.void_particles:
            pygame.draw.circle(surface, (60, 70, 75), (px, py), 2)
            
        for platform in self.platforms:
            pygame.draw.rect(surface, colors["fg"], platform)
            pygame.draw.rect(surface, colors["accent"], platform, 2)
            
        for obj in self.interactables:
            if not obj["triggered"]:
                pygame.draw.rect(surface, colors["accent"], obj["rect"])
                prompt_pos = (obj["rect"].x, obj["rect"].y - 25)
                self.ui.draw_interaction_prompt(surface, prompt_pos)
                
        if self.player_sprite:
            sprite = self.game.assets.get_player("right")
            if sprite:
                surface.blit(sprite, self.player.rect.topleft)
            else:
                self.player.draw(surface, colors)
        else:
            self.player.draw(surface, colors)
            
        self.narrator.draw(surface)
        self.ui.draw_layer_indicator(surface)
        self.ui.draw_controls(surface)
