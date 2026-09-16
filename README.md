# Retro DIN

A Plasma 6 global theme styled after 90s car-stereo DIN units and hi-fi
racks: brushed dark metal, recessed glowing VFD-style displays, a glowing
rotary-knob launcher, teal identity glow with amber for active/hover/focus
states, and CRT phosphor noise on the splash and lock screens.

![status](https://img.shields.io/badge/status-personal_theme-14b8a6)
![Plasma](https://img.shields.io/badge/Plasma-6-2fd4bf)
![license](https://img.shields.io/badge/license-GPL--3.0--or--later-black)

## What's in it

Nine independently-installable KDE packages, all under one repo:

| Package | Path | What it themes |
|---|---|---|
| Color scheme | `color-schemes/RetroDIN.colors` | `kdeglobals`-level app colors (Tier 2, see below) |
| Desktoptheme (Plasma Style) | `desktoptheme/RetroDIN/` | Panel, task buttons, menus, tooltips, OSD, pager — 43/43 assets, full parity with the default theme |
| Aurorae window decoration | `aurorae/RetroDIN/` | Titlebar, minimize/maximize/close |
| Look-and-feel (global theme) | `lookandfeel/com.retrodin.theme/` | Wires everything else together: color scheme, Aurorae, desktoptheme, icon theme, Kvantum, panel layout, and the animated CRT-noise boot splash |
| Icon theme | `icons/RetroDIN/` | Full teal recolor of Breeze Dark, plus 357 hand-generated status/tray icons and 101 app icons |
| Kvantum style | `kvantum/RetroDIN/` | Qt app interiors (Dolphin, Kate, browsers) — colour remap of KvDark |
| Lock-screen wallpaper plugin | `wallpapers/com.retrodin.crtnoise/` | Animated CRT noise on the lock screen (the stock `org.kde.image` plugin can't animate) |
| Desktop wallpaper | `wallpapers/RetroDIN-lockwall/` | Still charcoal/CRT composite used as the default desktop background |
| SDDM login theme | `sddm/RetroDIN/` | Animated login screen, derived from Breeze SDDM |

### The two-tier color rule

Glowing teal body text is unusable for daily reading in a file manager. So:

- **Tier 1 — display surfaces** (panel, task buttons, titlebar, menus,
  tooltips, OSD, splash, lock/login screens): full teal-glow-on-black, amber
  for active/focus/hover. Driven by the desktoptheme, Aurorae, and Kvantum
  SVGs — not by the color scheme.
- **Tier 2 — app interiors** (everything Qt apps render through Kvantum):
  flat, readable — soft off-white text on charcoal, no glow. Driven by
  `color-schemes/RetroDIN.colors`.

### Palette

| Role | Hex |
|---|---|
| Metal (light/mid/dark gradient stops) | `#34393b` / `#232829` / `#16191a` |
| Recessed well background | `#001210` |
| Recessed well border | `#0a2e29` |
| Teal (base / identity glow) | `#14b8a6` |
| Teal (bright / active glow) | `#5eead4` |
| Teal (dim / inactive) | `#0d6b60` |
| Amber (active/focus/hover) | `#ffb454` |
| Amber (bright glow) | `#ffd08a` |
| App body text (Tier 2 only) | `#cfece8` |

## Install

Requires Python 3 (stdlib only — no pip packages) and a Breeze Dark icon
theme on disk (`/usr/share/icons/breeze-dark`, present by default on any KDE
Plasma install). [Kvantum](https://github.com/tsujan/Kvantum) must be
installed separately (e.g. `apt install qt6ct kvantum`) for the app-interior
theming to take effect — without it, `widgetStyle=kvantum` just falls back
to whatever Qt picks by default.

```bash
git clone <your-fork-url> retro-din && cd retro-din
scripts/install.sh
```

This generates the icon theme and desktoptheme colors from source, then
symlinks all packages into `~/.local/share/...` and `~/.config/Kvantum/`.
Safe to re-run any time (idempotent) — do that after pulling changes.

Apply it: **System Settings → Appearance → Global Themes → Retro DIN**.

### Login screen (optional, needs root)

The SDDM theme installs system-wide and is a separate step:

```bash
sudo scripts/install-sddm.sh
```

Verify it before logging out: `sddm-greeter-qt6 --test-mode --theme /usr/share/sddm/themes/RetroDIN`.
Revert with `sudo rm /etc/sddm.conf.d/zz-retrodin.conf`.

## Repo layout

```
color-schemes/    desktoptheme/    aurorae/    lookandfeel/
icons/             kvantum/         sddm/       wallpapers/
assets/            scripts/         docs/
```

Generated output is gitignored, not tracked — `scripts/install.sh` rebuilds
it every run:

- `icons/RetroDIN/` (the ~40MB recolored icon tree)
- `icons/RetroDIN-src/status/` and `icons/RetroDIN-src/apps/` (the 357
  status/tray and 101 app icons `scripts/gen_din_icons.py` and
  `scripts/gen_app_icons.py` draw parametrically — there's no source SVG
  to edit for these, only the generator)
- `desktoptheme/RetroDIN/colors`
- the three `*.gif` noise-loop copies

Only `assets/noise.gif` (the one committed source loop) and the 8
hand-authored files under `icons/RetroDIN-src/` (the launcher glyph and its
aliases) are tracked as actual icon/asset sources.

See `scripts/` for the generators — most desktoptheme/icon assets are
parametric (drawn by a Python script from a small spec table), not
hand-edited SVG, so re-theming a color or a whole family is a one-file
change followed by re-running the relevant `scripts/gen_*.py`.

## Docs

- `CHANGELOG.md` — what shipped, grouped by area.
- `ROADMAP.md` — known gaps and ideas for more.
- `docs/KDE_STORE_QUICKSTART.md` — short numbered steps to package and
  upload this to [store.kde.org](https://store.kde.org).
- `docs/KDE_STORE_SUBMISSION.md` — the full packaging guide behind it
  (category mapping, license notes, why a single bundle instead of nine
  separate listings).
- `NOTICE.md` — third-party attribution (Breeze, KvDark, Breeze Dark icons).

## License

GPL-3.0-or-later, except the SDDM theme (CC-BY-SA, derived from Breeze) and
notes on the Kvantum/icon derivations — see `NOTICE.md`.
