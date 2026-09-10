#!/usr/bin/env python3
"""Verify theme assets through QtSvg - the renderer Plasma actually uses.

KSvg looks an element up by id and extracts it by its bounding box, so an
element that exists but reports an empty box draws nothing. Checking with
QSvgRenderer catches that, and catches constructs a third-party rasteriser
may accept but Qt does not.

Usage:
    render_check.py <file.svg> [...]           report per-element bounds
    render_check.py --sheet out.png <file.svg> [...]   also rasterise
"""
import sys
from pathlib import Path

from PyQt6.QtCore import QRectF, Qt
from PyQt6.QtGui import QColor, QImage, QPainter
from PyQt6.QtSvg import QSvgRenderer

sys.path.insert(0, str(Path(__file__).resolve().parent))
import svgslice as S  # noqa: E402

BG = QColor("#16191a")


def check(path):
    renderer = QSvgRenderer(str(path))
    if not renderer.isValid():
        return [(path.name, "INVALID SVG", None)], []
    rows, drawable = [], []
    for eid in S.element_ids(path):
        if not renderer.elementExists(eid):
            rows.append((eid, "MISSING", None))
            continue
        box = renderer.boundsOnElement(eid)
        if box.isEmpty() or box.width() <= 0 or box.height() <= 0:
            rows.append((eid, "EMPTY BOX", box))
        else:
            rows.append((eid, "ok", box))
            drawable.append((eid, box))
    return rows, drawable


def sheet(entries, out, scale=6, cell_pad=6):
    if not entries:
        return
    cols = min(8, len(entries))
    rowc = (len(entries) + cols - 1) // cols
    cw = int(max(b.width() for _, _, b in entries) * scale) + cell_pad * 2
    ch = int(max(b.height() for _, _, b in entries) * scale) + cell_pad * 2
    img = QImage(cw * cols, ch * rowc, QImage.Format.Format_RGB32)
    img.fill(BG)
    painter = QPainter(img)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    for i, (path, eid, box) in enumerate(entries):
        r = QSvgRenderer(str(path))
        cx = (i % cols) * cw + cell_pad
        cy = (i // cols) * ch + cell_pad
        target = QRectF(cx, cy, box.width() * scale, box.height() * scale)
        r.render(painter, eid, target)
    painter.end()
    img.save(out)
    print(f"wrote {out} ({len(entries)} elements)")


def main():
    args = sys.argv[1:]
    out = None
    if args and args[0] == "--sheet":
        out, args = args[1], args[2:]
    entries, bad = [], 0
    for name in args:
        path = Path(name)
        rows, drawable = check(path)
        problems = [(e, s) for e, s, _ in rows if s != "ok"]
        bad += len(problems)
        status = "OK" if not problems else f"{len(problems)} PROBLEM(S)"
        print(f"{path.name:26} {len(rows):3} elements  {status}")
        for eid, state in problems:
            print(f"    {state:10} {eid}")
        entries += [(path, eid, box) for eid, box in drawable]
    if out:
        sheet(entries, out)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
