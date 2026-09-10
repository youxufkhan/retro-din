#!/usr/bin/env python3
"""Author the illustration-style desktoptheme assets in the DIN idiom.

These are the pictorial assets - seven-segment timer digits, the analogue
clock face and hands, dial meters, note backgrounds. Kept apart from
gen_glyphs.py because they are drawings rather than control furniture.

Elements sharing a canvas are laid out in non-overlapping cells, since KSvg
extracts each by its own bounding box. Anchor elements that upstream uses
purely to locate a rotation origin are emitted as transparent markers: they
must exist and report a box, but must not paint.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import svgslice as S  # noqa: E402

OUT = Path(__file__).resolve().parent.parent / "desktoptheme/RetroDIN/widgets"

TEAL = "#5eead4"
TEAL_MID = "#14b8a6"
TEAL_DIM = "#0d6b60"
AMBER = "#ffb454"
WELL = "#001210"
OFF = "#062420"


def svg(w, h, body):
    return "\n".join([
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}"'
        f' viewBox="0 0 {w} {h}">', *body, '</svg>']) + "\n"


# seven-segment vocabulary: a vacuum-fluorescent readout, lit teal on dark
SEGMENTS = {
    "a": (2, 0, 8, 2), "g": (2, 9, 8, 2), "d": (2, 18, 8, 2),
    "f": (0, 1, 2, 8), "b": (10, 1, 2, 8),
    "e": (0, 10, 2, 8), "c": (10, 10, 2, 8),
}
DIGITS = {
    "0": "abcdef", "1": "bc", "2": "abdeg", "3": "abcdg", "4": "bcfg",
    "5": "acdfg", "6": "acdefg", "7": "abc", "8": "abcdefg", "9": "abcdfg",
}


def seven_seg(eid, x, y, digit, lit):
    on = DIGITS[digit]
    parts = [f'  <g id="{eid}">']
    for name, (sx, sy, sw, sh) in SEGMENTS.items():
        colour = lit if name in on else OFF
        parts.append(f'    <rect x="{x + sx}" y="{y + sy}" width="{sw}"'
                     f' height="{sh}" fill="{colour}"/>')
    parts.append('  </g>')
    return "\n".join(parts)


def timer():
    body, cell = [], 14
    for row, (suffix, lit) in enumerate([("", TEAL), ("_1", TEAL_DIM)]):
        y = row * 24
        for i in range(10):
            body.append(seven_seg(f"{i}{suffix}", i * cell, y, str(i), lit))
        base = 10 * cell
        for k, name in enumerate(["separator", "separatorB", "separatorC"]):
            cx = base + k * 8 + 3
            body.append(
                f'  <g id="{name}{suffix}">'
                f'<rect x="{cx}" y="{y + 5}" width="2" height="2" fill="{lit}"/>'
                f'<rect x="{cx}" y="{y + 13}" width="2" height="2" fill="{lit}"/>'
                f'</g>')
    return svg(10 * cell + 26, 44, body)


def clock():
    cx = cy = 32
    ticks = "".join(
        f'<rect x="{cx - 1}" y="4" width="2" height="{5 if a % 90 == 0 else 3}"'
        f' fill="{TEAL if a % 90 == 0 else TEAL_DIM}"'
        f' transform="rotate({a} {cx} {cy})"/>'
        for a in range(0, 360, 30))
    body = [
        f'  <g id="ClockFace">'
        f'<circle cx="{cx}" cy="{cy}" r="30" fill="{WELL}"'
        f' stroke="#050606" stroke-width="2"/>'
        f'<circle cx="{cx}" cy="{cy}" r="31" fill="none"'
        f' stroke="{TEAL_MID}" stroke-width="2"/>{ticks}</g>',
        f'  <rect id="HourHand" x="{cx - 1.5}" y="{cy - 16}" width="3"'
        f' height="18" fill="{TEAL}"/>',
        f'  <rect id="MinuteHand" x="{cx - 1}" y="{cy - 24}" width="2"'
        f' height="26" fill="{TEAL}"/>',
        f'  <rect id="SecondHand" x="{cx - 0.5}" y="{cy - 26}" width="1"'
        f' height="30" fill="{AMBER}"/>',
        f'  <circle id="HandCenterScrew" cx="{cx}" cy="{cy}" r="2.5"'
        f' fill="{AMBER}"/>',
        f'  <circle id="Glass" cx="{cx}" cy="{cy - 10}" r="18" fill="#ffffff"'
        f' fill-opacity="0.04"/>',
    ]
    # shadows exist so the clock applet can offset them; kept non-painting
    for eid, w, h in [("HourHandShadow", 3, 18), ("MinuteHandShadow", 2, 26),
                      ("SecondHandShadow", 1, 30)]:
        body.append(f'  <rect id="{eid}" x="66" y="0" width="{w}"'
                    f' height="{h}" fill="#000000" fill-opacity="0"/>')
    return svg(72, 64, body)


def analog_meter():
    cx, cy = 32, 34
    arc = "".join(
        f'<rect x="{cx - 0.75}" y="6" width="1.5" height="4"'
        f' fill="{TEAL_DIM}" transform="rotate({a} {cx} {cy})"/>'
        for a in range(-60, 61, 15))
    body = [
        f'  <g id="background">'
        f'<rect x="0" y="0" width="64" height="48" fill="{WELL}"/>'
        f'<path d="M 6 34 A 26 26 0 0 1 58 34" fill="none"'
        f' stroke="{TEAL_MID}" stroke-width="1.5"/>{arc}</g>',
        f'  <rect id="label0" x="8" y="38" width="8" height="6"'
        f' fill="{TEAL_DIM}" fill-opacity="0.7"/>',
        f'  <rect id="label1" x="48" y="38" width="8" height="6"'
        f' fill="{TEAL_DIM}" fill-opacity="0.7"/>',
        f'  <rect id="pointer" x="{cx - 1}" y="{cy - 24}" width="2"'
        f' height="26" fill="{AMBER}"/>',
        f'  <rect id="pointer-shadow" x="66" y="0" width="2" height="26"'
        f' fill="#000000" fill-opacity="0"/>',
        f'  <g id="foreground">'
        f'<circle cx="{cx}" cy="{cy}" r="3" fill="{AMBER}"/>'
        f'<rect x="0" y="0" width="64" height="20" fill="#ffffff"'
        f' fill-opacity="0.03"/></g>',
        # rotation anchors: must resolve to a box, must not paint
        f'  <rect id="rotatecenter" x="{cx - 1}" y="{cy - 1}" width="2"'
        f' height="2" fill="none" fill-opacity="0"/>',
        f'  <rect id="rotateminmax" x="6" y="8" width="52" height="26"'
        f' fill="none" fill-opacity="0"/>',
    ]
    return svg(72, 48, body)


def notes():
    tints = [("yellow", "#3a2f1c", AMBER), ("orange", "#3a2718", "#ff9a4d"),
             ("red", "#331c1c", "#ff7a6b"), ("pink", "#33202c", "#ff8fc0"),
             ("blue", "#132630", TEAL_MID), ("green", "#12301f", "#4fd98a"),
             ("white", "#2a3134", "#cfece8"), ("black", "#0c0f10", TEAL_DIM),
             ("transluscent", WELL, TEAL_DIM)]
    body, cell = [], 34
    for i, (name, fill, border) in enumerate(tints):
        x = i * cell
        opacity = "0.55" if name == "transluscent" else "1"
        body.append(
            f'  <g id="{name}-notes">'
            f'<rect x="{x + 1}" y="1" width="32" height="32" fill="{fill}"'
            f' fill-opacity="{opacity}"/>'
            f'<rect x="{x + 1}" y="1" width="32" height="2" fill="{border}"/>'
            f'</g>')
    return svg(len(tints) * cell, 34, body)


def branding():
    body = [
        '  <g id="brilliant">'
        f'<circle cx="16" cy="16" r="13" fill="none" stroke="{TEAL_MID}"'
        f' stroke-width="2"/>'
        f'<circle cx="16" cy="16" r="8" fill="{WELL}" stroke="#050606"'
        f' stroke-width="1"/>'
        f'<rect x="15" y="5" width="2" height="6" fill="{TEAL}"/>'
        f'<circle cx="16" cy="16" r="2" fill="{AMBER}"/></g>']
    return svg(32, 32, body)


def monitor():
    """A screen bezel plus the colourway swatches the applet indexes by id."""
    body = [ln.replace('id="X-', 'id="')
            for ln in S.frame("X", 64, 48, 8, WELL, 1,
                              rings=[(TEAL_MID, 1, 0, 2)])]
    swatch = {"VIO": TEAL_DIM, "PI": "#ff8fc0", "BLU": TEAL_MID,
              "GR": "#4fd98a", "RO": AMBER, "GRA": "#7e9295"}
    ids = []
    for tag, colour in swatch.items():
        for n in range(1, 6):
            ids.append((f"HIGHLIGHT_{tag}{n}_1_", colour, 0.55))
            ids.append((f"{tag}_{n}_3_", colour, 1))
    # upstream's exact spellings, including the odd and escaped ones
    fixed = [("HIGHLIGHT_PI2_1_-4", "#ff8fc0", 0.55),
             ("HIGHLIGHT_PI2_2_", "#ff8fc0", 0.55),
             ("PINK_1_3_", "#ff8fc0", 1), ("PINK_2_3_", "#ff8fc0", 1),
             ("VIOLET_1_3_", TEAL_DIM, 1), ("VIOLET_2_3_", TEAL_DIM, 1),
             ("BLUE_1_3_", TEAL_MID, 1), ("BLUE_2_3_", TEAL_MID, 1),
             ("BLUE_3_3_", TEAL_MID, 1), ("BLUE_4_3_", TEAL_MID, 1),
             ("GREEN_1_1_", "#4fd98a", 1), ("GREEN_2_1_", "#4fd98a", 1),
             ("GREEN_3_1_", "#4fd98a", 1), ("GREEN_4_1_", "#4fd98a", 1),
             ("RED_x2F_ORANGE_1_2_", AMBER, 1),
             ("RED_x2F_ORANGE_2_1_", AMBER, 1),
             ("RED_x2F_ORANGE_3_2_", AMBER, 1),
             ("RED_x2F_ORANGE_4_1_", AMBER, 1),
             ("RED_x2F_ORANGE_5_2_-8", AMBER, 1),
             ("HIGHLIGHTS_RO1_2_", AMBER, 0.55),
             ("HIGHLIGHTS_RO2_1_", AMBER, 0.55),
             ("HIGHLIGHTS_RO3_2_", AMBER, 0.55),
             ("HIGHLIGHTS_RO4_2_", AMBER, 0.55),
             ("HIGHLIGHTS_RO5_1_", AMBER, 0.55),
             ("GRAY_1_1_", "#7e9295", 1), ("GRAY_2_1_", "#7e9295", 1),
             ("GRAY_3_1_", "#7e9295", 1), ("GRAY_4_1_", "#7e9295", 1),
             ("GRAY_5_1_", "#7e9295", 1),
             ("HIGHLIGHT_VIO1_1_", TEAL_DIM, 0.55),
             ("HIGHLIGHT_VIO2_1_", TEAL_DIM, 0.55),
             ("HIGHLIGHT_BLU1_1_", TEAL_MID, 0.55),
             ("HIGHLIGHT_BLU2_1_", TEAL_MID, 0.55),
             ("HIGHLIGHT_BLU3_1_", TEAL_MID, 0.55),
             ("HIGHLIGHT_BLU4_1_", TEAL_MID, 0.55),
             ("HIGHLIGHT_GR1_1_", "#4fd98a", 0.55),
             ("HIGHLIGHT_GR2_1_", "#4fd98a", 0.55),
             ("HIGHLIGHT_GR3_1_", "#4fd98a", 0.55),
             ("HIGHLIGHT_GR4_1_", "#4fd98a", 0.55),
             ("HIGHLIGHT_GRA1_1_", "#7e9295", 0.55),
             ("HIGHLIGHT_GRA2_1_", "#7e9295", 0.55),
             ("HIGHLIGHT_GRA3_2_", "#7e9295", 0.55),
             ("HIGHLIGHT_GRA4_2_", "#7e9295", 0.55)]
    seen, x = set(), 64
    for eid, colour, opacity in fixed:
        if eid in seen:
            continue
        seen.add(eid)
        body.append(f'  <rect id="{eid}" x="{x}" y="0" width="6" height="6"'
                    f' fill="{colour}" fill-opacity="{opacity}"/>')
        x += 7
    body.append(f'  <rect id="glass" x="8" y="8" width="48" height="16"'
                f' fill="#ffffff" fill-opacity="0.04"/>')
    return svg(x, 48, body)


ASSETS = {
    "timer": timer,
    "clock": clock,
    "analog_meter": analog_meter,
    "notes": notes,
    "branding": branding,
    "monitor": monitor,
}


def main():
    for name, fn in ASSETS.items():
        (OUT / f"{name}.svg").write_text(fn(), encoding="utf-8")
        print(f"wrote {name}.svg")


if __name__ == "__main__":
    main()
