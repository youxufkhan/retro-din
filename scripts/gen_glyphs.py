#!/usr/bin/env python3
"""Author the drawn-artwork desktoptheme assets in the DIN idiom.

These are the widgets whose elements are glyphs rather than nine-slice
frames - arrows, checkmarks, switch knobs, meters. Each element is queried by
id and extracted by its own bounding box, so glyphs that share a file are
laid out in non-overlapping cells; frame states, which are selected by id
rather than position, deliberately share coordinates.

Drawing vocabulary: thin square-capped strokes, teal for a resting glyph,
amber for checked or active, the recessed well for anything inset.
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
AMBER_SOFT = "#ffd08a"
WELL = "#001210"
WELL_ALT = "#04201d"
BORDER_DARK = "#0a2e29"
METAL = "url(#metalgrad)"

GRAD = """  <defs>
    <linearGradient id="metalgrad" gradientUnits="userSpaceOnUse"
                    x1="0" y1="0" x2="0" y2="{h}">
      <stop offset="0" stop-color="#414a4d"/>
      <stop offset="0.45" stop-color="#272d2f"/>
      <stop offset="1" stop-color="#14181a"/>
    </linearGradient>
    <radialGradient id="knobgrad" cx="35%" cy="28%" r="75%">
      <stop offset="0" stop-color="#454b4d"/>
      <stop offset="1" stop-color="#181c1d"/>
    </radialGradient>
  </defs>"""


def svg(width, height, body, grad=False):
    head = ['<?xml version="1.0" encoding="UTF-8"?>',
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}"'
            f' height="{height}" viewBox="0 0 {width} {height}">']
    if grad:
        head.append(GRAD.format(h=height))
    return "\n".join(head + body + ['</svg>']) + "\n"


def chevron(eid, cx, cy, direction, colour=TEAL, size=5, w=2):
    """A square-capped chevron, drawn inside its own cell."""
    dx, dy = {"up": (0, -1), "down": (0, 1),
              "left": (-1, 0), "right": (1, 0)}[direction]
    if dx:
        pts = f"{cx - dx * size / 2},{cy - size} {cx + dx * size / 2},{cy} " \
              f"{cx - dx * size / 2},{cy + size}"
    else:
        pts = f"{cx - size},{cy - dy * size / 2} {cx},{cy + dy * size / 2} " \
              f"{cx + size},{cy - dy * size / 2}"
    return (f'  <polyline id="{eid}" points="{pts}" fill="none"'
            f' stroke="{colour}" stroke-width="{w}" stroke-linecap="square"'
            f' stroke-linejoin="miter"/>')


def knob(eid, cx, cy, r, ring=TEAL_MID, ring_w=2, notch=True):
    """The rotary knob that the launcher and slider handles share."""
    parts = [f'  <g id="{eid}">',
             f'    <circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#knobgrad)"'
             f' stroke="#050606" stroke-width="1"/>',
             f'    <circle cx="{cx}" cy="{cy}" r="{r + 1}" fill="none"'
             f' stroke="{ring}" stroke-width="{ring_w}"/>']
    if notch:
        parts.append(f'    <rect x="{cx - 0.75}" y="{cy - r + 1}" width="1.5"'
                     f' height="{r * 0.6:g}" fill="{TEAL}"/>')
    parts.append('  </g>')
    return "\n".join(parts)


def cell_frame(prefix, x, y, w, h, corner, fill, opacity=1, rings=()):
    """A nine-slice set offset into a cell of a shared canvas."""
    out = []
    for line in S.frame(prefix, w, h, corner, fill,
                        fill_opacity=opacity, rings=rings):
        out.append(line)
    if x or y:
        out = [f'  <g transform="translate({x},{y})">'] + \
              ["  " + ln for ln in out] + ['  </g>']
    return out


# ---------------------------------------------------------------- assets

def arrows():
    body = []
    for i, d in enumerate(["up", "down", "left", "right"]):
        body.append(chevron(f"{d}-arrow", 11 + i * 22, 11, d))
    return svg(88, 22, body)


def checkmarks():
    body = [
        '  <polyline id="checkbox" points="4,12 8,16 17,6" fill="none"'
        f' stroke="{AMBER}" stroke-width="2.5" stroke-linecap="square"/>',
        f'  <circle id="radiobutton" cx="33" cy="11" r="4" fill="{AMBER}"/>',
    ]
    return svg(44, 22, body)


def radiobutton():
    body = []
    for i, (eid, ring, dot) in enumerate([
            ("normal", TEAL_DIM, None), ("hover", TEAL_MID, None),
            ("focus", AMBER, None), ("checked", AMBER, AMBER)]):
        cx = 11 + i * 22
        g = [f'  <g id="{eid}">',
             f'    <circle cx="{cx}" cy="11" r="8" fill="{WELL}"'
             f' stroke="{ring}" stroke-width="1.5"/>']
        if dot:
            g.append(f'    <circle cx="{cx}" cy="11" r="4" fill="{dot}"/>')
        g.append('  </g>')
        body.append("\n".join(g))
    body.append(f'  <circle id="symbol" cx="99" cy="11" r="4" fill="{AMBER}"/>')
    body.append('  <rect id="shadow" x="110" y="0" width="22" height="22"'
                ' fill="none" fill-opacity="0"/>')
    return svg(132, 22, body)


def switch():
    body = []
    # slot: three horizontal slices per state, side by side in their own cells
    for row, (state, fill, border) in enumerate([
            ("inactive", WELL, BORDER_DARK), ("active", "#3a2f1c", AMBER)]):
        y = row * 22
        for eid, x, w in [("left", 0, 6), ("center", 6, 10), ("right", 16, 6)]:
            body.append(
                f'  <g id="{state}-{eid}">'
                f'<rect x="{x}" y="{y + 6}" width="{w}" height="10"'
                f' fill="{fill}"/>'
                f'<rect x="{x}" y="{y + 6}" width="{w}" height="1.5"'
                f' fill="{border}"/>'
                f'<rect x="{x}" y="{y + 14.5}" width="{w}" height="1.5"'
                f' fill="{border}"/></g>')
    for i, (eid, ring) in enumerate([
            ("handle", TEAL_MID), ("handle-hover", TEAL),
            ("handle-focus", AMBER), ("handle-pressed", AMBER_SOFT)]):
        body.append(knob(eid, 33 + i * 22, 11, 7, ring=ring, notch=False))
    body.append('  <rect id="handle-shadow" x="121" y="0" width="22"'
                ' height="22" fill="none" fill-opacity="0"/>')
    body.append('  <rect id="shadow" x="143" y="0" width="22" height="22"'
                ' fill="none" fill-opacity="0"/>')
    return svg(165, 44, body, grad=True)


def slider():
    body = []
    body += cell_frame("groove", 0, 0, 32, 32, 6, WELL, 1,
                       [(BORDER_DARK, 1, 0, 1)])
    body += cell_frame("groove-highlight", 0, 0, 32, 32, 6, AMBER, 0.85,
                       [(AMBER, 1, 0, 1)])
    for i, orient in enumerate(["horizontal", "vertical"]):
        base = 40 + i * 66
        body.append(knob(f"{orient}-slider-handle", base + 11, 11, 7))
        body.append(knob(f"{orient}-slider-hover", base + 33, 11, 7, ring=TEAL))
        body.append(knob(f"{orient}-slider-focus", base + 55, 11, 7, ring=AMBER))
        body.append(f'  <rect id="{orient}-slider-shadow" x="{base}" y="22"'
                    ' width="22" height="10" fill="none" fill-opacity="0"/>')
    body.append('  <rect id="shadow" x="172" y="22" width="22" height="10"'
                ' fill="none" fill-opacity="0"/>')
    body.append(f'  <rect id="msc" x="190" y="29" width="3" height="3"'
                f' fill="{AMBER}" fill-opacity="0.5"/>')
    return svg(196, 32, body, grad=True)


def busywidget():
    def reel(eid, cx, cy, r, colour):
        segs = []
        for k in range(8):
            a = k * 45
            op = 0.25 + 0.75 * (k / 7)
            segs.append(
                f'    <rect x="{cx - 1}" y="{cy - r}" width="2" height="{r * 0.45:g}"'
                f' fill="{colour}" fill-opacity="{op:.2f}"'
                f' transform="rotate({a} {cx} {cy})"/>')
        return f'  <g id="{eid}">\n' + "\n".join(segs) + '\n  </g>'
    body = [reel("busywidget", 16, 16, 13, TEAL),
            reel("22-22-busywidget", 43, 16, 10, TEAL),
            reel("16-16-busywidget", 64, 16, 7, TEAL),
            f'  <circle id="stopped" cx="84" cy="16" r="7" fill="none"'
            f' stroke="{TEAL_DIM}" stroke-width="2"/>']
    return svg(96, 32, body)


def line():
    body = [f'  <rect id="vertical-line" x="0" y="0" width="1" height="22"'
            f' fill="{TEAL_DIM}" fill-opacity="0.6"/>',
            f'  <rect id="horizontal-line" x="4" y="0" width="22" height="1"'
            f' fill="{TEAL_DIM}" fill-opacity="0.6"/>']
    return svg(32, 22, body)


def dragger():
    def grip(eid, x, y, w, h):
        dots = []
        for gy in range(y + 2, y + h - 1, 4):
            for gx in range(x + 2, x + w - 1, 4):
                dots.append(f'    <rect x="{gx}" y="{gy}" width="2" height="2"'
                            f' fill="{TEAL_DIM}"/>')
        return f'  <g id="{eid}">\n' + "\n".join(dots) + '\n  </g>'
    body = [grip("center", 0, 0, 16, 16),
            grip("top", 16, 0, 16, 8),
            grip("bottom", 16, 8, 16, 8),
            grip("background-vertical-top", 32, 0, 16, 8),
            grip("background-vertical-topleft", 32, 8, 8, 8),
            grip("background-vertical-topright", 40, 8, 8, 8)]
    return svg(48, 16, body)


def picker():
    body = _bare(32, 32, 6, WELL, 1, [(TEAL_MID, 1, 0, 2)])
    body += cell_frame("mask", 0, 0, 32, 32, 6, "#ffffff", 1, [])
    return svg(32, 32, body)


def translucentbackground():
    body = _bare(48, 48, 8, WELL, 0.82, [(BORDER_DARK, 1, 0, 1)])
    body += cell_frame("shadow", 0, 0, 48, 48, 8, "#000000", 0.28, [])
    body.append('  <rect id="hint-tile-center" x="0" y="0" width="1"'
                ' height="1"/>')
    return svg(48, 48, body)


def plot_background():
    body = [f'  <rect x="0" y="0" width="32" height="32" fill="{WELL}"/>',
            f'  <g stroke="{TEAL_DIM}" stroke-opacity="0.35" stroke-width="0.5">',
            *[f'    <line x1="0" y1="{y}" x2="32" y2="{y}"/>'
              for y in range(8, 32, 8)],
            *[f'    <line x1="{x}" y1="0" x2="{x}" y2="32"/>'
              for x in range(8, 32, 8)],
            '  </g>']
    return svg(32, 32, body)


def glowbar():
    body = _bare(32, 32, 6, AMBER, 0.22, [(AMBER, 0.7, 0, 1)])
    body.append(f'  <circle id="rad" cx="16" cy="16" r="6" fill="{AMBER}"'
                f' fill-opacity="0.35"/>')
    return svg(32, 32, body)


def margins_highlight():
    body = [f'  <rect id="fill" x="0" y="0" width="16" height="16"'
            f' fill="{AMBER}" fill-opacity="0.18"/>']
    for eid, x, y in [("topleft", 16, 0), ("topright", 24, 0),
                      ("bottomleft", 16, 8), ("bottomright", 24, 8)]:
        body.append(f'  <rect id="{eid}" x="{x}" y="{y}" width="8" height="8"'
                    f' fill="{AMBER}" fill-opacity="0.5"/>')
    return svg(32, 16, body)


def bar_meter(vertical):
    rings = [(TEAL_DIM, 1, 0, 1)]
    body = cell_frame("bar-inactive", 0, 0, 32, 32, 6, WELL, 1, rings)
    body += cell_frame("bar-active", 0, 0, 32, 32, 6, TEAL_MID, 0.9,
                       [(TEAL, 1, 0, 1)])
    body.append(f'  <rect id="msc" x="29" y="29" width="3" height="3"'
                f' fill="{AMBER}" fill-opacity="0.5"/>')
    body.append('  <rect id="hint-tile-center" x="0" y="0" width="1"'
                ' height="1"/>')
    return svg(32, 32, body)


def media_delegate():
    body = cell_frame("picture", 0, 0, 32, 32, 6, WELL, 1,
                      [(BORDER_DARK, 1, 0, 1)])
    body += cell_frame("picture-selected", 0, 0, 32, 32, 6, "#3a2f1c", 1,
                       [(AMBER, 1, 0, 1)])
    for eid, x, y in [("focus-topleft", 32, 0), ("focus-left", 32, 8),
                      ("focus-bottomleft", 32, 24)]:
        body.append(f'  <rect id="{eid}" x="{x}" y="{y}" width="8" height="8"'
                    f' fill="{AMBER}" fill-opacity="0.8"/>')
    return svg(40, 32, body)


def calendar():
    body = [f'  <circle id="event" cx="4" cy="4" r="3" fill="{AMBER}"/>']
    return svg(8, 8, body)


def background():
    body = _bare(48, 48, 8, WELL, 0.94, [(TEAL_DIM, 0.8, 0, 1)])
    body += cell_frame("shadow", 0, 0, 48, 48, 8, "#000000", 0.3, [])
    body.append(f'  <rect id="toolbutton-pressed-center" x="48" y="8"'
                f' width="32" height="32" fill="{AMBER}" fill-opacity="0.22"/>')
    # upstream carries these as duplicate editor ids; kept so lookups resolve
    for eid, x, y in [("shadow-topleft-2", 48, 0), ("shadow-topright-0", 56, 0),
                      ("shadow-bottomleft-9", 48, 40),
                      ("shadow-bottomright-2", 56, 40)]:
        body.append(f'  <rect id="{eid}" x="{x}" y="{y}" width="8" height="8"'
                    ' fill="#000000" fill-opacity="0.3"/>')
    body.append('  <rect id="hint-tile-center" x="0" y="0" width="1"'
                ' height="1"/>')
    return svg(80, 48, body)


def actionbutton():
    body, x = [], 0
    for size in ["16-16-", "22-22-", "24-24-", ""]:
        for state, ring in [("normal", TEAL_MID), ("hover", TEAL),
                            ("pressed", AMBER_SOFT), ("focus", AMBER)]:
            body.append(knob(f"{size}{state}", x + 12, 12, 9,
                             ring=ring, notch=False))
            x += 24
    return svg(x, 24, body, grad=True)


def action_overlays():
    def plus(cx, cy, c):
        return (f'<rect x="{cx - 5}" y="{cy - 1}" width="10" height="2" fill="{c}"/>'
                f'<rect x="{cx - 1}" y="{cy - 5}" width="2" height="10" fill="{c}"/>')

    def minus(cx, cy, c):
        return f'<rect x="{cx - 5}" y="{cy - 1}" width="10" height="2" fill="{c}"/>'

    def open_mark(cx, cy, c):
        return (f'<polyline points="{cx - 3},{cy - 5} {cx + 3},{cy} '
                f'{cx - 3},{cy + 5}" fill="none" stroke="{c}"'
                f' stroke-width="2" stroke-linecap="square"/>')

    shapes = {"add": plus, "remove": minus, "open": open_mark}
    body, x = [], 0
    for kind, draw in shapes.items():
        for state, colour in [("normal", TEAL), ("hover", TEAL_MID),
                              ("pressed", AMBER)]:
            body.append(f'  <g id="{kind}-{state}">'
                        f'<circle cx="{x + 11}" cy="11" r="9" fill="{WELL}"'
                        f' stroke="{colour}" stroke-width="1.5"/>'
                        f'{draw(x + 11, 11, colour)}</g>')
            x += 22
    return svg(x, 22, body)


def configuration_icons():
    C = TEAL

    def bars(cx, cy):
        return "".join(f'<rect x="{cx - 6}" y="{cy - 5 + i * 4}" width="12"'
                       f' height="2" fill="{C}"/>' for i in range(3))

    def gear(cx, cy):
        teeth = "".join(
            f'<rect x="{cx - 1}" y="{cy - 8}" width="2" height="4"'
            f' fill="{C}" transform="rotate({a} {cx} {cy})"/>'
            for a in range(0, 360, 45))
        return (f'{teeth}<circle cx="{cx}" cy="{cy}" r="4" fill="none"'
                f' stroke="{C}" stroke-width="2"/>')

    def arrow_pair(cx, cy, dx, dy):
        a = f'<polyline points="{cx - dx * 2 - dy * 3},{cy - dy * 2 - dx * 3} ' \
            f'{cx - dx * 6},{cy - dy * 6} ' \
            f'{cx - dx * 2 + dy * 3},{cy - dy * 2 + dx * 3}"' \
            f' fill="none" stroke="{C}" stroke-width="1.8"/>'
        b = f'<polyline points="{cx + dx * 2 - dy * 3},{cy + dy * 2 - dx * 3} ' \
            f'{cx + dx * 6},{cy + dy * 6} ' \
            f'{cx + dx * 2 + dy * 3},{cy + dy * 2 + dx * 3}"' \
            f' fill="none" stroke="{C}" stroke-width="1.8"/>'
        line_ = f'<line x1="{cx - dx * 6}" y1="{cy - dy * 6}" x2="{cx + dx * 6}"' \
                f' y2="{cy + dy * 6}" stroke="{C}" stroke-width="1.5"/>'
        return line_ + a + b

    def box(cx, cy, r, filled=False):
        fill = f'{AMBER}" fill-opacity="0.25' if filled else "none"
        return (f'<rect x="{cx - r}" y="{cy - r}" width="{r * 2}"'
                f' height="{r * 2}" fill="{fill}" stroke="{C}"'
                f' stroke-width="1.8"/>')

    def cross(cx, cy):
        return (f'<line x1="{cx - 5}" y1="{cy - 5}" x2="{cx + 5}" y2="{cy + 5}"'
                f' stroke="{C}" stroke-width="2"/>'
                f'<line x1="{cx + 5}" y1="{cy - 5}" x2="{cx - 5}" y2="{cy + 5}"'
                f' stroke="{C}" stroke-width="2"/>')

    def rotate(cx, cy):
        return (f'<path d="M {cx - 6} {cy} A 6 6 0 1 1 {cx} {cy + 6}"'
                f' fill="none" stroke="{C}" stroke-width="1.8"/>'
                f'<polyline points="{cx - 3},{cy + 3} {cx} {cy + 6} {cx - 3},{cy + 9}"'
                f' fill="none" stroke="{C}" stroke-width="1.8"/>')

    def dot(cx, cy):
        return f'<circle cx="{cx}" cy="{cy}" r="3.5" fill="{C}"/>'

    def question(cx, cy):
        return (f'<path d="M {cx - 3} {cy - 3} A 3 3 0 1 1 {cx} {cy + 1}"'
                f' fill="none" stroke="{C}" stroke-width="1.8"/>'
                f'<rect x="{cx - 1}" y="{cy + 4}" width="2" height="2"'
                f' fill="{C}"/>')

    def plus(cx, cy):
        return (f'<rect x="{cx - 6}" y="{cy - 1}" width="12" height="2" fill="{C}"/>'
                f'<rect x="{cx - 1}" y="{cy - 6}" width="2" height="12" fill="{C}"/>')

    def minus(cx, cy):
        return f'<rect x="{cx - 6}" y="{cy - 1}" width="12" height="2" fill="{C}"/>'

    def chevron_down(cx, cy):
        return (f'<polyline points="{cx - 5},{cy - 2} {cx},{cy + 3} {cx + 5},{cy - 2}"'
                f' fill="none" stroke="{C}" stroke-width="2"'
                f' stroke-linecap="square"/>')

    def back_arrow(cx, cy):
        return (f'<line x1="{cx + 6}" y1="{cy}" x2="{cx - 5}" y2="{cy}"'
                f' stroke="{C}" stroke-width="1.8"/>'
                f'<polyline points="{cx - 1},{cy - 4} {cx - 5},{cy} {cx - 1},{cy + 4}"'
                f' fill="none" stroke="{C}" stroke-width="1.8"/>')

    order = [
        ("menu", bars), ("configure", gear), ("rotate", rotate),
        ("move", lambda x, y: arrow_pair(x, y, 1, 0) + arrow_pair(x, y, 0, 1)),
        ("size-vertical", lambda x, y: arrow_pair(x, y, 0, 1)),
        ("size-horizontal", lambda x, y: arrow_pair(x, y, 1, 0)),
        ("size-diagonal-tr2bl",
         lambda x, y: f'<g transform="rotate(-45 {x} {y})">'
                      f'{arrow_pair(x, y, 1, 0)}</g>'),
        ("size-diagonal-tl2br",
         lambda x, y: f'<g transform="rotate(45 {x} {y})">'
                      f'{arrow_pair(x, y, 1, 0)}</g>'),
        ("maximize", lambda x, y: box(x, y, 7)),
        ("unmaximize", lambda x, y: box(x, y, 5)),
        ("status", dot), ("collapse", chevron_down),
        ("return-to-source", back_arrow),
        ("restore", lambda x, y: box(x, y, 6, True)),
        ("help", question), ("delete", cross), ("add", plus),
        ("remove", minus), ("close", cross),
        ("showbackground", lambda x, y: box(x, y, 7, True)),
    ]
    cell, cols = 22, 5
    body = []
    for i, (eid, draw) in enumerate(order):
        cx = (i % cols) * cell + cell // 2
        cy = (i // cols) * cell + cell // 2
        body.append(f'  <g id="{eid}">{draw(cx, cy)}</g>')
    rows = (len(order) + cols - 1) // cols
    return svg(cols * cell, rows * cell, body)


def containment_controls():
    cell = 16
    body, i = [], 0

    def place(eid, draw):
        nonlocal i
        cx = (i % 7) * cell + cell // 2
        cy = (i // 7) * cell + cell // 2
        body.append(f'  <g id="{eid}">{draw(cx, cy)}</g>')
        i += 1

    def grip(cx, cy):
        return "".join(f'<rect x="{cx - 5 + k * 4}" y="{cy - 3}" width="2"'
                       f' height="6" fill="{TEAL_DIM}"/>' for k in range(3))

    def bar(cx, cy):
        return (f'<rect x="{cx - 6}" y="{cy - 1}" width="12" height="2"'
                f' fill="{TEAL_MID}"/>')

    def handle(cx, cy):
        return (f'<rect x="{cx - 4}" y="{cy - 4}" width="8" height="8"'
                f' fill="{WELL}" stroke="{AMBER}" stroke-width="1.5"/>')

    for edge in ["south", "north", "east", "west"]:
        for part in ["center", "top", "bottom", "left", "right"]:
            eid = f"{edge}-{part}"
            if eid in ("south-left", "south-right", "north-left",
                       "north-right", "east-top", "east-bottom",
                       "west-top", "west-bottom"):
                continue
            place(eid, grip if part == "center" else bar)
        for part in ["maxslider", "offsetslider", "minslider"]:
            place(f"{edge}-{part}", handle)
    place("vertical-centerindicator", bar)
    place("horizontal-centerindicator", bar)
    rows = (i + 6) // 7
    return svg(7 * cell, rows * cell, body)


def _bare(w, h, corner, fill, opacity, rings):
    out = S.frame("X", w, h, corner, fill, fill_opacity=opacity, rings=rings)
    return [ln.replace('id="X-', 'id="') for ln in out]


ASSETS = {
    "arrows": arrows,
    "checkmarks": checkmarks,
    "radiobutton": radiobutton,
    "switch": switch,
    "slider": slider,
    "busywidget": busywidget,
    "line": line,
    "dragger": dragger,
    "picker": picker,
    "translucentbackground": translucentbackground,
    "plot-background": plot_background,
    "glowbar": glowbar,
    "margins-highlight": margins_highlight,
    "bar_meter_horizontal": lambda: bar_meter(False),
    "bar_meter_vertical": lambda: bar_meter(True),
    "media-delegate": media_delegate,
    "calendar": calendar,
    "background": background,
    "actionbutton": actionbutton,
    "action-overlays": action_overlays,
    "configuration-icons": configuration_icons,
    "containment-controls": containment_controls,
}


def main():
    for name, fn in ASSETS.items():
        (OUT / f"{name}.svg").write_text(fn(), encoding="utf-8")
        print(f"wrote {name}.svg")


if __name__ == "__main__":
    main()
