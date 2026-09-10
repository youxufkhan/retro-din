#!/usr/bin/env python3
"""Emit widgets/tasks.svg with correct 9-slice geometry.

Each <state>-<piece> element must cover ONLY its own slice region. Emitting the
whole button per piece makes FrameSvg draw the full bezel nine times per
button, stacked into the corner/edge/center regions.
"""

W, H, C = 64, 48, 8

BANDS_X = [(0, C), (C, W - C), (W - C, W)]
BANDS_Y = [(0, C), (C, H - C), (H - C, H)]
NAMES = [["topleft", "top", "topright"],
         ["left", "center", "right"],
         ["bottomleft", "bottom", "bottomright"]]

# state -> (fill_opacity, [(color, opacity, inset, width)], animate_rings)
STATES = {
    "normal":     (1.0,  [("#1d6b60", 1.0, 0, 1)],                              False),
    "hover":      (1.0,  [("#2fd4bf", 1.0, 0, 1.5)],                            False),
    "focus":      (1.0,  [("#ffb454", 1.0, 0, 2), ("#ffb454", 0.35, 2, 1)],     False),
    "attention":  (1.0,  [("#ffd08a", 1.0, 0, 2)],                              True),
    "minimized":  (0.45, [("#1d6b60", 0.5, 0, 1)],                              False),
    "progress":   (1.0,  [("#2fd4bf", 1.0, 0, 1.5)],                            False),
}

ORIENTATIONS = ["north-", "east-", "west-"]


def clip(rect, band):
    (x, y, w, h), (bx, by, bw, bh) = rect, band
    nx, ny = max(x, bx), max(y, by)
    nw, nh = min(x + w, bx + bw) - nx, min(y + h, by + bh) - ny
    return (nx, ny, nw, nh) if nw > 0 and nh > 0 else None


def ring_edges(color, opacity, i, w):
    return [(i, i, W - 2 * i, w),
            (i, H - i - w, W - 2 * i, w),
            (i, i, w, H - 2 * i),
            (W - i - w, i, w, H - 2 * i)]


def num(v):
    return f"{v:g}"


def emit_slice(state, name, band, fill_opacity, rings, animate):
    bx, by, bw, bh = band
    out = [f'  <g id="{state}-{name}">',
           f'    <rect x="{num(bx)}" y="{num(by)}" width="{num(bw)}" height="{num(bh)}"'
           f' fill="url(#btngrad)" fill-opacity="{num(fill_opacity)}"/>']
    for color, opacity, inset, width in rings:
        for edge in ring_edges(color, opacity, inset, width):
            r = clip(edge, band)
            if not r:
                continue
            body = (f'<rect x="{num(r[0])}" y="{num(r[1])}" width="{num(r[2])}"'
                    f' height="{num(r[3])}" fill="{color}" fill-opacity="{num(opacity)}"')
            if animate:
                out.append(f'    {body}>')
                out.append('      <animate attributeName="fill-opacity"'
                           ' values="1;0.35;1" dur="1s" repeatCount="indefinite"/>')
                out.append('    </rect>')
            else:
                out.append(f'    {body}/>')
    out.append('  </g>')
    return out


def main():
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"'
        f' width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
        '  <defs>',
        f'    <linearGradient id="btngrad" gradientUnits="userSpaceOnUse"'
        f' x1="0" y1="0" x2="0" y2="{H}">',
        '      <stop offset="0" stop-color="#333a3c"/>',
        '      <stop offset="1" stop-color="#191d1e"/>',
        '    </linearGradient>',
        '  </defs>',
    ]
    for state, (fill_opacity, rings, animate) in STATES.items():
        for row, (by, by2) in enumerate(BANDS_Y):
            for col, (bx, bx2) in enumerate(BANDS_X):
                band = (bx, by, bx2 - bx, by2 - by)
                lines += emit_slice(state, NAMES[row][col], band,
                                    fill_opacity, rings, animate)
        for orient in ORIENTATIONS:
            for row in NAMES:
                for name in row:
                    lines.append(f'  <use id="{orient}{state}-{name}"'
                                 f' xlink:href="#{state}-{name}"/>')
    # Margin hints must be explicit. Without them FrameSvg derives margins
    # from the corner artwork - 8px of a 48px button per edge - which leaves
    # the icon only a third of the height. 2px keeps the bezel readable while
    # giving the icon nearly the whole button.
    M = 2
    prefixes = [f"{o}{s}" for s in STATES for o in ("",) + tuple(ORIENTATIONS)]
    for prefix in prefixes:
        lines += [
            f'  <rect id="{prefix}-hint-top-margin" x="0" y="0"'
            f' width="{M}" height="{M}"/>',
            f'  <rect id="{prefix}-hint-bottom-margin" x="0" y="{H - M}"'
            f' width="{M}" height="{M}"/>',
            f'  <rect id="{prefix}-hint-left-margin" x="0" y="0"'
            f' width="{M}" height="{M}"/>',
            f'  <rect id="{prefix}-hint-right-margin" x="{W - M}" y="0"'
            f' width="{M}" height="{M}"/>',
        ]
    lines += [
        f'  <rect id="hint-top-margin" x="0" y="0" width="{M}" height="{M}"/>',
        f'  <rect id="hint-bottom-margin" x="0" y="{H - M}"'
        f' width="{M}" height="{M}"/>',
        f'  <rect id="hint-left-margin" x="0" y="0" width="{M}" height="{M}"/>',
        f'  <rect id="hint-right-margin" x="{W - M}" y="0"'
        f' width="{M}" height="{M}"/>',
    ]

    # grouped-task expander marks, one per panel edge
    for edge, pts in [("top", "3,7 6,3 9,7"), ("bottom", "3,3 6,7 9,3"),
                      ("left", "7,3 3,6 7,9"), ("right", "3,3 7,6 3,9")]:
        lines.append(f'  <polyline id="group-expander-{edge}"'
                     f' points="{pts}" fill="none" stroke="#5eead4"'
                     f' stroke-width="1.5" stroke-linecap="square"/>')
    lines.append('</svg>')
    print("\n".join(lines))


if __name__ == "__main__":
    main()
