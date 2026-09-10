#!/usr/bin/env python3
"""Author DIN status/tray icons, including the parametric families.

Breeze ships ~826 status names at 22px alone, most of them members of a
family that varies by one number: battery charge, signal strength, volume
step. Those are generated rather than drawn, which is both cheaper and more
consistent than hand-authoring each step.

Output goes to icons/RetroDIN-src, which gen_icons.py overlays last so
these win over the recoloured breeze fallback. Every icon also gets its
`-symbolic` (and where breeze has one, `-rtl`) alias as a symlink, because
applets ask for whichever spelling they were written against.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "icons/RetroDIN-src"
SIZES = ["16", "22", "24", "32"]

TEAL = "#5eead4"
TEAL_DIM = "#1d6b60"
AMBER = "#ffb454"
DANGER = "#ff8a5c"
OFF = "#0a2e29"

S = 22  # design canvas; the same art is installed at every listed size


def wrap(body):
    return ("".join([
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{S}" height="{S}"'
        f' viewBox="0 0 {S} {S}">',
        body, '</svg>'])) + "\n"


def rect(x, y, w, h, fill, op=1, rx=0):
    r = f' rx="{rx}"' if rx else ""
    return (f'<rect x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}"'
            f' fill="{fill}" fill-opacity="{op:g}"{r}/>')


def stroke_rect(x, y, w, h, colour, sw=1.6, rx=0):
    r = f' rx="{rx}"' if rx else ""
    return (f'<rect x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}"'
            f' fill="none" stroke="{colour}" stroke-width="{sw}"{r}/>')


def path(d, colour, sw=1.6, fill="none"):
    return (f'<path d="{d}" fill="{fill}" stroke="{colour}"'
            f' stroke-width="{sw}" stroke-linecap="square"/>')


def circle(cx, cy, r, fill="none", stroke=None, sw=1.6, op=1):
    s = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
    return (f'<circle cx="{cx:g}" cy="{cy:g}" r="{r:g}" fill="{fill}"'
            f' fill-opacity="{op:g}"{s}/>')


def slash():
    return path("M 4 18 L 18 4", DANGER, 2)


# ------------------------------------------------------------------ families

def battery_body(level, charging=False, profile=None, missing=False):
    out = [stroke_rect(3, 6, 14, 11, TEAL_DIM, 1.6, 1),
           rect(17, 9, 2, 5, TEAL_DIM, 1, 1)]
    if missing:
        out.append(slash())
        return "".join(out)
    fillw = max(0, min(12, round(12 * level / 100)))
    colour = TEAL if level > 20 else (AMBER if level > 10 else DANGER)
    if fillw:
        out.append(rect(4, 7, fillw, 9, colour))
    if charging:
        out.append(path("M 11 7 L 8 12 L 11 12 L 9 16", AMBER, 1.8))
    if profile == "performance":
        out.append(path("M 6 12 L 9 9 L 12 12", AMBER, 1.4))
    elif profile == "powersave":
        out.append(rect(7, 11, 6, 1.4, AMBER))
    elif profile == "balanced":
        out.append(circle(10, 11.5, 1.6, AMBER))
    return "".join(out)


def batteries():
    icons = {}
    names = {"000": 0, "010": 10, "020": 20, "030": 30, "040": 40, "050": 50,
             "060": 60, "070": 70, "080": 80, "090": 90, "100": 100}
    for tag, lvl in names.items():
        for charging in (False, True):
            base = f"battery-{tag}" + ("-charging" if charging else "")
            icons[base] = battery_body(lvl, charging)
            for prof in ("balanced", "performance", "powersave"):
                icons[f"{base}-profile-{prof}"] = battery_body(
                    lvl, charging, prof)
    for tag, lvl in [("empty", 0), ("caution", 10), ("low", 20),
                     ("good", 70), ("full", 100)]:
        icons[f"battery-{tag}"] = battery_body(lvl)
        icons[f"battery-{tag}-charging"] = battery_body(lvl, charging=True)
    icons["battery-missing"] = battery_body(0, missing=True)
    for prof in ("balanced", "performance", "powersave"):
        icons[f"battery-profile-{prof}"] = battery_body(60, profile=prof)
    return icons


def wireless_body(level, overlay=None):
    out = []
    for i, r in enumerate([4, 7.5, 11]):
        lit = level >= (i + 1) * 30
        out.append(path(f"M {11 - r} 15 A {r} {r} 0 0 1 {11 + r} 15",
                        TEAL if lit else OFF, 1.8))
    out.append(circle(11, 16, 1.6, TEAL if level > 0 else OFF))
    if overlay == "locked":
        out.append(rect(14, 13, 5, 5, AMBER, 1, 1))
    elif overlay == "limited":
        out.append(rect(15, 14, 4, 1.6, AMBER))
    elif overlay == "off":
        out.append(slash())
    return "".join(out)


def wireless():
    icons = {}
    for lvl in [0, 20, 40, 60, 80, 100]:
        icons[f"network-wireless-{lvl}"] = wireless_body(lvl)
        icons[f"network-wireless-{lvl}-locked"] = wireless_body(lvl, "locked")
        icons[f"network-wireless-{lvl}-limited"] = wireless_body(lvl, "limited")
        icons[f"network-wireless-connected-{lvl}"] = wireless_body(lvl)
        icons[f"nm-signal-{lvl}"] = wireless_body(lvl)
    for tag, lvl in [("none", 0), ("weak", 25), ("ok", 50),
                     ("good", 75), ("excellent", 100)]:
        icons[f"network-wireless-signal-{tag}"] = wireless_body(lvl)
    icons["network-wireless-on"] = wireless_body(100)
    icons["network-wireless-available"] = wireless_body(60)
    icons["network-wireless-acquiring"] = wireless_body(40)
    icons["network-wireless-off"] = wireless_body(0, "off")
    icons["network-wireless-disconnected"] = wireless_body(0, "off")
    icons["nm-no-connection"] = wireless_body(0, "off")
    for lvl in [0, 25, 50, 75, 100]:
        icons[f"network-wireless-connected-{lvl:02d}"] = wireless_body(lvl)
    return icons


def mobile_body(level, locked=False, off=False):
    out = []
    for i in range(4):
        h = 4 + i * 3
        lit = level >= (i + 1) * 25
        out.append(rect(3 + i * 4, 18 - h, 3, h, TEAL if lit else OFF))
    if locked:
        out.append(rect(16, 12, 5, 5, AMBER, 1, 1))
    if off:
        out.append(slash())
    return "".join(out)


def mobile():
    icons, techs = {}, ["", "-edge", "-gprs", "-hsdpa", "-hspa", "-hsupa",
                        "-lte", "-umts", "-5g"]
    for lvl in [0, 20, 40, 60, 80, 100]:
        for tech in techs:
            icons[f"network-mobile-{lvl}{tech}"] = mobile_body(lvl)
            icons[f"network-mobile-{lvl}{tech}-locked"] = mobile_body(lvl, True)
    icons["network-mobile-on"] = mobile_body(100)
    icons["network-mobile-off"] = mobile_body(0, off=True)
    icons["network-mobile-available"] = mobile_body(60)
    return icons


def volume_body(level, muted=False, warn=None):
    cone = path("M 4 9 L 8 9 L 12 5 L 12 17 L 8 13 L 4 13 Z",
                TEAL, 1.6, fill=TEAL)
    out = [cone]
    waves = [(14.5, 3.5), (17, 6.5), (19.5, 9.5)]
    lit = {"muted": 0, "low": 1, "medium": 2, "high": 3}[level]
    for i, (x, r) in enumerate(waves):
        colour = (warn or TEAL) if i < lit else OFF
        out.append(path(f"M {x} {11 - r} A {r} {r} 0 0 1 {x} {11 + r}",
                        colour, 1.6))
    if muted:
        out.append(slash())
    return "".join(out)


def volumes():
    icons = {}
    for tag in ["muted", "low", "medium", "high"]:
        icons[f"audio-volume-{tag}"] = volume_body(tag, muted=(tag == "muted"))
    icons["audio-volume-high-warning"] = volume_body("high", warn=AMBER)
    icons["audio-volume-high-danger"] = volume_body("high", warn=DANGER)
    icons["audio-off"] = volume_body("muted", muted=True)
    icons["audio-on"] = volume_body("high")
    icons["audio-ready"] = volume_body("medium")
    for tag in ["muted", "low", "medium", "high"]:
        icons[f"microphone-sensitivity-{tag}"] = mic_body(tag)
    icons["mic-off"] = mic_body("muted")
    icons["mic-on"] = mic_body("high")
    icons["mic-ready"] = mic_body("medium")
    return icons


def mic_body(level):
    out = [rect(9, 3, 4, 9, TEAL, 1, 2),
           path("M 6 11 A 5 5 0 0 0 16 11", TEAL, 1.6),
           rect(10.2, 16, 1.6, 3, TEAL)]
    if level == "muted":
        out.append(slash())
    return "".join(out)


def simple():
    """Singletons: one drawn glyph each."""
    disc = lambda c: circle(11, 11, 8, "none", c, 1.8)  # noqa: E731
    return {
        "media-playback-playing": path("M 8 5 L 17 11 L 8 17 Z", TEAL, 1.6,
                                       fill=TEAL),
        "media-playback-paused": rect(7, 5, 3, 12, TEAL) + rect(12, 5, 3, 12, TEAL),
        "media-playback-stopped": rect(6, 6, 10, 10, TEAL_DIM),
        "network-wired-activated": stroke_rect(4, 7, 14, 8, TEAL, 1.8, 1)
                                   + rect(10, 15, 2, 4, TEAL),
        "network-wired": stroke_rect(4, 7, 14, 8, TEAL, 1.8, 1),
        "network-wired-available": stroke_rect(4, 7, 14, 8, TEAL_DIM, 1.8, 1),
        "network-wired-disconnected": stroke_rect(4, 7, 14, 8, OFF, 1.8, 1)
                                      + slash(),
        "network-wired-unavailable": stroke_rect(4, 7, 14, 8, OFF, 1.8, 1)
                                     + slash(),
        "nm-device-wired": stroke_rect(4, 7, 14, 8, TEAL, 1.8, 1),
        "network-offline": disc(OFF) + slash(),
        "network-unavailable": disc(OFF) + slash(),
        "network-limited": disc(AMBER) + rect(9, 10, 4, 2, AMBER),
        "network-bluetooth-activated": bluetooth(TEAL),
        "network-bluetooth": bluetooth(TEAL_DIM),
        "network-bluetooth-inactive": bluetooth(OFF) + slash(),
        "network-wireless-bluetooth": bluetooth(TEAL),
        "flightmode-on": path("M 11 3 L 13 11 L 19 14 L 13 14 L 11 19 L 9 14"
                              " L 3 14 L 9 11 Z", AMBER, 1.4, fill=AMBER),
        "flightmode-off": path("M 11 3 L 13 11 L 19 14 L 13 14 L 11 19 L 9 14"
                               " L 3 14 L 9 11 Z", OFF, 1.4, fill=OFF),
        "klipper": stroke_rect(6, 4, 10, 14, TEAL, 1.8, 1)
                   + rect(8, 8, 6, 1.4, TEAL) + rect(8, 11, 6, 1.4, TEAL)
                   + rect(8, 14, 4, 1.4, TEAL),
        "kdeconnect-tray": stroke_rect(7, 3, 8, 16, TEAL, 1.8, 1)
                           + rect(9, 16, 4, 1.4, TEAL),
        "device-notifier": stroke_rect(4, 6, 14, 10, TEAL, 1.8, 1)
                           + circle(14, 11, 1.6, TEAL),
        "keyboard-layout": stroke_rect(3, 7, 16, 9, TEAL, 1.6, 1)
                           + "".join(rect(5 + i * 3, 10, 2, 1.4, TEAL)
                                     for i in range(4))
                           + rect(7, 13, 8, 1.4, TEAL),
        "input-caps-on": stroke_rect(4, 4, 14, 14, AMBER, 1.6, 2)
                         + path("M 8 12 L 11 8 L 14 12", AMBER, 1.8),
        "input-num-on": stroke_rect(4, 4, 14, 14, AMBER, 1.6, 2)
                        + rect(10, 7, 2, 8, AMBER),
        "camera-on": stroke_rect(3, 7, 13, 9, TEAL, 1.6, 1)
                     + path("M 16 11 L 19 8 L 19 15 Z", TEAL, 1.4, fill=TEAL),
        "camera-off": stroke_rect(3, 7, 13, 9, OFF, 1.6, 1) + slash(),
        "camera-ready": stroke_rect(3, 7, 13, 9, TEAL_DIM, 1.6, 1),
        "video-off": stroke_rect(3, 7, 13, 9, OFF, 1.6, 1) + slash(),
        "waveform-off": rect(3, 10, 16, 1.6, OFF) + slash(),
        "rotation-allowed": path("M 5 11 A 6 6 0 1 1 11 17", TEAL, 1.8)
                            + path("M 8 14 L 11 17 L 8 20", TEAL, 1.8),
        "rotation-locked-landscape": stroke_rect(3, 7, 16, 9, AMBER, 1.8, 1),
        "rotation-locked-portrait": stroke_rect(7, 3, 9, 16, AMBER, 1.8, 1),
        "system-suspend-inhibited": disc(AMBER) + rect(10, 6, 2, 6, AMBER),
        "system-suspend-uninhibited": disc(TEAL_DIM) + rect(10, 6, 2, 6, TEAL_DIM),
        "touchpad_enabled": stroke_rect(3, 6, 16, 11, TEAL, 1.6, 1)
                            + rect(11, 6, 1.4, 11, TEAL),
        "touchpad_disabled": stroke_rect(3, 6, 16, 11, OFF, 1.6, 1) + slash(),
        "input-touchpad-on": stroke_rect(3, 6, 16, 11, TEAL, 1.6, 1),
        "input-touchpad-off": stroke_rect(3, 6, 16, 11, OFF, 1.6, 1) + slash(),
        "plasmavault_error": disc(DANGER) + rect(10, 6, 2, 7, DANGER)
                             + rect(10, 15, 2, 2, DANGER),
    }


def bluetooth(colour):
    return path("M 8 5 L 14 10 L 8 16 M 11 3 L 11 19 M 8 8 L 14 13",
                colour, 1.8)


def statuses():
    """Circle-badge glyph families: state, dialog, user presence, levels."""
    icons = {}
    marks = {
        "ok": lambda c: path("M 7 11 L 10 14 L 15 8", c, 2),
        "error": lambda c: path("M 8 8 L 14 14 M 14 8 L 8 14", c, 2),
        "warning": lambda c: rect(10, 6, 2, 7, c) + rect(10, 15, 2, 2, c),
        "information": lambda c: rect(10, 9, 2, 8, c) + rect(10, 5, 2, 2, c),
        "question": lambda c: path("M 8 8 A 3 3 0 1 1 11 12", c, 1.8)
                              + rect(10, 15, 2, 2, c),
        "offline": lambda c: rect(7, 10, 8, 2, c),
        "pause": lambda c: rect(8, 7, 2, 8, c) + rect(12, 7, 2, 8, c),
        "sync": lambda c: path("M 6 11 A 5 5 0 1 1 11 16", c, 1.8),
        "download": lambda c: rect(10, 6, 2, 7, c)
                              + path("M 8 12 L 11 16 L 14 12", c, 1.8),
    }
    colours = {"ok": TEAL, "error": DANGER, "warning": AMBER,
               "information": TEAL, "question": TEAL, "offline": OFF,
               "pause": AMBER, "sync": TEAL, "download": TEAL}
    for tag, draw in marks.items():
        c = colours[tag]
        icons[f"state-{tag}"] = circle(11, 11, 8, "none", c, 1.6) + draw(c)
    for tag in ["error", "information", "warning", "question"]:
        c = colours[tag]
        icons[f"dialog-{tag}"] = circle(11, 11, 8, "none", c, 1.6) + marks[tag](c)
    icons["dialog-positive"] = circle(11, 11, 8, "none", TEAL, 1.6) \
        + marks["ok"](TEAL)
    icons["dialog-password"] = stroke_rect(5, 9, 12, 9, TEAL, 1.6, 1) \
        + path("M 8 9 A 3 3 0 0 1 14 9", TEAL, 1.6)
    presence = {"available": TEAL, "online": TEAL, "away": AMBER,
                "away-extended": AMBER, "busy": DANGER, "idle": AMBER,
                "offline": OFF, "invisible": TEAL_DIM}
    for tag, c in presence.items():
        icons[f"user-{tag}"] = circle(11, 11, 7, c)
    for tag, c in [("high", TEAL), ("medium", AMBER), ("low", DANGER)]:
        icons[f"security-{tag}"] = path(
            "M 11 4 L 18 7 L 18 12 A 7 7 0 0 1 11 19 A 7 7 0 0 1 4 12 L 4 7 Z",
            c, 1.6)
        icons[f"update-{tag}"] = circle(11, 11, 8, "none", c, 1.6) \
            + marks["download"](c)
    icons["update-none"] = circle(11, 11, 8, "none", TEAL_DIM, 1.6)
    icons["update-busy"] = circle(11, 11, 8, "none", TEAL, 1.6)
    icons["data-error"] = icons["state-error"]
    icons["data-warning"] = icons["state-warning"]
    icons["data-success"] = icons["state-ok"]
    icons["data-information"] = icons["state-information"]
    for i in range(5):
        icons[f"task-process-{i}"] = "".join(
            f'<g transform="rotate({k * 72} 11 11)">'
            + rect(10.2, 3, 1.6, 5, TEAL, 0.3 + 0.7 * ((i + k) % 5) / 4)
            + '</g>'
            for k in range(5))
    icons["task-complete"] = icons["state-ok"]
    for tag, c in [("cold", TEAL), ("normal", TEAL_DIM), ("warm", AMBER)]:
        icons[f"temperature-{tag}"] = rect(10, 4, 2, 10, c) \
            + circle(11, 16, 3, c)
    return icons


def collect():
    icons = {}
    for fn in (batteries, wireless, mobile, volumes, simple, statuses):
        icons.update(fn())
    return icons


def main():
    icons = collect()
    written = links = 0
    for size in SIZES:
        d = SRC / "status" / size
        d.mkdir(parents=True, exist_ok=True)
        for name, body in icons.items():
            (d / f"{name}.svg").write_text(wrap(body), encoding="utf-8")
            written += 1
            for suffix in ("-symbolic", "-rtl", "-symbolic-rtl"):
                alias = d / f"{name}{suffix}.svg"
                if alias.exists() or alias.is_symlink():
                    alias.unlink()
                alias.symlink_to(f"{name}.svg")
                links += 1
    print(f"{len(icons)} icons -> {written} files + {links} aliases "
          f"across sizes {', '.join(SIZES)}")


if __name__ == "__main__":
    main()
