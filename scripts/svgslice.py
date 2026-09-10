#!/usr/bin/env python3
"""Shared 9-slice emitter for the desktoptheme generators.

FrameSvg draws each `<prefix>-<piece>` element into its own slice slot, so a
piece must cover only its own region. Emitting the whole frame under every
piece id makes the bezel render nine times per widget.
"""
import gzip
import re

PIECES = ["topleft", "top", "topright",
          "left", "center", "right",
          "bottomleft", "bottom", "bottomright"]
_GRID = [["topleft", "top", "topright"],
         ["left", "center", "right"],
         ["bottomleft", "bottom", "bottomright"]]


def num(v):
    return f"{v:g}"


def clip(rect, band):
    """Intersect a rect with a slice band; None when they do not overlap."""
    nx, ny = max(rect[0], band[0]), max(rect[1], band[1])
    nw = min(rect[0] + rect[2], band[0] + band[2]) - nx
    nh = min(rect[1] + rect[3], band[1] + band[3]) - ny
    return (nx, ny, nw, nh) if nw > 0 and nh > 0 else None


def bands(width, height, corner):
    """Yield (piece_name, (x, y, w, h)) for the nine slice regions."""
    xs = [(0, corner), (corner, width - corner), (width - corner, width)]
    ys = [(0, corner), (corner, height - corner), (height - corner, height)]
    for row, (y0, y1) in enumerate(ys):
        for col, (x0, x1) in enumerate(xs):
            yield _GRID[row][col], (x0, y0, x1 - x0, y1 - y0)


def ring_edges(width, height, inset, thickness):
    """The four edge rects of one border ring, in absolute coordinates."""
    i, t = inset, thickness
    return [(i, i, width - 2 * i, t),
            (i, height - i - t, width - 2 * i, t),
            (i, i, t, height - 2 * i),
            (width - i - t, i, t, height - 2 * i)]


def frame(prefix, width, height, corner, fill,
          fill_opacity=1, rings=(), center_fill=None):
    """Emit the nine slice groups for one frame state.

    rings: iterable of (colour, opacity, inset, thickness) border rings, each
    clipped to whichever slices it actually crosses.
    """
    out = []
    for name, band in bands(width, height, corner):
        bx, by, bw, bh = band
        paint = center_fill if (name == "center" and center_fill) else fill
        out.append(f'  <g id="{prefix}-{name}">')
        out.append(f'    <rect x="{num(bx)}" y="{num(by)}" width="{num(bw)}"'
                   f' height="{num(bh)}" fill="{paint}"'
                   f' fill-opacity="{num(fill_opacity)}"/>')
        for colour, opacity, inset, thickness in rings:
            for edge in ring_edges(width, height, inset, thickness):
                r = clip(edge, band)
                if r:
                    out.append(
                        f'    <rect x="{num(r[0])}" y="{num(r[1])}"'
                        f' width="{num(r[2])}" height="{num(r[3])}"'
                        f' fill="{colour}" fill-opacity="{num(opacity)}"/>')
        out.append('  </g>')
    return out


def read_svg(path):
    """Read a desktoptheme asset, transparently handling .svgz."""
    data = open(path, "rb").read()
    if data[:2] == b"\x1f\x8b":
        data = gzip.decompress(data)
    return data.decode("utf-8", errors="surrogateescape")


_NOISE = re.compile(
    r"^("
    # inkscape/editor artefacts, incl. the dashed-suffix forms (path1632-6)
    r"(svg|defs|grid|path|rect|g|stop|use|circle|ellipse|polygon|line|text|"
    r"tspan|image|flowRoot|flowRegion|flowPara|guide|perspective|"
    r"linearGradient|radialGradient|pattern|metadata|namedview|filter|"
    r"clip|clipPath|mask|layer|feGaussianBlur|feBlend|feColorMatrix|"
    r"feFlood|feComposite|feOffset|feMerge|feMergeNode)[\d._-]*"
    r"|Checkerboard|current-color-scheme|true|false|base"
    r"|GridFromPre046Settings|XMLID_\d+_"
    r")$")


def element_ids(path):
    """Meaningful element ids in an upstream asset, editor noise dropped."""
    ids = re.findall(r'id="([^"]*)"', read_svg(path))
    seen, out = set(), []
    for i in ids:
        if i in seen or _NOISE.match(i):
            continue
        seen.add(i)
        out.append(i)
    return out


def slice_prefixes(ids):
    """Prefixes that own a complete nine-piece set.

    A suffix match alone is not enough - prefixes are multi-word
    (`mouseover-slider-topleft`), so every sibling must be present.
    """
    have = set(ids)
    prefixes = set()
    if all(p in have for p in PIECES):
        prefixes.add("")          # unprefixed set, e.g. widgets/toolbar
    for i in ids:
        for piece in PIECES:
            if i.endswith("-" + piece):
                prefix = i[: -len(piece) - 1]
                if all(f"{prefix}-{p}" in have for p in PIECES):
                    prefixes.add(prefix)
    return sorted(prefixes)


def unclaimed(ids, prefixes):
    """Semantic ids not covered by a slice set and not a margin hint.

    Plasma falls back per file, not per element: if an asset exists but omits
    an element the widget asks for, that part draws as nothing. So a widget is
    only safe to ship once every one of these is accounted for.
    """
    covered = {f"{p}-{q}" if p else q for p in prefixes for q in PIECES}
    return [i for i in ids if i not in covered and "hint" not in i]


def hint_elements(path):
    """Verbatim `<rect id="...hint...">` lines, geometry preserved.

    Hints encode margins the widget code relies on, and some are per-prefix
    (`base-hint-left-margin`), so they are copied rather than invented.
    """
    text = read_svg(path)
    out = []
    for m in re.finditer(r'<rect[^>]*id="([^"]*hint[^"]*)"[^>]*/?>', text):
        tag, name = m.group(0), m.group(1)
        attrs = dict(re.findall(r'(\w[\w-]*)="([^"]*)"', tag))
        geom = " ".join(
            f'{k}="{attrs[k]}"' for k in ("x", "y", "width", "height")
            if k in attrs)
        out.append(f'  <rect id="{name}" {geom}/>')
    return out
