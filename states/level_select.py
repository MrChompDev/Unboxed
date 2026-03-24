import pygame
from entities.player import Player
from systems.ui import UI
from systems.narrator import Narrator

class LevelSelectState:
    def __init__(self, game):
        self.game = game
        self.ui = UI()
        self.levels = [
            {"name": "THE CORRIDOR", "state": "corridor", "unlocked": True},
            {"name": "DATA STREAMS", "state": "data_stream", "unlocked": True},
            {"name": "THE STATIC", "state": "static", "unlocked": True},
            {"name": "OUTSIDE", "state": "outside", "unlocked": True},
        ]
        self.selected = 0
        self.background = self.game.assets.get_background(1)
        
    def handle_event(self, event):
        if event.type != pygame.KEYDOWN:
            return
            
        if event.key == pygame.K_UP or event.key == pygame.K_w:
            self.selected = (self.selected - 1) % len(self.levels)
        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
            self.selected = (self.selected + 1) % len(self.levels)
        elif event.key == pygame.K_RETURN:
            self.start_level()
        elif event.key == pygame.K_ESCAPE:
            self.game.change_state("menu")
                
    def start_level(self):
        level_map = {
            0: "corridor",
            1: "data_stream", 
            2: "static",
            3: "outside"
        }
        
        level_name = level_map.get(self.selected)
        if level_name and level_name in self.game.states:
            self.game.change_state(level_name)
                
    def update(self):
        pass
        
    def draw(self, surface):
        if self.background:
            surface.blit(self.background, (0, 0))
        else:
            surface.fill((15, 15, 20))
        
        title = self.ui.font_large.render("SELECT LEVEL", True, (200, 200, 210))
        surface.blit(title, ((surface.get_width() - title.get_width()) // 2, 100))
        
        for i, option in enumerate(self.options):
            color = (200, 200, 210) if i == self.selected else (80, 80, 90)
            text = self.ui.font_medium.render(option, True, color)
            surface.blit(text, (200, 200 + i * 50))
                
        hint = self.ui.font_small.render("Use UP/DOWN to select, ENTER to start, ESC for menu", True, (60, 60, 70))
        surface.blit(hint, ((surface.get_width() - hint.get_width()) // 2, 700))
