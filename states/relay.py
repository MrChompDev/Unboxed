import pygame
import random
from entities.player import Player
from systems.ui import UI
from systems.narrator import Narrator


class RelayState:
    def __init__(self, game):
        self.game = game
        self.player = Player(120, 900, perspective="side")
        self.ui = UI()
        self.narrator = Narrator()
        self.platforms = []
        self.interactables = []
        self.layer = 4
        self.perspective = "side"
        self.flicker_timer = 0
        self.background = self.game.assets.get_background(4)
        self.player_sprite = self.game.assets.get_player("right")
        self.setup_level()

    def setup_level(self):
        self.platforms = [
            pygame.Rect(0, 960, 1920, 120),
            pygame.Rect(120, 810, 240, 40),
            pygame.Rect(420, 690, 240, 40),
            pygame.Rect(720, 570, 240, 40),
            pygame.Rect(1020, 450, 240, 40),
            pygame.Rect(1320, 330, 240, 40),
            pygame.Rect(1620, 210, 240, 40),
            pygame.Rect(240, 510, 180, 30),
            pygame.Rect(540, 390, 180, 30),
            pygame.Rect(840, 270, 180, 30),
            pygame.Rect(1140, 150, 180, 30),
            pygame.Rect(300, 900, 120, 20),
            pygame.Rect(600, 780, 120, 20),
            pygame.Rect(900, 660, 120, 20),
            pygame.Rect(1200, 540, 120, 20),
            pygame.Rect(1500, 420, 120, 20),
        ]
        self.interactables = [
            {
                "rect": pygame.Rect(1740, 150, 80, 80),
                "triggered": False,
                "next": "uplink",
                "message": "Signal stabilized. Uplink ahead.",
            }
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
                    self.game.trigger_transition(4, 5, "fade")

    def update(self):
        self.narrator.update()
        self.player.update(self.platforms)
        self.flicker_timer = (self.flicker_timer + 1) % 60

    def draw(self, surface):
        colors = self.game.get_layer_colors(4)

        if self.background:
            surface.blit(self.background, (0, 0))
        else:
            surface.fill(colors["bg"])

        if self.flicker_timer < 30:
            for _ in range(60):
                x = random.randint(0, surface.get_width() - 1)
                y = random.randint(0, surface.get_height() - 1)
                surface.set_at((x, y), (80, 90, 110))

        for platform in self.platforms:
            pygame.draw.rect(surface, colors["fg"], platform)
            pygame.draw.rect(surface, colors["accent"], platform, 2)

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
