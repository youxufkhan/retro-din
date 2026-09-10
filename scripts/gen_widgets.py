#!/usr/bin/env python3
"""Generate the desktoptheme widget frames that Plasma asks for.

Plasma falls back per file, not per element: shipping an asset that omits an
element the widget queries draws that part as nothing. So a widget appears
here only once every element it declares is accounted for - the pure
nine-slice ones. Widgets whose artwork is drawn glyphs (arrows, checkmarks,
clock hands) are deliberately absent so they keep falling back cleanly.

Margin hints follow the geometry we draw rather than upstream's, since they
describe our own bezel. Behavioural hint flags are emitted as bare markers
because only their presence is read.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import svgslice as S  # noqa: E402

OUT = Path(__file__).resolve().parent.parent / "build/desktoptheme/RetroDIN/widgets"

WELL = "#001210"
BORDER_DARK = "#0a2e29"
TEAL_DIM = "#0d6b60"
TEAL = "#14b8a6"
TEAL_BRIGHT = "#2fd4bf"
AMBER = "#ffb454"
METAL = "url(#metalgrad)"

# name -> canvas, corner, margin, flags, [(prefix, fill, opacity, rings)]
SPEC = {
    "viewitem": dict(size=(32, 32), corner=4, margin=0,
                     flags=["hint-tile-center"], states=[
        ("normal",         WELL,      0,    []),
        ("hover",          "#3a2f1c", 1,    [("#5a4526", 1, 0, 1)]),
        ("selected",       "#4a3a20", 1,    [(AMBER, 1, 0, 1)]),
        ("selected+hover", "#56421f", 1,    [(AMBER, 1, 0, 1)]),
    ]),
    "lineedit": dict(size=(32, 32), corner=6, margin=4,
                     flags=["hint-tile-center", "hint-focus-over-base"], states=[
        ("base",       WELL, 1, [(BORDER_DARK, 1, 0, 1)]),
        ("hover",      WELL, 1, [(TEAL_DIM, 1, 0, 1)]),
        ("focus",      WELL, 1, [(TEAL, 1, 0, 1)]),
        ("focusframe", WELL, 0, [(AMBER, 1, 0, 2)]),
    ]),
    "menubaritem": dict(size=(32, 32), corner=4, margin=4, flags=[], states=[
        ("normal",  WELL,      0, []),
        ("hover",   "#04201d", 1, [(TEAL_DIM, 1, 0, 1)]),
        ("pressed", "#3a2f1c", 1, [(AMBER, 1, 0, 1)]),
    ]),
    "scrollwidget": dict(size=(32, 32), corner=4, margin=0, flags=[], states=[
        ("border", WELL, 0, [(BORDER_DARK, 1, 0, 1)]),
    ]),
    "toolbar": dict(size=(64, 64), corner=8, margin=4,
                    flags=["hint-tile-center"], states=[
        ("", METAL, 1, [(TEAL_DIM, 0.55, 0, 1)]),
    ]),
    "plasmoidheading": dict(size=(64, 64), corner=8, margin=4,
                            flags=["hint-stretch-borders"], states=[
        ("header", METAL, 1, [(TEAL_DIM, 0.6, 0, 1)]),
        ("footer", METAL, 1, [(TEAL_DIM, 0.6, 0, 1)]),
    ]),
    "frame": dict(size=(32, 32), corner=6, margin=4,
                  flags=["hint-tile-center"], states=[
        ("plain",  WELL,  0, [(TEAL_DIM, 0.5, 0, 1)]),
        ("raised", METAL, 1, [(TEAL_DIM, 1, 0, 1)]),
        ("sunken", WELL,  1, [(BORDER_DARK, 1, 0, 1)]),
    ], extras=[
        # upstream ships this fully transparent; kept so the element resolves
        '  <rect id="border-bottomleft" x="0" y="24" width="8" height="8"'
        ' fill="none" fill-opacity="0"/>',
    ]),
    "scrollbar": dict(size=(32, 32), corner=6, margin=0,
                      flags=["hint-tile-center", "private-hint-show-separator"],
                      states=[
        ("background-horizontal", WELL,  0.5, []),
        ("background-vertical",   WELL,  0.5, []),
        ("slider",                METAL, 1,   [(TEAL_DIM, 1, 0, 1)]),
        ("mouseover-slider",      METAL, 1,   [(TEAL_BRIGHT, 1, 0, 1)]),
    ], extras=[
        f'  <rect id="msc" x="29" y="29" width="3" height="3"'
        f' fill="{AMBER}" fill-opacity="0.5"/>',
        '  <rect id="hint-scrollbar-size" x="0" y="0" width="12" height="12"'
        ' fill="none"/>',
    ]),
    "tabbar": dict(size=(64, 64), corner=8, margin=4,
                   flags=["hint-tile-center"], states=[
        ("north-active-tab", METAL, 1, [(AMBER, 1, 0, 1)]),
        ("south-active-tab", METAL, 1, [(AMBER, 1, 0, 1)]),
        ("east-active-tab",  METAL, 1, [(AMBER, 1, 0, 1)]),
        ("west-active-tab",  METAL, 1, [(AMBER, 1, 0, 1)]),
    ]),
}

GRAD = """  <defs>
    <linearGradient id="metalgrad" gradientUnits="userSpaceOnUse"
                    x1="0" y1="0" x2="0" y2="{h}">
      <stop offset="0" stop-color="#414a4d"/>
      <stop offset="0.45" stop-color="#272d2f"/>
      <stop offset="1" stop-color="#14181a"/>
    </linearGradient>
  </defs>"""


def build(name, spec):
    w, h = spec["size"]
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}"'
             f' viewBox="0 0 {w} {h}">']
    if any(st[1] == METAL for st in spec["states"]):
        lines.append(GRAD.format(h=h))
    m = spec["margin"]
    if m:
        lines += [
            f'  <rect id="hint-top-margin" x="0" y="0" width="1" height="{m}"/>',
            f'  <rect id="hint-bottom-margin" x="0" y="{h - m}" width="1" height="{m}"/>',
            f'  <rect id="hint-left-margin" x="0" y="0" width="{m}" height="1"/>',
            f'  <rect id="hint-right-margin" x="{w - m}" y="0" width="{m}" height="1"/>',
        ]
    for flag in spec["flags"]:
        lines.append(f'  <rect id="{flag}" x="0" y="0" width="1" height="1"/>')
    lines += spec.get("extras", [])
    for prefix, fill, opacity, rings in spec["states"]:
        lines += S.frame(prefix, w, h, spec["corner"], fill,
                         fill_opacity=opacity, rings=rings) if prefix else \
                 _bare(w, h, spec["corner"], fill, opacity, rings)
    lines.append('</svg>')
    return "\n".join(lines) + "\n"


def _bare(w, h, corner, fill, opacity, rings):
    """Unprefixed nine-slice set, ids are the bare piece names."""
    out = S.frame("X", w, h, corner, fill, fill_opacity=opacity, rings=rings)
    return [ln.replace('id="X-', 'id="') for ln in out]


def main():
    for name, spec in SPEC.items():
        path = OUT / f"{name}.svg"
        path.write_text(build(name, spec), encoding="utf-8")
        print(f"wrote {path.name}")


if __name__ == "__main__":
    main()
