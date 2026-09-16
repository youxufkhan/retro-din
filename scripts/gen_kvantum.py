#!/usr/bin/env python3
"""Generate the Kvantum theme that styles Qt app interiors.

Kvantum is what reaches the surfaces the desktoptheme cannot: menus,
toolbars, scrollbars, tabs and buttons inside Dolphin, Kate, browsers.

KvDark is used as the base because its artwork is pure greyscale - every
colour in it has zero saturation - so remapping its luminance ramp onto the
DIN charcoal ramp keeps the shading structure intact without hue conflicts.
A blind substitution table over a hand-drawn colour theme would produce mud;
a monotonic ramp over a greyscale one does not.

Contrast structure is preserved by mapping in bands: dark values stay
backgrounds, light values stay glyphs and text. Collapsing the light end into
mid-grey would wash out the arrows and checkmarks drawn in the SVG.
"""
import re
import sys
from pathlib import Path

BASE = Path(sys.argv[1] if len(sys.argv) > 1 else "/usr/share/Kvantum/KvDark")
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "kvantum/RetroDIN"

# (max_luminance, target) - the DIN ramp, cool-tinted, monotonic
RAMP = [
    (12,  "#050807"), (22,  "#0a0f10"), (28,  "#0d1314"), (33,  "#14181a"),
    (38,  "#171c1d"), (45,  "#1a2022"), (52,  "#21282a"), (58,  "#252c2e"),
    (65,  "#272d2f"), (80,  "#313a3c"), (92,  "#384245"), (96,  "#3b4649"),
    (105, "#414a4d"), (125, "#4b5659"), (140, "#525e61"), (155, "#7d9e99"),
    (172, "#8bada8"), (185, "#9bbdb7"), (196, "#a8c4c0"), (215, "#bcd9d4"),
    (232, "#c7e3de"),
]
FALLBACK = "#cfece8"

PALETTE = {
    "window.color": "#1a2022",
    "base.color": "#001210",
    "alt.base.color": "#04201d",
    "button.color": "#272d2f",
    "light.color": "#414a4d",
    "mid.light.color": "#313a3c",
    "dark.color": "#0a0f10",
    "mid.color": "#21282a",
    "highlight.color": "#ffb454",
    "inactive.highlight.color": "#8a6a3a",
    "text.color": "#cfece8",
    "window.text.color": "#cfece8",
    "button.text.color": "#cfece8",
    "disabled.text.color": "#5e7875",
    "tooltip.text.color": "#cfece8",
    "highlight.text.color": "#101314",
    "link.color": "#14b8a6",
    "link.visited.color": "#0d6b60",
    "progress.indicator.text.color": "#101314",
}


def luminance(hex_colour):
    r, g, b = (int(hex_colour[i:i + 2], 16) for i in (1, 3, 5))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def remap(match):
    lum = luminance(match.group(0))
    for ceiling, target in RAMP:
        if lum <= ceiling:
            return target
    return FALLBACK


def build_svg():
    text = (BASE / f"{BASE.name}.svg").read_text(encoding="utf-8",
                                                 errors="surrogateescape")
    return re.sub(r"#[0-9a-fA-F]{6}", remap, text)


def build_config():
    text = (BASE / f"{BASE.name}.kvconfig").read_text(encoding="utf-8",
                                                      errors="surrogateescape")
    body = "\n".join(f"{k}={v}" for k, v in PALETTE.items())
    text, n = re.subn(r"\[GeneralColors\]\n(?:[^\[]*)",
                      f"[GeneralColors]\n{body}\n\n", text, count=1)
    if n != 1:
        sys.exit("could not locate [GeneralColors] in the base kvconfig")
    text = re.sub(r"^comment=.*$", "comment=90s car-stereo/hi-fi DIN unit style",
                  text, flags=re.MULTILINE)
    text = re.sub(r"^author=.*$",
                  "author=yousuf khan (youxufkhan), colour remap of Tsu Jan's KvDark",
                  text, flags=re.MULTILINE)
    return text


def main():
    if not BASE.is_dir():
        sys.exit(f"base Kvantum theme not found: {BASE}")
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "RetroDIN.svg").write_text(build_svg(), encoding="utf-8",
                                      errors="surrogateescape")
    (OUT / "RetroDIN.kvconfig").write_text(build_config(), encoding="utf-8",
                                           errors="surrogateescape")
    print(f"wrote {OUT}/RetroDIN.svg and RetroDIN.kvconfig")


if __name__ == "__main__":
    main()
