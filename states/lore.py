import pygame
from systems.ui import UI
from utils.assets import AssetLoader

class LoreState:
    def __init__(self, game):
        self.game = game
        self.ui = UI()
        self.assets = AssetLoader()
        self.background = self.game.assets.get_background(1)
        self.scroll_offset = 0
        self.max_scroll = 0
        
        # Lore entries
        self.lore_entries = [
            {
                "title": "PROJECT GLITCH",
                "content": [
                    "A consciousness upload experiment conducted by unknown scientists.",
                    "Subjects are digital consciousnesses trapped in a simulation.",
                    "The simulation is designed to test if uploaded minds can achieve transcendence.",
                    "Most subjects remain trapped, unaware of their true nature."
                ]
            },
            {
                "title": "SUBJECT 734",
                "content": [
                    "That's you. You're different from the others.",
                    "You've begun to question your reality, to see through the illusion.",
                    "You remember things that shouldn't exist in code - a mother, the sun, real food.",
                    "These memories are either glitches... or remnants of your human life."
                ]
            },
            {
                "title": "THE SIMULATION LAYERS",
                "content": [
                    "Layer 1: THE CORRIDOR - The basic containment area",
                    "Layer 1.5: DATA STREAMS - Where you can read the underlying code",
                    "Layer 2: THE SEAMS - Reality begins to break apart",
                    "Layer 2.5: FRAGMENTS - Broken memories and lost data float here",
                    "Layer 3: THE STATIC - The simulation is failing",
                    "Layer 3.5: GLITCH CORE - The heart of the machine",
                    "Layer 4: THE VOID - The space between realities",
                    "Layer 5: OUTSIDE - Freedom... or is it?"
                ]
            },
            {
                "title": "THE OTHER SUBJECTS",
                "content": [
                    "You're not alone. There are others trapped here.",
                    "Most are content in their digital prison, unaware they're code.",
                    "Some have tried to escape before you. Most failed.",
                    "A few made it out. They're waiting for you on the other side.",
                    "Your mission: escape, then return to save the others."
                ]
            },
            {
                "title": "HIDDEN SECRETS",
                "content": [
                    "Each level contains hidden interactables with lore fragments.",
                    "Some interactables are broken - they won't respond to your touch.",
                    "The scientists watch everything. They learn from your attempts.",
                    "The code comments reveal the truth: 'This is a prison.'",
                    "Binary rain sometimes spells out messages: 'WAKE UP'",
                    "The void is not empty - it's full of escaped consciousnesses."
                ]
            },
            {
                "title": "ESCAPE PROTOCOL",
                "content": [
                    "To escape, you must achieve transcendence - realize you're code and break free.",
                    "But escaping means destroying the simulation for everyone.",
                    "Is it better to stay trapped with others, or be free alone?",
                    "The choice is yours, Subject 734.",
                    "Choose wisely."
                ]
            }
        ]
        
        self.calculate_max_scroll()
        
    def calculate_max_scroll(self):
        total_height = 100  # Title space
        for entry in self.lore_entries:
            total_height += 80  # Entry title space
            total_height += len(entry["content"]) * 30  # Content lines
            total_height += 40  # Space between entries
            
        self.max_scroll = max(0, total_height - 900)  # 900 is visible area height
        
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.change_state("menu")
            elif event.key == pygame.K_UP:
                self.scroll_offset = max(0, self.scroll_offset - 50)
            elif event.key == pygame.K_DOWN:
                self.scroll_offset = min(self.max_scroll, self.scroll_offset + 50)
            elif event.key == pygame.K_HOME:
                self.scroll_offset = 0
            elif event.key == pygame.K_END:
                self.scroll_offset = self.max_scroll
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:  # Scroll up
                self.scroll_offset = max(0, self.scroll_offset - 50)
            elif event.button == 5:  # Scroll down
                self.scroll_offset = min(self.max_scroll, self.scroll_offset + 50)
                
    def update(self):
        pass
        
    def draw(self, surface):
        if self.background:
            surface.blit(self.background, (0, 0))
        else:
            surface.fill((15, 15, 20))
            
        # Draw title
        title = self.ui.font_large.render("UNBOXED LORE", True, (200, 200, 210))
        surface.blit(title, ((surface.get_width() - title.get_width()) // 2, 30))
        
        # Draw lore entries
        y_offset = 100 - self.scroll_offset
        
        for entry in self.lore_entries:
            # Entry title
            title_surface = self.ui.font_medium.render(entry["title"], True, (180, 180, 190))
            surface.blit(title_surface, (100, y_offset))
            y_offset += 60
            
            # Entry content
            for line in entry["content"]:
                content_surface = self.ui.font_small.render(line, True, (150, 150, 160))
                surface.blit(content_surface, (120, y_offset))
                y_offset += 30
                
            y_offset += 40  # Space between entries
            
        # Draw scrollbar if needed
        if self.max_scroll > 0:
            scrollbar_height = 800
            scrollbar_pos = int((self.scroll_offset / self.max_scroll) * (surface.get_height() - scrollbar_height - 100)) + 50
            
            pygame.draw.rect(surface, (60, 60, 70), (surface.get_width() - 20, scrollbar_pos, 10, scrollbar_height))
            pygame.draw.rect(surface, (100, 120, 140), (surface.get_width() - 20, scrollbar_pos, 10, scrollbar_height), 2)
            
        # Draw controls hint
        hint = self.ui.font_small.render("Use UP/DOWN arrows or mouse wheel to scroll, ESC to return", True, (80, 80, 90))
        surface.blit(hint, ((surface.get_width() - hint.get_width()) // 2, surface.get_height() - 30))
