import pygame
import os
import time
from utils.assets import AssetLoader

def _log_audio(message: str) -> None:
    try:
        with open("audio.log", "a", encoding="utf-8") as f:
            f.write(f"{time.strftime('%H:%M:%S')} | {message}\n")
    except Exception:
        pass

class MusicSystem:
    def __init__(self):
        self.assets = AssetLoader()
        self.current_music = None
        self.target_music = None
        self.music_volume = 0.5
        self.fade_volume = 0.5
        self.fading = False
        self.fade_direction = "out"  # "out" or "in"
        self.fade_speed = 0.05
        self.audio_ready = False
        try:
            pygame.mixer.init()
            self.audio_ready = True
        except Exception as e:
            _log_audio(f"mixer init failed: {e}")
        
    def load_music(self, music_name):
        if not self.audio_ready:
            _log_audio("load_music called but mixer not initialized")
            return False
        music_path = os.path.join(self.assets.base_path, "Music", f"{music_name}.mp3")
        if os.path.exists(music_path):
            try:
                pygame.mixer.music.load(music_path)
                return True
            except pygame.error as e:
                _log_audio(f"error loading {music_name}: {e}")
                return False
        _log_audio(f"music file not found: {music_path}")
        return False
        
    def play_level_music(self):
        """Play music during gameplay"""
        if not self.audio_ready:
            return
        # If already on level music and it's still playing, don't restart it.
        if self.current_music == "level" and self.is_playing():
            return
        if self.current_music != "level":
            if self.load_music("TheEscapistOST"):
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(self.music_volume)
                self.current_music = "level"
            else:
                self.current_music = "level"
        else:
            # Same track requested but not playing; restart it.
            if self.load_music("TheEscapistOST"):
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(self.music_volume)
            
    def play_menu_music(self):
        """Play music for menu, cutscenes, and credits"""
        if not self.audio_ready:
            return
        # If already on menu music and it's still playing, don't restart it.
        if self.current_music == "menu" and self.is_playing():
            return
        if self.current_music != "menu":
            if self.load_music("WorldOutsideOST"):
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(self.music_volume)
                self.current_music = "menu"
            else:
                self.current_music = "menu"
        else:
            # Same track requested but not playing; restart it.
            if self.load_music("WorldOutsideOST"):
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(self.music_volume)
            
    def stop_music(self):
        pygame.mixer.music.stop()
        self.current_music = None
        self.target_music = None
        self.fading = False
        self.fade_volume = self.music_volume
        
    def set_volume(self, volume):
        self.music_volume = max(0.0, min(1.0, volume))
        if not self.fading:
            pygame.mixer.music.set_volume(self.music_volume)
            
    def update_fade(self):
        """Update music fade transitions"""
        if not self.fading:
            return
            
        if self.fade_direction == "out":
            self.fade_volume = max(0, self.fade_volume - self.fade_speed)
            pygame.mixer.music.set_volume(self.fade_volume)
            
            if self.fade_volume <= 0:
                pygame.mixer.music.stop()
                self.fade_direction = "in"
                
                # Start new music
                if self.target_music == "level":
                    if self.load_music("TheEscapistOST"):
                        pygame.mixer.music.play(-1)
                        self.current_music = "level"
                elif self.target_music == "menu":
                    if self.load_music("WorldOutsideOST"):
                        pygame.mixer.music.play(-1)
                        self.current_music = "menu"
                        
        elif self.fade_direction == "in":
            self.fade_volume = min(self.music_volume, self.fade_volume + self.fade_speed)
            pygame.mixer.music.set_volume(self.fade_volume)
            
            if self.fade_volume >= self.music_volume:
                self.fading = False
                self.fade_volume = self.music_volume
                
    def is_playing(self):
        return pygame.mixer.music.get_busy()
