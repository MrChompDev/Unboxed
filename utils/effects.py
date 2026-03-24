from __future__ import annotations

import random

import pygame
import numpy as np

def apply_scanlines(surface: pygame.Surface, intensity: int = 30) -> pygame.Surface:
    result = surface.copy()
    for y in range(0, surface.get_height(), 4):
        pygame.draw.line(result, (0, 0, 0), (0, y), (surface.get_width(), y))
    return result

def apply_noise(surface: pygame.Surface, amount: int = 10) -> pygame.Surface:
    arr = pygame.surfarray.array3d(surface)
    noise = np.random.randint(-amount, amount, arr.shape)
    arr = np.clip(arr.astype(np.int16) + noise, 0, 255).astype(np.uint8)
    return pygame.surfarray.make_surface(arr)

def apply_glitch(surface: pygame.Surface, offset_range: int = 8) -> pygame.Surface:
    arr = pygame.surfarray.array3d(surface.copy())
    height = arr.shape[1]
    for _ in range(random.randint(1, 4)):
        y = random.randint(0, height - 1)
        offset = random.randint(-offset_range, offset_range)
        if 0 <= y < height:
            arr[:, y] = np.roll(arr[:, y], offset, axis=0)
    return pygame.surfarray.make_surface(arr)

def chromatic_aberration(surface: pygame.Surface, amount: int = 3) -> pygame.Surface:
    r = pygame.surfarray.array2d(pygame.Surface(surface.get_size()))
    g = pygame.surfarray.array2d(pygame.Surface(surface.get_size()))
    b = pygame.surfarray.array2d(pygame.Surface(surface.get_size()))
    r[:] = pygame.surfarray.array2d(surface) >> 16 & 0xFF
    g[:] = pygame.surfarray.array2d(surface) >> 8 & 0xFF
    b[:] = pygame.surfarray.array2d(surface) & 0xFF
    
    result = pygame.Surface(surface.get_size())
    pygame.surfarray.blit_array(result, np.dstack([np.roll(r, amount, 0), g, np.roll(b, -amount, 0)]))
    return result

def pixel_sort(surface: pygame.Surface, threshold: int = 128) -> pygame.Surface:
    arr = pygame.surfarray.array3d(surface)
    for x in range(arr.shape[0]):
        column = arr[x]
        mask = np.all(column > threshold, axis=1)
        sorted_pixels = column[mask][np.argsort(column[mask].sum(axis=1))]
        arr[x][mask] = sorted_pixels
    return pygame.surfarray.make_surface(arr)
