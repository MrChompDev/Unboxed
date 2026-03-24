from __future__ import annotations

from typing import Protocol, runtime_checkable, Any

import pygame
import sys
from utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, COLOUR_PALETTE
from systems.transition import Transition
from systems.glitch import GlitchSystem
from systems.ui import UI
from systems.cutscenes import IntroCutscene, MidGameCutscene, EndingCutscene
from systems.credits import CreditsCutscene
from systems.music import MusicSystem
from utils.assets import AssetLoader


@runtime_checkable
class GameState(Protocol):
    def handle_event(self, event: pygame.event.Event) -> None: ...
    def update(self) -> None: ...
    def draw(self, surface: pygame.Surface) -> None: ...


@runtime_checkable
class InteractableState(Protocol):
    interactables: list[dict[str, Any]]

class Game:
    def __init__(self) -> None:
        pygame.init()
        self.screen: pygame.Surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("UNBOXED")
        self.clock: pygame.time.Clock = pygame.time.Clock()
        self.running: bool = True
        
        self.transition: Transition = Transition()
        self.glitch: GlitchSystem = GlitchSystem()
        self.ui: UI = UI()
        self.assets: AssetLoader = AssetLoader()
        
        # Music system
        self.music = MusicSystem()
        
        # Cutscene system
        self.intro_cutscene = IntroCutscene(self)
        self.midgame_cutscene = MidGameCutscene(self)
        self.ending_cutscene = EndingCutscene(self)
        self.credits_cutscene = CreditsCutscene(self)
        self.active_cutscene = None
        self.cutscene_triggered = {"intro": False, "mid": False, "ending": False, "credits": False}
        
        self.current_state: GameState | None = None
        self.states: dict[str, GameState] = {}
        self.pending_transition: tuple[int, int, str] | None = None
        
        self.load_states()
        
        # Start with menu music and intro cutscene
        self.music.play_menu_music()
        self.intro_cutscene.start()  # Start with intro cutscene
        
    def load_states(self) -> None:
        from states.menu import MenuState
        from states.settings import SettingsState
        from states.data_stream import DataStreamState
        from states.static import StaticState
        from states.echo import EchoState
        from states.relay import RelayState
        from states.uplink import UplinkState
        from states.outside import OutsideState
        
        self.states = {
            "menu": MenuState(self),
            "settings": SettingsState(self),
            "data_stream": DataStreamState(self),
            "static": StaticState(self),
            "echo": EchoState(self),
            "relay": RelayState(self),
            "uplink": UplinkState(self),
            "outside": OutsideState(self),
        }
        self.current_state = self.states["menu"]
        
    def change_state(self, state_name: str) -> None:
        if state_name in self.states:
            self.current_state = self.states[state_name]
            
            # Switch music based on state
            if state_name in ["menu", "level_select", "settings"]:
                self.music.play_menu_music()
            elif state_name in ["data_stream", "static", "echo", "relay", "uplink", "outside"]:
                self.music.play_level_music()
            
    def trigger_cutscene(self, cutscene_type):
        if cutscene_type == "intro" and not self.cutscene_triggered["intro"]:
            self.active_cutscene = self.intro_cutscene
            self.cutscene_triggered["intro"] = True
            self.music.play_menu_music()  # Menu music for cutscenes
        elif cutscene_type == "mid" and not self.cutscene_triggered["mid"]:
            self.active_cutscene = self.midgame_cutscene
            self.cutscene_triggered["mid"] = True
            self.music.play_menu_music()  # Menu music for cutscenes
        elif cutscene_type == "ending" and not self.cutscene_triggered["ending"]:
            self.active_cutscene = self.ending_cutscene
            self.cutscene_triggered["ending"] = True
            self.music.play_menu_music()  # Menu music for cutscenes
        elif cutscene_type == "credits" and not self.cutscene_triggered["credits"]:
            self.active_cutscene = self.credits_cutscene
            self.cutscene_triggered["credits"] = True
            self.music.play_menu_music()  # Menu music for credits
            
    def update_cutscenes(self):
        if self.active_cutscene:
            finished = self.active_cutscene.update()
            if finished:
                self.active_cutscene = None
                
                # Handle post-cutscene logic
                if self.cutscene_triggered["intro"] and self.current_state is None:
                    self.current_state = self.states["menu"]  # Start game after intro
                    self.music.play_menu_music()
                elif self.cutscene_triggered["ending"] and not self.cutscene_triggered["credits"]:
                    # Trigger credits after ending
                    self.trigger_cutscene("credits")
                elif self.cutscene_triggered["credits"]:
                    # Return to menu after credits
                    self.change_state("menu")
                    self.music.play_menu_music()
                    
    def draw_cutscenes(self, surface):
        if self.active_cutscene:
            self.active_cutscene.draw(surface)
            
    def trigger_transition(self, from_layer: int, to_layer: int, mode: str = "fade") -> None:
        self.pending_transition = (from_layer, to_layer, mode)
        
    def get_layer_colors(self, layer: int) -> dict[str, tuple[int, int, int]]:
        return COLOUR_PALETTE.get(f"layer{layer}", COLOUR_PALETTE["layer1"])
        
    def handle_events(self) -> None:
        if self.current_state is None:
            return
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F4:
                    self.running = False
            self.current_state.handle_event(event)
            
    def update(self) -> None:
        # Update music fades
        self.music.update_fade()
        
        # Update cutscenes first
        self.update_cutscenes()
        
        # Only update game state if no cutscene is active
        if not self.active_cutscene and self.current_state:
            if self.pending_transition:
                from_layer, to_layer, mode = self.pending_transition
                self.transition.start(from_layer, to_layer, mode)
                self.pending_transition = None
                
            self.transition.update()
            self.glitch.update()
            self.current_state.update()
            
            if self.transition.is_complete() and self.pending_transition is None:
                if isinstance(self.current_state, InteractableState):
                    for obj in self.current_state.interactables:
                        if obj.get("triggered") and "next" in obj:
                            next_state = obj["next"]
                            if next_state in self.states:
                                self.change_state(next_state)
                                break
                            
    def draw(self) -> None:
        surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # Draw cutscene if active, otherwise draw game state
        if self.active_cutscene:
            self.active_cutscene.draw(surface)
        elif self.current_state:
            self.current_state.draw(surface)
            surface = self.transition.apply(surface)
            surface = self.glitch.apply(surface)
        
        self.screen.blit(surface, (0, 0))
        pygame.display.flip()
        
    def run(self) -> None:
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
            
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
