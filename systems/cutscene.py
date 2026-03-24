import pygame
import time
from utils.assets import AssetLoader

class Cutscene:
    def __init__(self, game, scenes):
        self.game = game
        self.scenes = scenes
        self.current_scene = 0
        self.timer = 0
        self.active = False
        self.assets = AssetLoader()
        self.skippable = False  # Papa Games style - no skipping during first playthrough
        
    def start(self, skippable=False):
        self.active = True
        self.current_scene = 0
        self.timer = time.time()
        self.skippable = skippable
        
    def update(self):
        if not self.active:
            return
            
        # Handle input for skippable cutscenes
        if self.skippable:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE] or keys[pygame.K_RETURN] or keys[pygame.K_ESCAPE]:
                self.active = False
                return True  # Cutscene finished
                
        current_time = time.time()
        elapsed = current_time - self.timer
        
        if elapsed > self.scenes[self.current_scene]["duration"]:
            self.current_scene += 1
            self.timer = current_time
            
            if self.current_scene >= len(self.scenes):
                self.active = False
                return True  # Cutscene finished
                
        return False
        
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
            
        # Draw scene elements
        self.draw_scene_elements(surface, scene)
        
        # Draw text
        if "text" in scene:
            self.draw_text(surface, scene["text"])
            
        # Draw skip hint for skippable cutscenes
        if self.skippable:
            self.draw_skip_hint(surface)
            
    def draw_skip_hint(self, surface):
        font = self.assets.load_font("Kenney Future", 18)
        hint_text = "Press SPACE to skip"
        text_surface = font.render(hint_text, True, (150, 150, 160))
        surface.blit(text_surface, (surface.get_width() - text_surface.get_width() - 20, surface.get_height() - 30))
            
    def draw_scene_elements(self, surface, scene):
        # Draw pod/box
        if scene.get("show_pod", False):
            # Pod exterior
            pygame.draw.rect(surface, (50, 50, 60), (400, 200, 1120, 680))
            pygame.draw.rect(surface, (30, 30, 40), (400, 200, 1120, 680), 4)
            
            # Glass viewport
            pygame.draw.rect(surface, (100, 120, 140), (500, 300, 920, 480))
            pygame.draw.rect(surface, (150, 170, 190), (500, 300, 920, 480), 2)
            
            # Reflection on glass
            for i in range(5):
                alpha = 50 - i * 10
                reflection = pygame.Surface((920, 480))
                reflection.set_alpha(alpha)
                reflection.fill((200, 200, 255))
                surface.blit(reflection, (500 + i * 2, 300 + i * 2))
                
        # Draw character inside pod
        if scene.get("show_character", False):
            # Character silhouette
            pygame.draw.ellipse(surface, (30, 150, 255), (860, 500, 200, 280))
            pygame.draw.circle(surface, (30, 150, 255), (960, 450), 60)
            
            # Wires/tubes connected to character
            pygame.draw.line(surface, (100, 100, 120), (960, 450), (800, 300), 3)
            pygame.draw.line(surface, (100, 100, 120), (960, 450), (1120, 300), 3)
            pygame.draw.line(surface, (100, 100, 120), (960, 550), (900, 700), 3)
            pygame.draw.line(surface, (100, 100, 120), (960, 550), (1020, 700), 3)
            
        # Draw outside world
        if scene.get("show_outside", False):
            # Sky
            pygame.draw.rect(surface, (135, 206, 235), (500, 300, 920, 240))
            
            # Sun
            pygame.draw.circle(surface, (255, 220, 100), (1300, 400), 40)
            
            # Clouds
            pygame.draw.ellipse(surface, (255, 255, 255), (600, 350, 120, 60))
            pygame.draw.ellipse(surface, (255, 255, 255), (1000, 380, 140, 70))
            
            # Ground/grass
            pygame.draw.rect(surface, (50, 150, 50), (500, 540, 920, 240))
            
            # Trees in distance
            for x in range(550, 1400, 100):
                pygame.draw.rect(surface, (101, 67, 33), (x - 5, 500, 10, 40))
                pygame.draw.circle(surface, (34, 139, 34), (x, 490), 15)
                
        # Draw lab environment
        if scene.get("show_lab", False):
            # Lab walls
            pygame.draw.rect(surface, (40, 40, 50), (300, 100, 1320, 880))
            
            # Computer monitors
            for x in range(350, 1600, 200):
                pygame.draw.rect(surface, (20, 20, 30), (x, 150, 150, 100))
                pygame.draw.rect(surface, (100, 200, 100), (x + 10, 160, 130, 80))
                
            # Data streams on monitors
            for x in range(350, 1600, 200):
                for y in range(170, 230, 10):
                    if pygame.time.get_ticks() % 100 < 50:
                        pygame.draw.line(surface, (0, 255, 0), (x + 20, y), (x + 130, y), 1)
                        
    def draw_text(self, surface, text_data):
        font = self.assets.load_font("Kenney Future", 32)
        
        if isinstance(text_data, str):
            text = text_data
            color = (200, 200, 210)
        else:
            text = text_data.get("text", "")
            color = text_data.get("color", (200, 200, 210))
            
        # Draw text background
        text_surface = font.render(text, True, color)
        padding = 20
        bg_rect = pygame.Rect(
            (surface.get_width() - text_surface.get_width()) // 2 - padding,
            surface.get_height() - 150,
            text_surface.get_width() + padding * 2,
            text_surface.get_height() + padding
        )
        pygame.draw.rect(surface, (20, 20, 30), bg_rect)
        pygame.draw.rect(surface, (100, 120, 140), bg_rect, 2)
        
        # Draw text
        surface.blit(text_surface, (bg_rect.x + padding, bg_rect.y + padding // 2))
        
    def is_active(self):
        return self.active
