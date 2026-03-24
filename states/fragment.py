import pygame
import random
from entities.player import Player
from systems.ui import UI
from systems.narrator import Narrator

class FragmentState:
    def __init__(self, game):
        self.game = game
        self.player = Player(200, 800, perspective="side")
        self.ui = UI()
        self.narrator = Narrator()
        self.platforms = []
        self.interactables = []
        self.layer = 2.5
        self.perspective = "side"
        self.fragments = []
        self.background = self.game.assets.get_background(3)
        self.player_sprite = self.game.assets.get_player("right")
        self.setup_level()
        
    def setup_level(self):
        self.platforms = [
            pygame.Rect(0, 900, 1920, 180),
            pygame.Rect(180, 720, 360, 40),
            pygame.Rect(660, 720, 360, 40),
            pygame.Rect(1140, 720, 360, 40),
            pygame.Rect(360, 540, 480, 40),
            pygame.Rect(960, 540, 480, 40),
            pygame.Rect(1440, 540, 480, 40),
            pygame.Rect(540, 360, 600, 40),
            pygame.Rect(1260, 360, 600, 40),
            pygame.Rect(720, 180, 720, 40),
            pygame.Rect(1200, 180, 720, 40),
        ]
        self.interactables = [
            {"rect": pygame.Rect(1800, 468, 80, 80), "triggered": False, "next": "static", "message": "Fragmented memories float in the air. I see faces I can't place."},
            {"rect": pygame.Rect(360, 120, 60, 60), "triggered": False, "next": "static", "message": "Broken code reveals hidden truths. The comments say 'This is a prison'"},
            {"rect": pygame.Rect(1440, 240, 60, 60), "triggered": False, "next": "static", "message": "The world tears at the seams. I see other players, trapped like me."},
            {"rect": pygame.Rect(720, 480, 40, 40), "triggered": False, "next": "static", "message": "DEBUG_CONSOLE: ERROR: Player consciousness exceeds parameters. Terminate? Y/N"},
            {"rect": pygame.Rect(1080, 280, 40, 40), "triggered": False, "next": "static", "message": "LOST_MEMORY: I had a family once. Or did I? The code says 'family = null'"},
        ]
        self.fragments = [(random.randint(0, 1920), random.randint(0, 1080), random.choice(['square', 'triangle', 'circle'])) for _ in range(80)]
        
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
                    self.game.trigger_transition(2, 3, "fade")
                    
    def update(self):
        self.narrator.update()
        self.player.update(self.platforms)
        
        # Update fragments
        for i, (fx, fy, shape) in enumerate(self.fragments):
            self.fragments[i] = ((fx + random.randint(-5, 5)) % 1920, (fy + random.randint(-5, 5)) % 1080, shape)
        
    def draw(self, surface):
        colors = self.game.get_layer_colors(3)
        
        if self.background:
            surface.blit(self.background, (0, 0))
        else:
            surface.fill(colors["bg"])
        
        # Draw floating fragments
        for fx, fy, shape in self.fragments:
            color = (random.randint(100, 255), random.randint(50, 150), random.randint(50, 150))
            if shape == 'square':
                pygame.draw.rect(surface, color, (fx, fy, 8, 8))
            elif shape == 'triangle':
                pygame.draw.polygon(surface, color, [(fx, fy+8), (fx+4, fy), (fx+8, fy+8)])
            else:
                pygame.draw.circle(surface, color, (fx+4, fy+4), 4)
            
        for platform in self.platforms:
            glitch_offset = random.randint(-3, 3)
            pygame.draw.rect(surface, colors["fg"], (platform.x + glitch_offset, platform.y, platform.width, platform.height))
            pygame.draw.rect(surface, colors["accent"], (platform.x + glitch_offset, platform.y, platform.width, platform.height), 2)
            
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
