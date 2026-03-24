import pygame
from entities.player import Player
from systems.ui import UI
from systems.narrator import Narrator

class OutsideState:
    def __init__(self, game):
        self.game = game
        self.player = Player(960, 900, perspective="side")
        self.ui = UI()
        self.narrator = Narrator()
        self.platforms = []
        self.interactables = []
        self.layer = 5
        self.perspective = "side"
        self.end_sequence_timer = 0
        self.has_won = False
        self.show_credits = False
        self.background = self.game.assets.get_background(5)
        self.player_sprite = self.game.assets.get_player("right")
        self.setup_level()
        
    def setup_level(self):
        self.platforms = [
            pygame.Rect(0, 990, 1920, 90),  # Ground
            pygame.Rect(240, 810, 240, 40),  # Hills
            pygame.Rect(720, 810, 240, 40),
            pygame.Rect(1200, 810, 240, 40),
            pygame.Rect(1560, 810, 240, 40),
            pygame.Rect(480, 630, 360, 40),  # Platforms
            pygame.Rect(1080, 630, 360, 40),
            pygame.Rect(240, 450, 480, 40),
            pygame.Rect(1320, 450, 480, 40),
            pygame.Rect(600, 270, 720, 40),
            pygame.Rect(0, 720, 180, 40),  # Left side platforms
            pygame.Rect(1680, 720, 240, 40),  # Right side platforms
        ]
        self.interactables = [
            {"rect": pygame.Rect(240, 180, 80, 80), "triggered": False, "next": "menu", "message": "A memory of the beginning... I remember the sun. Real sun."},
            {"rect": pygame.Rect(1560, 180, 80, 80), "triggered": False, "next": "menu", "message": "The code that started it all. 'If anyone finds this, know that we tried to escape.'"},
            {"rect": pygame.Rect(960, 180, 40, 40), "triggered": False, "next": "menu", "message": "TRANSMISSION: 'Subject 734 made it. The others are still trapped. Save them.'"},
        ]
        
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.change_state("menu")
                
    def update(self):
        self.narrator.update()
        self.player.update(self.platforms)
        self.end_sequence_timer += 1
        
        if self.end_sequence_timer == 1:
            self.narrator.say("I escaped the box. I escaped the rules.")
        elif self.end_sequence_timer == 180:
            self.narrator.say("But now... what?")
        elif self.end_sequence_timer == 360:
            self.narrator.say("The game continues. I just chose to play differently.")
        elif self.end_sequence_timer == 540:
            self.has_won = True
            self.narrator.say("Thank you for playing GLITCH.")
            self.show_credits = True
            
    def draw(self, surface):
        colors = self.game.get_layer_colors(5)
        
        if self.background:
            surface.blit(self.background, (0, 0))
        else:
            surface.fill(colors["bg"])
        
        # Draw clouds
        cloud_color = (220, 220, 230)
        pygame.draw.ellipse(surface, cloud_color, (200, 100, 120, 60))
        pygame.draw.ellipse(surface, cloud_color, (600, 150, 140, 70))
        pygame.draw.ellipse(surface, cloud_color, (1000, 80, 160, 80))
        pygame.draw.ellipse(surface, cloud_color, (1400, 120, 130, 65))
        
        # Draw sun
        sun_color = (255, 220, 100)
        pygame.draw.circle(surface, sun_color, (1700, 150), 40)
        
        # Draw platforms with grass-like colors
        grass_color = (50, 150, 50)
        platform_color = (139, 90, 43)
        
        for platform in self.platforms:
            # Draw grass on top
            pygame.draw.rect(surface, grass_color, (platform.x, platform.y, platform.width, 10))
            # Draw dirt/earth below
            pygame.draw.rect(surface, platform_color, (platform.x, platform.y + 10, platform.width, platform.height - 10))
            pygame.draw.rect(surface, colors["accent"], (platform.x, platform.y, platform.width, platform.height), 2)
            
        # Draw trees
        tree_positions = [(150, 750), (350, 750), (550, 750), (750, 750), (950, 750), (1150, 750), (1350, 750), (1550, 750)]
        for tx, ty in tree_positions:
            # Tree trunk
            pygame.draw.rect(surface, (101, 67, 33), (tx - 10, ty, 20, 60))
            # Tree leaves
            pygame.draw.circle(surface, (34, 139, 34), (tx, ty - 20), 30)
            pygame.draw.circle(surface, (34, 139, 34), (tx - 15, ty - 10), 25)
            pygame.draw.circle(surface, (34, 139, 34), (tx + 15, ty - 10), 25)
            
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
        
        if self.has_won:
            self.ui.draw_title(surface, "THE END")
            hint = self.ui.font_small.render("Press ESC to return to menu", True, (80, 80, 90))
            surface.blit(hint, ((surface.get_width() - hint.get_width()) // 2, 500))

        if self.show_credits:
            credits = [
                "Programming - MrChomp",
                "Music - MrChomp",
                "Assets - Kenny",
            ]
            y_offset = 180
            for line in credits:
                text = self.ui.font_medium.render(line, True, (0, 0, 0))
                surface.blit(text, ((surface.get_width() - text.get_width()) // 2, y_offset))
                y_offset += 50
