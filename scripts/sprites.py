#!/usr/bin/env python3
"""Export 4x pixel-art sprites from the Paulo Unity project for the website.

    scripts/sprites.py [path/to/paulo]

Frames sit on a regular grid in every sheet (32x32 blocks and characters, 16x16 items and
boosters); this script crops them, scales with nearest neighbour and writes
public/images/sprites/<name>.png. The sprite indices follow the Unity slicing in the
.meta files: row-major from the top-left corner ("atlas/0" is the top-left 32x32 cell).

Sources (Assets/App/Images):
  atlas.psd                bricks 0-7, crates 8-11, lock 12, anvil 13
  bomb.png, tnt.psd        two frames each, frame 0 is used
  heart.png, coin.png      animation frames, frame 0 is used
  boosters.png             skull, mushroom, key, star (16x16)
  items.png                32 fruits, vegetables and snacks (16x16)
  Themes/<name>/character.png  costumes, frame 0 is Paulo standing
"""
import sys
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
SITE = HERE.parent
PROJECT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.home() / "ghq/github.com/aureliendrouet/paulo"
IMAGES = PROJECT / "Assets/App/Images"
OUT = SITE / "public/images/sprites"
SCALE = 4

COSTUMES = ["base", "disco", "judo", "kungfu", "office", "robot", "soccer", "superhero", "surf"]

# name -> (sheet, cell size, column, row)
PICKS = {
    "lock": ("atlas.psd", 32, 0, 3),
    "anvil": ("atlas.psd", 32, 1, 3),
    "bomb": ("bomb.png", 32, 0, 0),
    "tnt": ("tnt.psd", 32, 0, 0),
    "heart": ("heart.png", 32, 0, 0),
    "coin": ("coin.png", 32, 0, 0),
    "skull": ("boosters.png", 16, 0, 0),
    "mushroom": ("boosters.png", 16, 1, 0),
    "key": ("boosters.png", 16, 2, 0),
    "star": ("boosters.png", 16, 3, 0),
}
for i in range(8):
    PICKS[f"brick-{i}"] = ("atlas.psd", 32, i % 4, i // 4)
for i in range(4):
    PICKS[f"crate-{i}"] = ("atlas.psd", 32, i, 2)
for i in range(32):
    PICKS[f"item-{i:02d}"] = ("items.png", 16, i % 8, i // 8)
for name in COSTUMES:
    PICKS[f"costume-{name}"] = (f"Themes/{name}/character.png", 32, 0, 0)

_sheets = {}


def sheet(path):
    if path not in _sheets:
        _sheets[path] = Image.open(IMAGES / path).convert("RGBA")
    return _sheets[path]


def export(name, path, size, col, row):
    im = sheet(path)
    x, y = col * size, row * size
    frame = im.crop((x, y, x + size, y + size))
    frame = frame.resize((size * SCALE, size * SCALE), Image.NEAREST)
    frame.save(OUT / f"{name}.png", optimize=True)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, (path, size, col, row) in PICKS.items():
        export(name, path, size, col, row)
    print(f"{len(PICKS)} sprites -> {OUT}")


if __name__ == "__main__":
    main()
