import pygame
from systems.ui import UI
from utils.assets import AssetLoader

class SettingsState:
    def __init__(self, game):
        self.game = game
        self.ui = UI()
        self.assets = AssetLoader()
        self.background = self.game.assets.get_background(1)
        
        # Settings options
        self.settings = {
            "music_volume": 0.5,
            "sound_volume": 0.5,
        }
        
        self.selected = 0
        self.options = ["Music Volume", "Sound Volume", "Back"]
        
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.change_state("menu")
            elif event.key == pygame.K_UP:
                self.selected = (self.selected - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected = (self.selected + 1) % len(self.options)
            elif event.key == pygame.K_LEFT:
                if self.selected == 0:  # Music volume
                    self.settings["music_volume"] = max(0, self.settings["music_volume"] - 0.1)
                    self.game.music.set_volume(self.settings["music_volume"])
                elif self.selected == 1:  # Sound volume
                    self.settings["sound_volume"] = max(0, self.settings["sound_volume"] - 0.1)
            elif event.key == pygame.K_RIGHT:
                if self.selected == 0:  # Music volume
                    self.settings["music_volume"] = min(1.0, self.settings["music_volume"] + 0.1)
                    self.game.music.set_volume(self.settings["music_volume"])
                elif self.selected == 1:  # Sound volume
                    self.settings["sound_volume"] = min(1.0, self.settings["sound_volume"] + 0.1)
            elif event.key == pygame.K_RETURN:
                if self.selected == 2:  # Back
                    self.game.change_state("menu")
                    
    def update(self):
        pass
        
    def draw(self, surface):
        if self.background:
            surface.blit(self.background, (0, 0))
        else:
            surface.fill((15, 15, 20))
            
        # Draw title
        title = self.ui.font_large.render("SETTINGS", True, (200, 200, 210))
        surface.blit(title, ((surface.get_width() - title.get_width()) // 2, 100))
        
        # Draw settings options
        start_y = 300
        for i, option in enumerate(self.options):
            color = (200, 200, 210) if i == self.selected else (80, 80, 90)
            
            if i == 0:  # Music volume
                text = f"Music Volume: {int(self.settings['music_volume'] * 100)}%"
            elif i == 1:  # Sound volume
                text = f"Sound Volume: {int(self.settings['sound_volume'] * 100)}%"
            else:  # Back
                text = option
                
            text_surface = self.ui.font_medium.render(text, True, color)
            surface.blit(text_surface, (300, start_y + i * 60))
            
        # Draw controls hint
        hint = self.ui.font_small.render("Use UP/DOWN to select, LEFT/RIGHT to adjust, ENTER to confirm", True, (80, 80, 90))
        surface.blit(hint, ((surface.get_width() - hint.get_width()) // 2, surface.get_height() - 30))
