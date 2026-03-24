import pygame
import random
from entities.player import Player
from systems.ui import UI
from systems.narrator import Narrator

class StaticState:
    def __init__(self, game):
        self.game = game
        self.player = Player(60, 780, perspective="side")
        self.ui = UI()
        self.narrator = Narrator()
        self.platforms = []
        self.moving_platforms = []
        self.interactables = []
        self.layer = 3
        self.perspective = "side"
        self.static_intensity = 0
        self.background = self.game.assets.get_background(3)
        self.player_sprite = self.game.assets.get_player("right")
        self.setup_level()
        
    def setup_level(self):
        self.platforms = [
            pygame.Rect(0, 900, 1920, 180),
            pygame.Rect(120, 810, 180, 40),
            pygame.Rect(360, 810, 180, 40),
            pygame.Rect(600, 810, 180, 40),
            pygame.Rect(840, 810, 180, 40),
            pygame.Rect(1080, 810, 180, 40),
            pygame.Rect(1320, 810, 180, 40),
            pygame.Rect(1560, 810, 180, 40),
            pygame.Rect(240, 690, 240, 40),
            pygame.Rect(600, 690, 240, 40),
            pygame.Rect(960, 690, 240, 40),
            pygame.Rect(1320, 690, 240, 40),
            pygame.Rect(360, 570, 300, 40),
            pygame.Rect(720, 570, 300, 40),
            pygame.Rect(1080, 570, 300, 40),
            pygame.Rect(1440, 570, 300, 40),
            pygame.Rect(480, 450, 360, 40),
            pygame.Rect(840, 450, 360, 40),
            pygame.Rect(1200, 450, 360, 40),
            pygame.Rect(600, 330, 480, 40),
            pygame.Rect(1080, 330, 480, 40),
        ]
        self.moving_platforms = [
            {"rect": pygame.Rect(420, 640, 200, 30), "axis": "x", "speed": 2, "min": 360, "max": 720, "dir": 1},
            {"rect": pygame.Rect(1080, 520, 200, 30), "axis": "x", "speed": 2, "min": 1000, "max": 1380, "dir": -1},
            {"rect": pygame.Rect(780, 400, 180, 30), "axis": "y", "speed": 1, "min": 360, "max": 480, "dir": 1},
        ]
        self.interactables = [
            {"rect": pygame.Rect(1800, 558, 80, 80), "triggered": False, "next": "echo", "message": "Exit to next area"},
            {"rect": pygame.Rect(240, 240, 60, 60), "triggered": False, "next": "echo", "message": "Exit to next area"},
            {"rect": pygame.Rect(1320, 180, 60, 60), "triggered": False, "next": "echo", "message": "Exit to next area"},
            {"rect": pygame.Rect(840, 480, 40, 40), "triggered": False, "next": "echo", "message": "Exit to next area"},
            {"rect": pygame.Rect(480, 240, 40, 40), "triggered": False, "next": "echo", "message": "Exit to next area"},
        ]
        
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
                    
                    # Trigger mid-game cutscene on specific interaction
                    if obj["rect"] == pygame.Rect(1320, 180, 60, 60):
                        self.game.trigger_cutscene("mid")
                    
                    self.game.trigger_transition(3, 4, "perspective_flip")
                    
    def update(self):
        self.narrator.update()
        for mp in self.moving_platforms:
            if mp["axis"] == "x":
                mp["rect"].x += mp["speed"] * mp["dir"]
                if mp["rect"].x < mp["min"] or mp["rect"].x > mp["max"]:
                    mp["dir"] *= -1
                    mp["rect"].x = max(mp["min"], min(mp["rect"].x, mp["max"]))
            else:
                mp["rect"].y += mp["speed"] * mp["dir"]
                if mp["rect"].y < mp["min"] or mp["rect"].y > mp["max"]:
                    mp["dir"] *= -1
                    mp["rect"].y = max(mp["min"], min(mp["rect"].y, mp["max"]))
        platforms = self.platforms + [mp["rect"] for mp in self.moving_platforms]
        self.player.update(platforms)
        self.static_intensity = (self.static_intensity + 1) % 100
        
    def draw(self, surface):
        colors = self.game.get_layer_colors(3)
        
        if self.background:
            surface.blit(self.background, (0, 0))
        else:
            surface.fill(colors["bg"])
        
        if self.static_intensity < 50:
            for x in range(0, surface.get_width(), 4):
                if random.random() < 0.3:
                    pygame.draw.line(surface, (50, 40, 55), (x, 0), (x, surface.get_height()))
                    
        for platform in self.platforms:
            pygame.draw.rect(surface, colors["fg"], platform)
            pygame.draw.rect(surface, colors["accent"], platform, 2)
        for mp in self.moving_platforms:
            pygame.draw.rect(surface, colors["accent"], mp["rect"])
            pygame.draw.rect(surface, colors["fg"], mp["rect"], 2)
            
        for obj in self.interactables:
            if not obj["triggered"]:
                pygame.draw.rect(surface, colors["accent"], obj["rect"])
                prompt_pos = (obj["rect"].x, obj["rect"].y - 25)
                self.ui.draw_interaction_prompt(surface, prompt_pos)
                
        if self.player_sprite:
            direction = "right" if self.player.facing_right else "left"
            sprite = self.game.assets.get_player(direction)
            if sprite:
                surface.blit(sprite, self.player.rect.topleft)
            else:
                self.player.draw(surface, colors)
        else:
            self.player.draw(surface, colors)
            
        self.narrator.draw(surface)
        self.ui.draw_layer_indicator(surface)
        self.ui.draw_controls(surface)
