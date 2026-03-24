from __future__ import annotations

from typing import Tuple

import pygame
from utils.constants import COLOUR_PALETTE
import os

Color = Tuple[int, int, int]

class UI:
    def __init__(self) -> None:
        from utils.assets import AssetLoader
        self.assets = AssetLoader()
        self.font_large: pygame.font.Font = self.assets.load_font("Kenney Future", 48)
        self.font_medium: pygame.font.Font = self.assets.load_font("Kenney Future", 28)
        self.font_small: pygame.font.Font = self.assets.load_font("Kenney Future", 18)
        self.current_layer: int = 1
        self.layer_names: dict[int, str] = {
            1: "THE CORRIDOR",
            2: "THE SEAMS",
            3: "THE STATIC",
            4: "THE VOID",
            5: "OUTSIDE"
        }
        
        # Load UI buttons from Kenny's pack
        self.ui_buttons = self.load_ui_buttons()
        
    def load_ui_buttons(self):
        buttons = {}
        ui_path = os.path.join(self.assets.base_path, "UI")
        
        # Try to load different button states
        button_types = ["button_normal", "button_hover", "button_pressed"]
        
        for button_type in button_types:
            button_path = os.path.join(ui_path, f"{button_type}.png")
            if os.path.exists(button_path):
                try:
                    img = pygame.image.load(button_path)
                    buttons[button_type] = img
                except pygame.error:
                    buttons[button_type] = None
            else:
                buttons[button_type] = None
                
        return buttons
        
    def draw_button(self, surface, text, rect, hover=False, pressed=False):
        # Determine which button image to use
        if pressed and "button_pressed" in self.ui_buttons and self.ui_buttons["button_pressed"]:
            button_img = pygame.transform.scale(self.ui_buttons["button_pressed"], rect.size)
        elif hover and "button_hover" in self.ui_buttons and self.ui_buttons["button_hover"]:
            button_img = pygame.transform.scale(self.ui_buttons["button_hover"], rect.size)
        elif "button_normal" in self.ui_buttons and self.ui_buttons["button_normal"]:
            button_img = pygame.transform.scale(self.ui_buttons["button_normal"], rect.size)
        else:
            # Fallback: draw procedural button
            color = (80, 80, 90) if hover else (60, 60, 70)
            pygame.draw.rect(surface, color, rect)
            pygame.draw.rect(surface, (100, 120, 140), rect, 2)
            button_img = None
            
        if button_img:
            surface.blit(button_img, rect)
            
        # Draw text on button
        text_surface = self.font_medium.render(text, True, (200, 200, 210))
        text_rect = text_surface.get_rect(center=rect.center)
        surface.blit(text_surface, text_rect)
        
    def set_layer(self, layer: int) -> None:
        self.current_layer = layer
        
    def draw_layer_indicator(self, surface: pygame.Surface) -> None:
        if self.current_layer in self.layer_names:
            text = self.layer_names[self.current_layer]
            text_surface = self.font_large.render(text, True, (200, 200, 210))
            surface.blit(text_surface, (50, 50))
            
    def draw_title(self, surface: pygame.Surface, title: str) -> None:
        text_surface = self.font_large.render(title, True, (200, 200, 210))
        surface.blit(text_surface, ((surface.get_width() - text_surface.get_width()) // 2, 100))
        
    def draw_controls(self, surface: pygame.Surface) -> None:
        controls = [
            "ARROW KEYS / WASD - Move",
            "SPACE - Interact",
            "ESC - Menu"
        ]
        
        y_offset = surface.get_height() - 100
        for control in controls:
            text_surface = self.font_small.render(control, True, (80, 80, 90))
            surface.blit(text_surface, (50, y_offset))
            y_offset += 25
            
    def draw_interaction_prompt(self, surface: pygame.Surface, position: Tuple[int, int], text: str = "[SPACE] Interact") -> None:
        prompt = self.font_small.render("Press SPACE", True, (150, 150, 160))
        surface.blit(prompt, position)
        
    def draw_vignette(self, surface: pygame.Surface, intensity: float = 0.3) -> None:
        vignette = pygame.Surface((surface.get_width(), surface.get_height()))
        vignette.set_alpha(100)
        vignette.fill((0, 0, 0))
        
        # Create vignette effect
        center_x = surface.get_width() // 2
        center_y = surface.get_height() // 2
        max_radius = int((surface.get_width() ** 2 + surface.get_height() ** 2) ** 0.5)
        
        for radius in range(max_radius, 0, -10):
            alpha = int(100 * (1 - radius / max_radius))
            color = (0, 0, 0, alpha)
            pygame.draw.circle(vignette, color, (center_x, center_y), radius)
            
        vignette = pygame.Surface(surface.get_size())
        vignette.set_alpha(int(255 * intensity))
        for i in range(100):
            pygame.draw.rect(vignette, (0, 0, 0), (i * 8, 0, 8, surface.get_height()))
        surface.blit(vignette, (0, 0))
