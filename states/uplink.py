import pygame
import random
from entities.player import Player
from systems.ui import UI
from systems.narrator import Narrator


class UplinkState:
    def __init__(self, game):
        self.game = game
        self.player = Player(160, 900, perspective="side")
        self.ui = UI()
        self.narrator = Narrator()
        self.platforms = []
        self.interactables = []
        self.layer = 5
        self.perspective = "side"
        self.spark_timer = 0
        self.background = self.game.assets.get_background(2)
        self.player_sprite = self.game.assets.get_player("right")
        self.setup_level()

    def setup_level(self):
        self.platforms = [
            pygame.Rect(0, 960, 1920, 120),
            pygame.Rect(180, 840, 200, 40),
            pygame.Rect(420, 720, 200, 40),
            pygame.Rect(660, 600, 200, 40),
            pygame.Rect(900, 480, 200, 40),
            pygame.Rect(1140, 360, 200, 40),
            pygame.Rect(1380, 240, 200, 40),
            pygame.Rect(1620, 120, 200, 40),
            pygame.Rect(300, 900, 140, 20),
            pygame.Rect(540, 780, 140, 20),
            pygame.Rect(780, 660, 140, 20),
            pygame.Rect(1020, 540, 140, 20),
            pygame.Rect(1260, 420, 140, 20),
            pygame.Rect(1500, 300, 140, 20),
        ]
        self.interactables = [
            {"rect": pygame.Rect(1700, 60, 80, 80), "triggered": False, "next": "outside", "message": "Uplink complete. Step outside."}
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
                    self.game.trigger_transition(5, 5, "fade")

    def update(self):
        self.narrator.update()
        self.player.update(self.platforms)
        self.spark_timer = (self.spark_timer + 1) % 40

    def draw(self, surface):
        colors = self.game.get_layer_colors(2)

        if self.background:
            surface.blit(self.background, (0, 0))
        else:
            surface.fill(colors["bg"])

        if self.spark_timer < 20:
            for _ in range(40):
                x = random.randint(0, surface.get_width() - 1)
                y = random.randint(0, surface.get_height() - 1)
                surface.set_at((x, y), (120, 200, 220))

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
