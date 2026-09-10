#!/usr/bin/env python3
"""Generate icons/RetroDIN: breeze-dark recoloured to the DIN palette.

Breeze icons carry a `current-color-scheme` <style> block whose colour the
paths reference through fill:currentColor, so rewriting that one declaration
restyles the whole glyph. Icons without the block are hand-drawn colour art
(app logos, mimetypes) and are copied through untouched so they stay
recognisable.

The output is ~43MB and fully reproducible, so it is generated rather than
committed. Hand-authored overrides live in icons/RetroDIN-src and are
layered on last. Run before scripts/install.sh.
"""
import re
import shutil
import sys
from pathlib import Path

BASE = Path(sys.argv[1] if len(sys.argv) > 1 else "/usr/share/icons/breeze-dark")
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "icons/RetroDIN"
SRC = ROOT / "icons/RetroDIN-src"

# breeze semantic colour -> DIN palette. Amber carries both warning tiers, per
# the spec's "keep amber, stay consistent" decision; no red is introduced.
COLORS = {
    "#fcfcfc": "#5eead4", "#f2f2f2": "#5eead4",             # Text
    "#3daee9": "#14b8a6", "#3498db": "#14b8a6",             # Accent
    "#3DAEE6": "#14b8a6", "#3593e6": "#14b8a6",
    "#da4453": "#ffb454", "#e74c3c": "#ffb454",             # NegativeText
    "#ff4747": "#ffb454",
    "#27ae60": "#2fd4bf",                                    # PositiveText
    "#f67400": "#ffd08a",                                    # NeutralText
    "#2a2e32": "#16191a",                                    # Background
    "#31363b": "#0a2e29", "#7B7C7E": "#0a2e29",             # ButtonText
}
STYLE = re.compile(r'(<style[^>]*id="current-color-scheme"[^>]*>)(.*?)(</style>)',
                   re.DOTALL)


def recolor(block):
    for old, new in COLORS.items():
        block = re.sub(re.escape(old), new, block, flags=re.IGNORECASE)
    return block


def write_index():
    """Keep breeze's Directories list - it is what makes every context
    resolvable - but retitle the theme and append our own scalable dir."""
    index = (OUT / "index.theme").read_text(encoding="utf-8")
    index = re.sub(r"^Name(\[[^\]]*\])?=.*$\n?", "", index, flags=re.MULTILINE)
    index = re.sub(r"^Comment(\[[^\]]*\])?=.*$\n?", "", index, flags=re.MULTILINE)
    index = re.sub(r"^Inherits=.*$", "Inherits=breeze-dark,hicolor",
                   index, flags=re.MULTILINE)
    index = re.sub(r"^Directories=(.*)$", r"Directories=\1,places/scalable",
                   index, flags=re.MULTILINE)
    index = index.replace(
        "[Icon Theme]",
        "[Icon Theme]\nName=Retro DIN\n"
        "Comment=90s car-stereo/hi-fi DIN unit icons", 1)
    index = index.rstrip() + (
        "\n\n[places/scalable]\nSize=48\nMinSize=16\nMaxSize=512\n"
        "Type=Scalable\nContext=Places\n")
    (OUT / "index.theme").write_text(index, encoding="utf-8")
    if "Directories=" not in index or "places/scalable" not in index:
        sys.exit("index.theme rewrite lost its Directories list")


def overlay_src():
    for item in SRC.rglob("*"):
        if item.is_dir() or item.name == "index.theme":
            continue
        dest = OUT / item.relative_to(SRC)
        dest.parent.mkdir(parents=True, exist_ok=True)
        if dest.exists() or dest.is_symlink():
            dest.unlink()
        if item.is_symlink():
            dest.symlink_to(item.readlink())
        else:
            shutil.copy2(item, dest)


def main():
    if not BASE.is_dir():
        sys.exit(f"base icon theme not found: {BASE}")
    if OUT.exists():
        shutil.rmtree(OUT)
    shutil.copytree(BASE, OUT, symlinks=True)

    touched = 0
    for path in OUT.rglob("*.svg"):
        if path.is_symlink():
            continue
        text = path.read_text(encoding="utf-8", errors="surrogateescape")
        if 'id="current-color-scheme"' not in text:
            continue
        new = STYLE.sub(lambda m: m.group(1) + recolor(m.group(2)) + m.group(3), text)
        if new != text:
            path.write_text(new, encoding="utf-8", errors="surrogateescape")
            touched += 1

    write_index()
    overlay_src()
    print(f"recoloured {touched} icons -> {OUT}")


if __name__ == "__main__":
    main()
