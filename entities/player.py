from __future__ import annotations

from typing import Mapping, Sequence, Tuple, Literal

import pygame
from utils.constants import PLAYER_SPEED, PLAYER_JUMP, GRAVITY, FRICTION, PLAYER_COLOR

Perspective = Literal["side", "top"]
Color = Tuple[int, int, int]

class Player:
    def __init__(self, x: int, y: int, perspective: Perspective = "side") -> None:
        self.rect: pygame.Rect = pygame.Rect(x, y, 48, 96)
        self.velocity: pygame.math.Vector2 = pygame.math.Vector2(0, 0)
        self.on_ground: bool = False
        self.facing_right: bool = True
        self.perspective: Perspective = perspective
        self.layer: int = 1
        self.glitching: bool = False
        self.anim_frame: int = 0
        self.anim_timer: int = 0
        self.jump_cooldown: int = 0
        
    def set_perspective(self, perspective: Perspective) -> None:
        self.perspective = perspective
        
    def set_layer(self, layer: int) -> None:
        self.layer = layer
        
    def move(self, dx: int, dy: int) -> None:
        self.rect.x += dx
        self.rect.y += dy
        
    def jump(self) -> None:
        if self.on_ground and self.jump_cooldown <= 0:
            self.velocity.y = PLAYER_JUMP
            self.on_ground = False
            self.jump_cooldown = 10
            
    def apply_gravity(self) -> None:
        if self.perspective == "side":
            self.velocity.y += GRAVITY
            
    def apply_friction(self) -> None:
        self.velocity.x *= FRICTION
        
    def update(self, platforms: Sequence[pygame.Rect]) -> None:
        keys = pygame.key.get_pressed()
        
        if self.jump_cooldown > 0:
            self.jump_cooldown -= 1
        
        if self.perspective == "side":
            if keys[pygame.K_LEFT] or keys[pygame.K_a] or keys[pygame.K_KP4]:
                self.velocity.x = -PLAYER_SPEED
                self.facing_right = False
            elif keys[pygame.K_RIGHT] or keys[pygame.K_d] or keys[pygame.K_KP6]:
                self.velocity.x = PLAYER_SPEED
                self.facing_right = True
            else:
                self.velocity.x *= FRICTION
                
            if keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w] or keys[pygame.K_KP8]:
                self.jump()
                
            self.apply_gravity()
            self.rect.x += self.velocity.x
            self.handle_collisions(platforms, horizontal=True)
            self.rect.y += self.velocity.y
            self.handle_collisions(platforms, horizontal=False)
            
        elif self.perspective == "top":
            if keys[pygame.K_LEFT] or keys[pygame.K_a] or keys[pygame.K_KP4]:
                self.rect.x -= PLAYER_SPEED
            if keys[pygame.K_RIGHT] or keys[pygame.K_d] or keys[pygame.K_KP6]:
                self.rect.x += PLAYER_SPEED
            if keys[pygame.K_UP] or keys[pygame.K_w] or keys[pygame.K_KP8]:
                self.rect.y -= PLAYER_SPEED
            if keys[pygame.K_DOWN] or keys[pygame.K_s] or keys[pygame.K_KP2]:
                self.rect.y += PLAYER_SPEED
                
        self.anim_timer += 1
        if self.anim_timer > 10:
            self.anim_frame = (self.anim_frame + 1) % 4
            self.anim_timer = 0
            
    def handle_collisions(self, platforms: Sequence[pygame.Rect], horizontal: bool) -> None:
        for platform in platforms:
            if self.rect.colliderect(platform):
                if horizontal:
                    if self.velocity.x > 0:
                        self.rect.right = platform.left
                    elif self.velocity.x < 0:
                        self.rect.left = platform.right
                else:
                    if self.velocity.y > 0:
                        self.rect.bottom = platform.top
                        self.on_ground = True
                        self.velocity.y = 0
                    elif self.velocity.y < 0:
                        self.rect.top = platform.bottom
                        self.velocity.y = 0
                        
    def draw(self, surface: pygame.Surface, layer_colors: Mapping[str, Color]) -> None:
        color = PLAYER_COLOR
        
        x, y = self.rect.x, self.rect.y
        w, h = self.rect.width, self.rect.height
        
        pygame.draw.rect(surface, color, (x, y, w, h))
        
        eye_offset = 16 if self.facing_right else 8
        pygame.draw.rect(surface, (30, 30, 35), (x + eye_offset, y + 16, 16, 16))
        
        if self.perspective == "side":
            pygame.draw.line(surface, color, (x, y + h - 8), (x + w, y + h - 8), 4)
            
    def get_center(self) -> Tuple[int, int]:
        return self.rect.center
        
    def teleport(self, x: int, y: int) -> None:
        self.rect.x = int(x)
        self.rect.y = int(y)
