from __future__ import annotations

import random
from typing import Tuple

RGB = Tuple[int, int, int]

def hex_to_rgb(hex_color: str) -> RGB:
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def shift_hue(rgb: RGB, shift: int) -> RGB:
    r, g, b = rgb
    if r > g and r > b:
        g = min(255, g + shift)
        b = max(0, b - shift)
    elif g > r and g > b:
        r = max(0, r - shift)
        b = min(255, b + shift)
    return (r, g, b)

def random_glitch_color() -> RGB:
    return (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))

def degrade_colour(rgb: RGB, factor: int) -> RGB:
    return (
        max(0, min(255, rgb[0] - factor)),
        max(0, min(255, rgb[1] - factor)),
        max(0, min(255, rgb[2] - factor))
    )
