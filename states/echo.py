import pygame
import random
from entities.player import Player
from systems.ui import UI
from systems.narrator import Narrator


class EchoState:
    def __init__(self, game):
        self.game = game
        self.player = Player(140, 900, perspective="side")
        self.ui = UI()
        self.narrator = Narrator()
        self.platforms = []
        self.interactables = []
        self.layer = 4
        self.perspective = "side"
        self.echo_particles = []
        self.background = self.game.assets.get_background(4)
        self.player_sprite = self.game.assets.get_player("right")
        self.setup_level()

    def setup_level(self):
        self.platforms = [
            pygame.Rect(0, 960, 1920, 120),
            pygame.Rect(120, 780, 220, 40),
            pygame.Rect(420, 660, 220, 40),
            pygame.Rect(720, 540, 220, 40),
            pygame.Rect(1020, 420, 220, 40),
            pygame.Rect(1320, 300, 220, 40),
            pygame.Rect(1620, 180, 220, 40),
            pygame.Rect(300, 900, 140, 20),
            pygame.Rect(540, 780, 140, 20),
            pygame.Rect(780, 660, 140, 20),
            pygame.Rect(1020, 540, 140, 20),
            pygame.Rect(1260, 420, 140, 20),
            pygame.Rect(1500, 300, 140, 20),
        ]
        self.interactables = [
            {"rect": pygame.Rect(1740, 120, 80, 80), "triggered": False, "next": "relay", "message": "The echo fades. Move on."}
        ]
        self.echo_particles = [(random.randint(0, 1920), random.randint(0, 1080)) for _ in range(80)]

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
                    self.game.trigger_transition(4, 4, "fade")

    def update(self):
        self.narrator.update()
        self.player.update(self.platforms)

        for i, (px, py) in enumerate(self.echo_particles):
            self.echo_particles[i] = ((px + random.randint(-2, 2)) % 1920, (py + random.randint(-2, 2)) % 1080)

    def draw(self, surface):
        colors = self.game.get_layer_colors(4)

        if self.background:
            surface.blit(self.background, (0, 0))
        else:
            surface.fill(colors["bg"])

        for px, py in self.echo_particles:
            pygame.draw.circle(surface, (120, 140, 170), (px, py), 2)

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
