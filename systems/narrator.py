from __future__ import annotations

import time

import pygame

class Narrator:
    def __init__(self, font_size: int = 24) -> None:
        from utils.assets import AssetLoader
        self.assets = AssetLoader()
        self.font: pygame.font.Font = self.assets.load_font("Kenney Future", font_size)
        self.messages: list[str] = []
        self.current_message: str = ""
        self.char_index: int = 0
        self.timer: float = 0.0
        self.visible: bool = False
        self.speed: float = 0.05
        self.layer: int = 1
        
    def set_layer(self, layer: int) -> None:
        self.layer = layer
        
    def say(self, text: str) -> None:
        self.messages.append(text)
        self.current_message = text
        self.char_index = 0
        self.visible = True
        self.timer = time.time()
        
    def update(self) -> None:
        if self.visible and self.char_index < len(self.current_message):
            if time.time() - self.timer > self.speed:
                self.char_index += 1
                self.timer = time.time()
                
    def draw(self, surface: pygame.Surface) -> None:
        if self.visible:
            display_text = self.current_message[:self.char_index]
            text_surf = self.font.render(display_text, True, (200, 200, 200))
            padding = 20
            bg_rect = pygame.Rect(padding - 10, surface.get_height() - 80, text_surf.get_width() + 20, 50)
            pygame.draw.rect(surface, (30, 30, 35), bg_rect)
            pygame.draw.rect(surface, (100, 120, 140), bg_rect, 2)
            surface.blit(text_surf, (padding, surface.get_height() - 70))
            
    def skip(self) -> None:
        if self.char_index < len(self.current_message):
            self.char_index = len(self.current_message)
        elif len(self.messages) > 1:
            self.messages.pop(0)
            self.current_message = self.messages[0]
            self.char_index = 0
        else:
            self.visible = False
            
    def is_done(self) -> bool:
        return self.char_index >= len(self.current_message)
