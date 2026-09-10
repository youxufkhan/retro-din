#!/usr/bin/env python3
"""Derive desktoptheme/RetroDIN/colors from the colour scheme.

The desktoptheme's colors file only styles Plasma shell widgets - panel,
systray, popups - so its foregrounds can be the palette's bright teal while
the app-facing colour scheme keeps the calmer off-white that document text
needs for legibility.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "color-schemes/RetroDIN.colors"
DEST = ROOT / "desktoptheme/RetroDIN/colors"

PANEL_TEAL = "94,234,212"
PANEL_GROUPS = {"Colors:Window", "Colors:View", "Colors:Header",
                "Colors:Complementary", "Colors:Tooltip"}

out, group = [], None
for line in SRC.read_text(encoding="utf-8").splitlines():
    header = re.match(r"^\[([^\]]+)\]", line)
    if header:
        group = header.group(1)
    elif group in PANEL_GROUPS and line.startswith("ForegroundNormal="):
        line = f"ForegroundNormal={PANEL_TEAL}"
    out.append(line)

DEST.write_text("\n".join(out) + "\n", encoding="utf-8")
print(f"wrote {DEST}")
