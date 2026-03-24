import pygame
from entities.player import Player
from systems.ui import UI
from systems.narrator import Narrator

class CorridorState:
    def __init__(self, game):
        self.game = game
        self.player = Player(260, 800, perspective="side")
        self.ui = UI()
        self.narrator = Narrator()
        self.platforms = []
        self.moving_platforms = []
        self.interactables = []
        self.layer = 1
        self.perspective = "side"
        self.background = self.game.assets.get_background(1)
        self.player_sprite = self.game.assets.get_player("right")
        self.setup_level()
        
    def setup_level(self):
        self.platforms = [
            pygame.Rect(0, 900, 1920, 180),
            pygame.Rect(0, 720, 300, 40),
            pygame.Rect(360, 660, 280, 40),
            pygame.Rect(720, 600, 280, 40),
            pygame.Rect(1080, 540, 280, 40),
            pygame.Rect(1440, 480, 320, 40),
            pygame.Rect(420, 520, 220, 40),
            pygame.Rect(780, 460, 220, 40),
            pygame.Rect(1140, 400, 220, 40),
            pygame.Rect(1460, 340, 220, 40),
            pygame.Rect(900, 340, 220, 40),
            pygame.Rect(600, 280, 220, 40),
            pygame.Rect(300, 220, 220, 40),
            pygame.Rect(600, 160, 220, 40),
            pygame.Rect(960, 140, 240, 40),
        ]
        self.moving_platforms = [
            {"rect": pygame.Rect(520, 620, 180, 30), "axis": "x", "speed": 2, "min": 460, "max": 720, "dir": 1},
            {"rect": pygame.Rect(980, 500, 180, 30), "axis": "x", "speed": 2, "min": 900, "max": 1260, "dir": -1},
            {"rect": pygame.Rect(760, 240, 180, 30), "axis": "y", "speed": 1, "min": 210, "max": 300, "dir": 1},
        ]
        self.interactables = [
            {"rect": pygame.Rect(1680, 432, 80, 80), "triggered": False, "next": "data_stream", "message": "Exit to next area", "broken": False},
            {"rect": pygame.Rect(120, 120, 60, 60), "triggered": False, "next": "data_stream", "message": "Exit to next area", "broken": False},
            {"rect": pygame.Rect(840, 280, 40, 40), "triggered": False, "next": "data_stream", "message": "Exit to next area", "broken": True},
            {"rect": pygame.Rect(480, 480, 40, 40), "triggered": False, "next": "data_stream", "message": "Exit to next area", "broken": True},
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
                    if obj.get("broken", False):
                        # Broken interactable - doesn't work
                        self.narrator.say("This interactable seems to be broken... The connection is lost.")
                        obj["triggered"] = True  # Mark as triggered so it doesn't keep showing message
                    else:
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
        
        if self.narrator.is_done() and self.game.transition.is_complete():
            if any(obj["triggered"] for obj in self.interactables):
                pass
                
    def draw(self, surface):
        colors = self.game.get_layer_colors(1)
        
        if self.background:
            surface.blit(self.background, (0, 0))
        else:
            surface.fill(colors["bg"])
            
        for platform in self.platforms:
            pygame.draw.rect(surface, colors["fg"], platform)
            pygame.draw.rect(surface, colors["accent"], platform, 2)
        for mp in self.moving_platforms:
            pygame.draw.rect(surface, colors["accent"], mp["rect"])
            pygame.draw.rect(surface, colors["fg"], mp["rect"], 2)
            
        for obj in self.interactables:
            if not obj["triggered"]:
                if obj.get("broken", False):
                    # Draw broken interactable with red tint
                    pygame.draw.rect(surface, (150, 50, 50), obj["rect"])
                    pygame.draw.rect(surface, (100, 30, 30), obj["rect"], 3)
                    # Draw broken effect
                    pygame.draw.line(surface, (200, 100, 100), (obj["rect"].x, obj["rect"].y), 
                                   (obj["rect"].x + obj["rect"].width, obj["rect"].y + obj["rect"].height), 3)
                    pygame.draw.line(surface, (200, 100, 100), (obj["rect"].x + obj["rect"].width, obj["rect"].y), 
                                   (obj["rect"].x, obj["rect"].y + obj["rect"].height), 3)
                else:
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
