import pygame
from systems.ui import UI

class MenuState:
    def __init__(self, game):
        self.game = game
        self.ui = UI()
        self.options = ["START GAME", "SETTINGS", "CONTROLS", "EXIT"]
        self.selected = 0
        self.show_controls = False
        self.background = self.game.assets.get_background(1)
        
    def handle_event(self, event):
        if self.show_controls:
            if event.type == pygame.KEYDOWN:
                self.show_controls = False
            return
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                mouse_pos = pygame.mouse.get_pos()
                
                # Calculate button positions
                button_width = 300
                button_height = 50
                button_spacing = 70
                start_y = 300
                
                for i, option in enumerate(self.options):
                    button_rect = pygame.Rect(
                        (self.game.screen.get_width() - button_width) // 2,
                        start_y + i * button_spacing,
                        button_width,
                        button_height
                    )
                    
                    if button_rect.collidepoint(mouse_pos):
                        if i == 0:
                            self.game.change_state("data_stream")
                        elif i == 1:
                            self.game.change_state("settings")
                        elif i == 2:
                            self.show_controls = True
                        elif i == 3:
                            self.game.running = False
                        return
                        
        if event.type != pygame.KEYDOWN:
            return
            
        if event.key == pygame.K_UP or event.key == pygame.K_w:
            self.selected = (self.selected - 1) % len(self.options)
        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
            self.selected = (self.selected + 1) % len(self.options)
        elif event.key == pygame.K_RETURN:
            if self.selected == 0:
                self.game.change_state("data_stream")
            elif self.selected == 1:
                self.game.change_state("settings")
            elif self.selected == 2:
                self.show_controls = True
            elif self.selected == 3:
                self.game.running = False
                
    def update(self):
        pass
        
    def draw(self, surface):
        if self.background:
            surface.blit(self.background, (0, 0))
        else:
            surface.fill((15, 15, 20))
        
        title = self.ui.font_large.render("UNBOXED", True, (200, 200, 210))
        surface.blit(title, ((surface.get_width() - title.get_width()) // 2, 100))
        
        if not self.show_controls:
            # Calculate button positions
            button_width = 300
            button_height = 50
            button_spacing = 70
            start_y = 300
            
            mouse_pos = pygame.mouse.get_pos()
            
            for i, option in enumerate(self.options):
                button_rect = pygame.Rect(
                    (surface.get_width() - button_width) // 2,
                    start_y + i * button_spacing,
                    button_width,
                    button_height
                )
                
                # Check if mouse is hovering over button
                hover = button_rect.collidepoint(mouse_pos)
                
                # Draw button using UI system
                self.ui.draw_button(surface, option, button_rect, hover=hover)
        else:
            # Draw controls overlay
            overlay = pygame.Surface((surface.get_width(), surface.get_height()))
            overlay.set_alpha(200)
            overlay.fill((15, 15, 20))
            surface.blit(overlay, (0, 0))
            
            controls_title = self.ui.font_large.render("CONTROLS", True, (200, 200, 210))
            surface.blit(controls_title, ((surface.get_width() - controls_title.get_width()) // 2, 150))
            
            controls = [
                "ARROW KEYS / WASD - Move",
                "SPACE - Interact",
                "ESC - Menu",
                "",
                "Find the secrets to uncover the truth",
                "Explore all layers to escape the simulation",
                "",
                "Press any key to return"
            ]
            
            y_offset = 250
            for control in controls:
                text_surface = self.ui.font_medium.render(control, True, (180, 180, 190))
                surface.blit(text_surface, ((surface.get_width() - text_surface.get_width()) // 2, y_offset))
                y_offset += 40
