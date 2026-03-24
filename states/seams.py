import pygame
from entities.player import Player
from systems.ui import UI
from systems.narrator import Narrator

class SeamsState:
    def __init__(self, game):
        self.game = game
        self.player = Player(200, 800, perspective="side")
        self.ui = UI()
        self.narrator = Narrator()
        self.platforms = []
        self.interactables = []
        self.layer = 2
        self.perspective = "side"
        self.seam_glitch_timer = 0
        self.background = self.game.assets.get_background(2)
        self.player_sprite = self.game.assets.get_player("right")
        self.setup_level()
        
    def setup_level(self):
        self.platforms = [
            pygame.Rect(0, 900, 1920, 180),
            pygame.Rect(120, 756, 240, 40),
            pygame.Rect(480, 756, 240, 40),
            pygame.Rect(840, 756, 240, 40),
            pygame.Rect(1200, 756, 240, 40),
            pygame.Rect(1560, 756, 240, 40),
            pygame.Rect(240, 612, 192, 40),
            pygame.Rect(600, 612, 192, 40),
            pygame.Rect(960, 612, 192, 40),
            pygame.Rect(1320, 612, 192, 40),
            pygame.Rect(360, 468, 144, 40),
            pygame.Rect(720, 468, 144, 40),
            pygame.Rect(1080, 468, 144, 40),
            pygame.Rect(1440, 468, 144, 40),
            pygame.Rect(480, 324, 192, 40),
            pygame.Rect(960, 324, 192, 40),
            pygame.Rect(1440, 324, 192, 40),
        ]
        self.interactables = [
            {"rect": pygame.Rect(1800, 468, 80, 80), "triggered": False, "next": "fragment", "message": "The seams are splitting. Reality is unraveling. I can see the code behind it all."},
            {"rect": pygame.Rect(240, 180, 60, 60), "triggered": False, "next": "fragment", "message": "Glitching fragments float in the air. They whisper my name..."},
            {"rect": pygame.Rect(1320, 240, 60, 60), "triggered": False, "next": "fragment", "message": "The code is visible through the cracks. I see function calls to 'create_player()'"},
            {"rect": pygame.Rect(600, 180, 40, 40), "triggered": False, "next": "fragment", "message": "SYSTEM_WARNING: Reality cohesion at 47%. Memory leaks detected."},
            {"rect": pygame.Rect(360, 360, 40, 40), "triggered": False, "next": "fragment", "message": "ECHO_MESSAGE: 'You're not real. None of this is real.' - Anonymous"},
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
                    self.game.trigger_transition(2, 3, "fade")
                    
    def update(self):
        self.narrator.update()
        self.player.update(self.platforms)
        self.seam_glitch_timer += 1
        
    def draw(self, surface):
        colors = self.game.get_layer_colors(2)
        
        if self.background:
            surface.blit(self.background, (0, 0))
        else:
            surface.fill(colors["bg"])
        
        for i, platform in enumerate(self.platforms):
            glitch_offset = 0
            if i > 0 and self.seam_glitch_timer % 60 < 30:
                glitch_offset = pygame.math.Vector2(2, 0).x
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
