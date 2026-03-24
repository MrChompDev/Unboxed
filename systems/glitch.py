from __future__ import annotations

import random
from typing import Optional

import pygame
from utils.effects import apply_glitch, apply_noise, chromatic_aberration

class GlitchSystem:
    def __init__(self) -> None:
        self.intensity: float = 0.0
        self.target_intensity: float = 0.0
        self.active: bool = False
        self.duration: float = 0.0
        self.timer: int = 0
        self.triggered_by: Optional[str] = None
        
    def trigger(self, intensity: int = 5, duration: float = 1.0, triggered_by: Optional[str] = None) -> None:
        self.target_intensity = float(intensity)
        self.duration = float(duration)
        self.timer = pygame.time.get_ticks()
        self.active = True
        self.triggered_by = triggered_by
        
    def update(self) -> None:
        if self.active:
            elapsed = (pygame.time.get_ticks() - self.timer) / 1000
            if elapsed < self.duration:
                progress = elapsed / self.duration
                self.intensity = self.target_intensity * (1 - progress)
            else:
                self.active = False
                self.intensity = 0
                
    def apply(self, surface: pygame.Surface) -> pygame.Surface:
        if self.active and self.intensity > 0:
            if random.random() < 0.3:
                surface = apply_glitch(surface, int(self.intensity))
            if random.random() < 0.2:
                surface = apply_noise(surface, int(self.intensity * 2))
            if random.random() < 0.1:
                surface = chromatic_aberration(surface, int(self.intensity))
            return surface
        return surface
        
    def set_trigger(self, trigger_name: str) -> None:
        self.triggered_by = trigger_name
        
    def is_active(self) -> bool:
        return self.active
