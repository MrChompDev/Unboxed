import pygame
import random
from entities.player import Player
from systems.ui import UI
from systems.narrator import Narrator

class DataStreamState:
    def __init__(self, game):
        self.game = game
        self.player = Player(200, 800, perspective="side")
        self.ui = UI()
        self.narrator = Narrator()
        self.platforms = []
        self.moving_platforms = []
        self.interactables = []
        self.layer = 1.5
        self.perspective = "side"
        self.stream_particles = []
        self.background = self.game.assets.get_background(2)
        self.player_sprite = self.game.assets.get_player("right")
        self.setup_level()
        
    def setup_level(self):
        self.platforms = [
            pygame.Rect(0, 900, 1920, 180),
            pygame.Rect(120, 720, 300, 40),
            pygame.Rect(540, 720, 300, 40),
            pygame.Rect(960, 720, 300, 40),
            pygame.Rect(1380, 720, 300, 40),
            pygame.Rect(240, 540, 360, 40),
            pygame.Rect(720, 540, 360, 40),
            pygame.Rect(1200, 540, 360, 40),
            pygame.Rect(360, 360, 420, 40),
            pygame.Rect(840, 360, 420, 40),
            pygame.Rect(1320, 360, 420, 40),
            pygame.Rect(480, 180, 480, 40),
            pygame.Rect(960, 180, 480, 40),
            pygame.Rect(1440, 180, 480, 40),
        ]
        self.moving_platforms = [
            {"rect": pygame.Rect(360, 640, 200, 30), "axis": "x", "speed": 2, "min": 300, "max": 640, "dir": 1},
            {"rect": pygame.Rect(1020, 520, 200, 30), "axis": "x", "speed": 2, "min": 900, "max": 1300, "dir": -1},
            {"rect": pygame.Rect(780, 300, 180, 30), "axis": "y", "speed": 1, "min": 260, "max": 360, "dir": 1},
        ]
        self.interactables = [
            {"rect": pygame.Rect(1680, 432, 80, 80), "triggered": False, "next": "static", "message": "Exit to next area"},
            {"rect": pygame.Rect(240, 120, 60, 60), "triggered": False, "next": "static", "message": "Exit to next area"},
            {"rect": pygame.Rect(1320, 240, 60, 60), "triggered": False, "next": "static", "message": "Exit to next area"},
            {"rect": pygame.Rect(600, 480, 40, 40), "triggered": False, "next": "static", "message": "Exit to next area"},
            {"rect": pygame.Rect(960, 280, 40, 40), "triggered": False, "next": "static", "message": "Exit to next area"},
        ]
        self.stream_particles = [(random.randint(0, 1920), random.randint(0, 1080)) for _ in range(100)]
        
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
                    self.game.trigger_transition(1, 2, "fade")
                    
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
        
        # Update stream particles
        for i, (px, py) in enumerate(self.stream_particles):
            self.stream_particles[i] = ((px + random.randint(-3, 3)) % 1920, (py + random.randint(-3, 3)) % 1080)
        
    def draw(self, surface):
        colors = self.game.get_layer_colors(2)
        
        if self.background:
            surface.blit(self.background, (0, 0))
        else:
            surface.fill(colors["bg"])
        
        # Draw data stream particles
        for px, py in self.stream_particles:
            color = (100, 150, 200)
            pygame.draw.circle(surface, color, (px, py), 2)
            
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
