import pygame
import os
import sys

class AssetLoader:
    def __init__(self):
        if getattr(sys, "frozen", False):
            base_dir = sys._MEIPASS
        else:
            base_dir = os.path.join(os.path.dirname(__file__), "..")
        self.base_path = os.path.join(base_dir, "Assets")
        self.backgrounds = {}
        self.players = {}
        self.fonts = {}
        self.load_all()
        
    def load_background(self, layer):
        if layer == 5:
            path = os.path.join(self.base_path, "Backgrounds", "backgroundColorGrass.png")
        else:
            path = os.path.join(self.base_path, "Backgrounds", f"set{layer}_background.png")
        if os.path.exists(path):
            img = pygame.image.load(path)
            return pygame.transform.scale(img, (1920, 1080))
        return None
        
    def load_player_sprite(self, direction="right"):
        path = os.path.join(self.base_path, "Players", "Player Red", "playerRed_stand.png")
        if os.path.exists(path):
            img = pygame.image.load(path)
            if direction == "left":
                img = pygame.transform.flip(img, True, False)
            return pygame.transform.scale(img, (48, 96))
        return None
        
    def load_font(self, name="Kenney Future", size=24):
        key = (name, size)
        if key in self.fonts:
            return self.fonts[key]
            
        font_path = os.path.join(self.base_path, "UI", "Font", f"{name}.ttf")
        if os.path.exists(font_path):
            font = pygame.font.Font(font_path, size)
        else:
            font = pygame.font.SysFont("Consolas", size)
            
        self.fonts[key] = font
        return font
        
    def load_all(self):
        for layer in range(1, 5):
            self.backgrounds[layer] = self.load_background(layer)
        self.backgrounds[5] = self.load_background(1)
        
    def get_background(self, layer):
        return self.backgrounds.get(layer)
        
    def get_player(self, direction="right"):
        return self.load_player_sprite(direction)
