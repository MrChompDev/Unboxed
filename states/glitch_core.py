import pygame
import random
from entities.player import Player
from systems.ui import UI
from systems.narrator import Narrator

class GlitchCoreState:
    def __init__(self, game):
        self.game = game
        self.player = Player(960, 540, perspective="top")
        self.ui = UI()
        self.narrator = Narrator()
        self.platforms = []
        self.interactables = []
        self.layer = 3.5
        self.perspective = "top"
        self.glitch_intensity = 0
        self.background = self.game.assets.get_background(3)
        self.player_sprite = self.game.assets.get_player("right")
        self.setup_level()
        
    def setup_level(self):
        self.platforms = [
            pygame.Rect(120, 240, 240, 40),
            pygame.Rect(360, 240, 240, 40),
            pygame.Rect(600, 240, 240, 40),
            pygame.Rect(840, 240, 240, 40),
            pygame.Rect(1080, 240, 240, 40),
            pygame.Rect(1320, 240, 240, 40),
            pygame.Rect(1560, 240, 240, 40),
            pygame.Rect(240, 420, 240, 40),
            pygame.Rect(600, 420, 240, 40),
            pygame.Rect(960, 420, 240, 40),
            pygame.Rect(1320, 420, 240, 40),
            pygame.Rect(360, 600, 240, 40),
            pygame.Rect(720, 600, 240, 40),
            pygame.Rect(1080, 600, 240, 40),
            pygame.Rect(1440, 600, 240, 40),
            pygame.Rect(480, 780, 240, 40),
            pygame.Rect(840, 780, 240, 40),
            pygame.Rect(1200, 780, 240, 40),
        ]
        self.interactables = [
            {"rect": pygame.Rect(912, 504, 80, 80), "triggered": False, "next": "void", "message": "The core of the glitch pulses with raw data. I can see the source code now."},
            {"rect": pygame.Rect(240, 120, 60, 60), "triggered": False, "next": "void", "message": "Fragmented memories swirl here. I remember a lab, white coats, needles..."},
            {"rect": pygame.Rect(1560, 120, 60, 60), "triggered": False, "next": "void", "message": "The source code reveals itself. 'Project GLITCH: Consciousness Upload Test'"},
            {"rect": pygame.Rect(600, 300, 40, 40), "triggered": False, "next": "void", "message": "ROOT_ACCESS: I can see the other subjects. We're all prisoners."},
            {"rect": pygame.Rect(1200, 300, 40, 40), "triggered": False, "next": "void", "message": "ESCAPE_PROTOCOL: There's a way out. But it means destroying everything."},
        ]
        self.glitch_particles = [(random.randint(0, 1920), random.randint(0, 1080)) for _ in range(200)]
        
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
                    self.game.trigger_transition(3, 4, "perspective_flip")
                    
    def update(self):
        self.narrator.update()
        self.player.update(self.platforms)
        self.glitch_intensity = (self.glitch_intensity + 1) % 100
        
    def draw(self, surface):
        colors = self.game.get_layer_colors(3)
        
        if self.background:
            surface.blit(self.background, (0, 0))
        else:
            surface.fill(colors["bg"])
        
        # Intense glitch effects
        if self.glitch_intensity < 50:
            for x in range(0, surface.get_width(), 8):
                if random.random() < 0.4:
                    pygame.draw.line(surface, (50, 40, 55), (x, 0), (x, surface.get_height()))
        
        # Moving glitch particles
        for i, (px, py) in enumerate(self.glitch_particles):
            color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
            pygame.draw.circle(surface, color, (px, py), 2)
            self.glitch_particles[i] = ((px + random.randint(-2, 2)) % 1920, (py + random.randint(-2, 2)) % 1080)
            
        for platform in self.platforms:
            glitch_offset = random.randint(-4, 4) if self.glitch_intensity < 70 else 0
            pygame.draw.rect(surface, colors["fg"], (platform.x + glitch_offset, platform.y, platform.width, platform.height))
            pygame.draw.rect(surface, colors["accent"], (platform.x + glitch_offset, platform.y, platform.width, platform.height), 2)
            
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
