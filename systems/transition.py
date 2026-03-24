from __future__ import annotations

import time

import pygame
from utils.constants import LAYER_TRANSITION_DURATION

class Transition:
    def __init__(self) -> None:
        self.active: bool = False
        self.progress: float = 0.0
        self.from_layer: int = 1
        self.to_layer: int = 1
        self.start_time: float = 0.0
        self.mode: str = "fade"
        self.squish_factor: float = 1.0
        
    def start(self, from_layer: int, to_layer: int, mode: str = "fade") -> None:
        self.active = True
        self.from_layer = from_layer
        self.to_layer = to_layer
        self.start_time = time.time()
        self.mode = mode
        self.progress = 0
        self.squish_factor = 1.0
        
    def update(self) -> None:
        if self.active:
            elapsed = time.time() - self.start_time
            self.progress = min(1.0, elapsed / LAYER_TRANSITION_DURATION)
            
            if self.mode == "perspective_flip":
                if self.progress < 0.5:
                    self.squish_factor = 1.0 - (self.progress * 2)
                else:
                    self.squish_factor = (self.progress - 0.5) * 2
                    
            if self.progress >= 1.0:
                self.active = False
                
    def apply(self, surface: pygame.Surface) -> pygame.Surface:
        if not self.active:
            return surface
            
        if self.mode == "fade":
            alpha = int(255 * abs(0.5 - self.progress) * 2)
            fade_surface = pygame.Surface(surface.get_size())
            fade_surface.set_alpha(alpha)
            result = surface.copy()
            result.blit(fade_surface, (0, 0))
            return result
            
        elif self.mode == "perspective_flip":
            width, height = surface.get_size()
            if self.progress < 0.5:
                scale_factor = 1.0 - (self.progress * 2)
                new_height = max(1, int(height * scale_factor))
                scaled = pygame.transform.scale(surface, (width, new_height))
                result = pygame.transform.scale(scaled, (width, height))
            else:
                scale_factor = (self.progress - 0.5) * 2
                new_height = max(1, int(height * scale_factor))
                scaled = pygame.transform.scale(surface, (width, new_height))
                result = pygame.transform.scale(scaled, (width, height))
            return result
            
        elif self.mode == "glitch":
            if self.progress < 0.3:
                return surface
            elif self.progress < 0.7:
                return surface
            else:
                return surface
                
        return surface
        
    def is_complete(self) -> bool:
        return not self.active
        
    def get_mode(self) -> str:
        return self.mode
