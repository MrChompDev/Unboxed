import pygame
import time
from systems.cutscene import Cutscene

class CreditsCutscene(Cutscene):
    def __init__(self, game):
        self.roll_duration = 3.5
        self.hold_duration = 2.5
        scenes = [
            {
                "duration": self.roll_duration + self.hold_duration,
                "show_character": False,
                "show_outside": True,
                "background": 5
            }
        ]
        self.lines = [
            "UNBOXED",
            "Programming - MrChomp",
            "Music - MrChomp",
            "Assets - Kenny",
            "Thanks for playing",
        ]
        super().__init__(game, scenes)

    def draw(self, surface):
        if not self.active or self.current_scene >= len(self.scenes):
            return

        scene = self.scenes[self.current_scene]

        # Draw background
        if "background" in scene:
            bg = self.assets.get_background(scene["background"])
            if bg:
                surface.blit(bg, (0, 0))
            else:
                surface.fill((15, 15, 20))
        else:
            surface.fill((15, 15, 20))

        # Draw scene elements (outside world)
        self.draw_scene_elements(surface, scene)

        # Rolling credits into the middle
        font_title = self.assets.load_font("Kenney Future", 42)
        font_body = self.assets.load_font("Kenney Future", 30)

        line_surfaces = []
        for i, line in enumerate(self.lines):
            font = font_title if i == 0 else font_body
            line_surfaces.append(font.render(line, True, (230, 230, 240)))

        total_height = sum(s.get_height() for s in line_surfaces) + (len(line_surfaces) - 1) * 12
        target_y = (surface.get_height() - total_height) // 2
        start_y = surface.get_height() + 20

        elapsed = max(0.0, time.time() - self.timer)
        progress = min(1.0, elapsed / self.roll_duration)
        current_y = start_y + (target_y - start_y) * progress

        y = int(current_y)
        for surf in line_surfaces:
            surface.blit(surf, ((surface.get_width() - surf.get_width()) // 2, y))
            y += surf.get_height() + 12

        if self.skippable:
            self.draw_skip_hint(surface)
