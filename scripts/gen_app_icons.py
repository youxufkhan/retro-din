#!/usr/bin/env python3
"""Author DIN app icons for every application installed on this machine.

App icons are identity marks rather than a parametric family, so they cannot
be derived the way battery levels can. What makes them tractable is that the
system only references ~75 distinct app icon names, and nearly all of the
.desktop files carry a Categories= line that says what kind of program it is.
So each name is mapped to one of a small set of DIN archetypes - by explicit
override where the app is well known, by category otherwise, and to a plain
tile when neither says anything useful.

Icons are drawn as monochrome teal line art. That is a deliberate trade: it
matches the theme and loses brand colour, which is what makes Chrome instantly
findable. Reverting is a one-line icon-theme change, and individual apps can
be exempted by adding them to EXEMPT.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "icons/RetroDIN-src"
SIZES = ["16", "22", "24", "32", "48", "64"]

TEAL = "#5eead4"
TEAL_DIM = "#1d6b60"
AMBER = "#ffb454"
WELL = "#001210"

C = 48  # design canvas
SW = 2.4

# app icon names to keep as the application ships them
EXEMPT: set[str] = set()

DESKTOP_DIRS = [Path("/usr/share/applications"),
                Path.home() / ".local/share/applications",
                Path("/var/lib/snapd/desktop/applications"),
                Path("/var/lib/flatpak/exports/share/applications")]


def wrap(body):
    return ("".join([
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{C}" height="{C}"'
        f' viewBox="0 0 {C} {C}">', body, '</svg>'])) + "\n"


def p(d, colour=TEAL, sw=SW, fill="none"):
    return (f'<path d="{d}" fill="{fill}" stroke="{colour}"'
            f' stroke-width="{sw}" stroke-linecap="square"'
            f' stroke-linejoin="miter"/>')


def r(x, y, w, h, colour=TEAL, sw=SW, fill="none", rx=0):
    rr = f' rx="{rx}"' if rx else ""
    return (f'<rect x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}"'
            f' fill="{fill}" stroke="{colour}" stroke-width="{sw}"{rr}/>')


def solid(x, y, w, h, colour=TEAL, op=1):
    return (f'<rect x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}"'
            f' fill="{colour}" fill-opacity="{op:g}"/>')


def circ(cx, cy, rad, colour=TEAL, sw=SW, fill="none"):
    return (f'<circle cx="{cx:g}" cy="{cy:g}" r="{rad:g}" fill="{fill}"'
            f' stroke="{colour}" stroke-width="{sw}"/>')


def tile(body, accent=TEAL_DIM):
    """Every app icon sits in the same DIN faceplate."""
    return (r(4, 4, 40, 40, accent, 2, rx=3) + body)


# ------------------------------------------------------------- archetypes

def browser():
    # the meridian must stay inside the globe, so its rx is under the radius
    return tile(circ(24, 24, 13) + p("M 11 24 H 37")
                + p("M 24 11 A 7 13 0 0 1 24 37 A 7 13 0 0 1 24 11"))


def terminal():
    return tile(p("M 14 19 L 20 24 L 14 29") + solid(23, 27, 11, 2.4))


def code():
    return tile(p("M 18 17 L 11 24 L 18 31") + p("M 30 17 L 37 24 L 30 31")
                + p("M 27 15 L 21 33", AMBER, 2))


def editor():
    return tile(p("M 16 12 H 28 L 33 17 V 36 H 16 Z")
                + p("M 20 22 H 29", TEAL_DIM, 2)
                + p("M 20 27 H 29", TEAL_DIM, 2)
                + p("M 28 12 V 17 H 33", TEAL_DIM, 2))


def folder():
    return tile(p("M 12 18 H 21 L 24 21 H 36 V 34 H 12 Z"))


def gear():
    teeth = "".join(solid(22.8, 9, 2.4, 6, TEAL) if a == 0 else
                    f'<g transform="rotate({a} 24 24)">'
                    f'{solid(22.8, 9, 2.4, 6, TEAL)}</g>'
                    for a in range(0, 360, 45))
    return tile(teeth + circ(24, 24, 8) + circ(24, 24, 3, TEAL_DIM, 2))


def sliders():
    out = []
    for i, y in enumerate([16, 24, 32]):
        out.append(solid(12, y - 1, 24, 2, TEAL_DIM))
        out.append(solid(16 + i * 7, y - 4, 3, 8, TEAL))
    return tile("".join(out))


def spreadsheet():
    out = [r(12, 13, 24, 22, TEAL, 2), solid(12, 13, 24, 5, TEAL, 0.5)]
    for x in [20, 28]:
        out.append(solid(x, 13, 1.6, 22, TEAL_DIM))
    for y in [23, 29]:
        out.append(solid(12, y, 24, 1.6, TEAL_DIM))
    return tile("".join(out))


def document():
    out = [p("M 15 11 H 28 L 34 17 V 37 H 15 Z"),
           p("M 28 11 V 17 H 34", TEAL_DIM, 2)]
    for y in [22, 26, 30]:
        out.append(solid(19, y, 11, 1.8, TEAL_DIM))
    return tile("".join(out))


def presentation():
    return tile(r(11, 13, 26, 18, TEAL, 2) + solid(24, 31, 1.8, 5, TEAL_DIM)
                + solid(16, 22, 3, 6, TEAL) + solid(22, 18, 3, 10, TEAL)
                + solid(28, 24, 3, 4, AMBER))


def math():
    return tile(p("M 32 14 H 17 L 26 24 L 17 34 H 32", TEAL, 2.6))


def image():
    return tile(r(11, 14, 26, 20, TEAL, 2) + circ(18, 21, 2.6, AMBER, 2)
                + p("M 13 32 L 21 24 L 28 30 L 32 26 L 35 30", TEAL, 2))


def video():
    return tile(r(11, 15, 26, 18, TEAL, 2)
                + p("M 21 21 L 30 24 L 21 27 Z", TEAL, 1.6, fill=TEAL))


def audio():
    return tile(circ(19, 32, 4) + solid(22.6, 14, 2.4, 18, TEAL)
                + p("M 25 14 L 34 17", TEAL, 2.4))


def game():
    pips = "".join(circ(x, y, 1.8, TEAL, 1, fill=TEAL)
                   for x, y in [(18, 18), (30, 18), (24, 24),
                                (18, 30), (30, 30)])
    return tile(r(13, 13, 22, 22, TEAL, 2, rx=3) + pips)


def chat():
    return tile(p("M 12 15 H 36 V 30 H 22 L 15 36 V 30 H 12 Z"))


def archive():
    return tile(r(11, 15, 26, 20, TEAL, 2) + solid(11, 22, 26, 2, TEAL_DIM)
                + solid(21, 15, 6, 7, AMBER, 0.8))


def calculator():
    keys = "".join(solid(15 + c * 6, 24 + rw * 5, 4, 3, TEAL_DIM)
                   for rw in range(3) for c in range(3))
    return tile(r(13, 11, 22, 26, TEAL, 2, rx=2)
                + solid(16, 15, 16, 6, TEAL, 0.35) + keys)


def monitor_graph():
    return tile(r(11, 14, 26, 20, TEAL, 2)
                + p("M 14 29 L 19 22 L 24 26 L 29 18 L 34 24", AMBER, 2))


def package():
    return tile(p("M 24 11 L 36 17 V 31 L 24 37 L 12 31 V 17 Z")
                + p("M 12 17 L 24 23 L 36 17", TEAL_DIM, 2)
                + solid(22.8, 23, 2.4, 14, TEAL_DIM))


def security():
    return tile(p("M 24 11 L 35 15 V 25 A 13 13 0 0 1 24 37"
                  " A 13 13 0 0 1 13 25 V 15 Z")
                + circ(24, 22, 3, AMBER, 2) + solid(22.8, 24, 2.4, 6, AMBER))


def book():
    return tile(p("M 24 15 V 35") + p("M 24 15 C 20 12 15 12 12 14 V 32"
                                      " C 15 30 20 30 24 33")
                + p("M 24 15 C 28 12 33 12 36 14 V 32"
                    " C 33 30 28 30 24 33"))


def scanner():
    return tile(r(11, 24, 26, 10, TEAL, 2, rx=2)
                + solid(15, 28, 18, 2, TEAL_DIM)
                + p("M 16 20 H 32", AMBER, 2.4)
                + p("M 20 14 H 28", TEAL_DIM, 2))


def network():
    return tile(circ(24, 14, 3.4) + circ(14, 33, 3.4) + circ(34, 33, 3.4)
                + p("M 24 17 L 15 30", TEAL_DIM, 2)
                + p("M 24 17 L 33 30", TEAL_DIM, 2)
                + p("M 17 33 H 31", TEAL_DIM, 2))


def disk():
    return tile(circ(24, 24, 13) + circ(24, 24, 4, TEAL_DIM, 2)
                + p("M 24 11 A 13 13 0 0 1 37 24", AMBER, 2.4))


def bug():
    return tile(circ(24, 25, 8) + p("M 18 15 L 21 20", TEAL_DIM, 2)
                + p("M 30 15 L 27 20", TEAL_DIM, 2)
                + p("M 13 25 H 16", TEAL_DIM, 2) + p("M 32 25 H 35", TEAL_DIM, 2)
                + p("M 15 33 L 18 30", TEAL_DIM, 2)
                + p("M 33 33 L 30 30", TEAL_DIM, 2))


def emoji():
    return tile(circ(24, 24, 13) + circ(19, 20, 1.6, TEAL, 1, fill=TEAL)
                + circ(29, 20, 1.6, TEAL, 1, fill=TEAL)
                + p("M 17 28 A 8 8 0 0 0 31 28", AMBER, 2))


def keyboard():
    keys = "".join(solid(13 + c * 5, 21 + rw * 5, 3.4, 2.6, TEAL_DIM)
                   for rw in range(2) for c in range(5))
    return tile(r(10, 17, 28, 15, TEAL, 2, rx=2) + keys
                + solid(18, 27, 12, 2.6, TEAL))


def email():
    return tile(r(11, 16, 26, 18, TEAL, 2)
                + p("M 11 16 L 24 27 L 37 16", TEAL, 2))


def plain():
    return tile(solid(18, 18, 12, 12, TEAL_DIM, 0.8)
                + solid(21, 21, 6, 6, TEAL))


ARCHETYPES = {
    "browser": browser, "terminal": terminal, "code": code, "editor": editor,
    "folder": folder, "gear": gear, "sliders": sliders,
    "spreadsheet": spreadsheet, "document": document,
    "presentation": presentation, "math": math, "image": image,
    "video": video, "audio": audio, "game": game, "chat": chat,
    "archive": archive, "calculator": calculator, "monitor": monitor_graph,
    "package": package, "security": security, "book": book,
    "scanner": scanner, "network": network, "disk": disk, "bug": bug,
    "emoji": emoji, "keyboard": keyboard, "email": email,
    "plain": plain,
}

# where the category line is absent, wrong, or too generic to be useful
OVERRIDES = {
    "google-chrome": "browser", "vscode": "code", "gvim": "code",
    "kate": "editor", "obsidian": "document", "koodo-reader": "book",
    "discord": "chat", "teams-for-linux": "chat", "org.kde.neochat": "chat",
    "claude-desktop": "chat", "vlc": "video", "haruna": "video",
    "youtube-music": "audio", "elisa": "audio", "okular": "book",
    "gwenview": "image", "spectacle": "image", "skanpage": "scanner",
    "org.kde.dolphin": "folder", "utilities-terminal": "terminal",
    "dev.warp.Warp": "terminal", "htop": "monitor",
    "utilities-system-monitor": "monitor", "utilities-log-viewer": "monitor",
    "filelight": "disk", "org.kde.isoimagewriter": "disk",
    "usb-creator-kde": "disk", "partitionmanager": "disk",
    "ark": "archive", "accessories-calculator": "calculator",
    "kwalletmanager": "security", "zero-trust-orange": "security",
    "preferences-system": "gear", "kmenuedit": "sliders",
    "kvantum": "sliders", "applications-other": "package",
    "kubuntu-manage-software": "package", "plasmadiscover": "package",
    "synaptic": "package", "calamares": "disk", "bleachbit": "package",
    "apport": "bug", "tools-report-bug": "bug",
    "preferences-desktop-emoticons": "emoji",
    "input-keyboard": "keyboard", "keyboard-layout": "keyboard",
    "accessories-character-map": "keyboard",
    "kdeconnect": "network", "org.remmina.Remmina": "network",
    "apidog": "network", "help-browser": "book", "kubuntu-web-link": "book",
    "dialog-information": "book", "hwinfo": "monitor",
    "libreoffice-calc": "spreadsheet", "libreoffice-writer": "document",
    "libreoffice-impress": "presentation", "libreoffice-math": "math",
    "libreoffice-draw": "image", "libreoffice-startcenter": "document",
    "org.kde.qrca": "image", "display-im7.q16": "image",
    "emblem-system-symbolic": "gear", "jockey": "gear",
    "preferences-desktop-tablet": "sliders",
    "preferences-desktop-notification": "sliders",
    "preferences-system-bluetooth": "network",
    "start-here-kde-plasma": "book", "unsloth-studio": "code",
    "OpenWork-Dev": "code", "internet-web-browser-symbolic": "browser",
}

# Categories= keyword -> archetype, first match wins
CATEGORY_RULES = [
    ("Email", "email"), ("WebBrowser", "browser"), ("TerminalEmulator", "terminal"),
    ("IDE", "code"), ("Development", "code"), ("TextEditor", "editor"),
    ("FileManager", "folder"), ("Spreadsheet", "spreadsheet"),
    ("WordProcessor", "document"), ("Presentation", "presentation"),
    ("Math", "math"), ("Calculator", "calculator"),
    ("InstantMessaging", "chat"), ("Chat", "chat"),
    ("Player", "video"), ("Video", "video"), ("AudioVideo", "video"),
    ("Audio", "audio"), ("Photography", "image"), ("Viewer", "image"),
    ("Graphics", "image"), ("Game", "game"), ("Archiving", "archive"),
    ("Monitor", "monitor"), ("PackageManager", "package"),
    ("Security", "security"), ("Documentation", "book"),
    ("Scanning", "scanner"), ("Network", "network"),
    ("Filesystem", "disk"), ("HardwareSettings", "sliders"),
    ("DesktopSettings", "sliders"), ("Settings", "gear"),
    ("System", "gear"), ("Office", "document"), ("Utility", "plain"),
]


EXTRA_NAMES = {
    "firefox": "browser", "firefox_firefox": "browser",
    "thunderbird": "email", "thunderbird_thunderbird": "email",
    "chromium": "browser", "brave-browser": "browser",
    "code": "code", "codium": "code", "sublime_text": "editor",
    "telegram": "chat", "signal-desktop": "chat", "slack": "chat",
    "spotify": "audio", "mpv": "video", "gimp": "image",
    "inkscape": "image", "blender": "image", "steam": "game",
    "virtualbox": "package", "docker": "package", "postman": "network",
    "thunar": "folder", "nautilus": "folder", "nemo": "folder",
    "libreoffice-base": "spreadsheet", "evince": "book", "zathura": "book",
}


def scan_desktop_files():
    found = {}
    for d in DESKTOP_DIRS:
        if not d.is_dir():
            continue
        for f in d.glob("*.desktop"):
            try:
                text = f.read_text(errors="replace")
            except OSError:
                continue
            if "NoDisplay=true" in text:
                continue
            icon = re.search(r"^Icon=(.+)$", text, re.M)
            cats = re.search(r"^Categories=(.+)$", text, re.M)
            if not icon:
                continue
            name = icon.group(1).strip()
            if name.startswith("/") or "/" in name:
                continue
            found.setdefault(name, cats.group(1) if cats else "")
    return found


def classify(name, categories):
    if name in OVERRIDES:
        return OVERRIDES[name]
    for keyword, arch in CATEGORY_RULES:
        if keyword in categories:
            return arch
    return "plain"


def main():
    apps = scan_desktop_files()
    chosen = {n: classify(n, c) for n, c in apps.items() if n not in EXEMPT}
    for name, arch in EXTRA_NAMES.items():
        chosen.setdefault(name, arch)
    written = 0
    for size in SIZES:
        d = SRC / "apps" / size
        d.mkdir(parents=True, exist_ok=True)
        for name, arch in chosen.items():
            (d / f"{name}.svg").write_text(wrap(ARCHETYPES[arch]()),
                                           encoding="utf-8")
            written += 1
    used = {}
    for arch in chosen.values():
        used[arch] = used.get(arch, 0) + 1
    print(f"{len(chosen)} app icons -> {written} files across "
          f"{len(SIZES)} sizes")
    print("archetype use:", ", ".join(
        f"{k}={v}" for k, v in sorted(used.items(), key=lambda kv: -kv[1])))
    plain = [n for n, a in chosen.items() if a == "plain"]
    if plain:
        print(f"fell back to plain tile ({len(plain)}): {', '.join(sorted(plain))}")


if __name__ == "__main__":
    main()
