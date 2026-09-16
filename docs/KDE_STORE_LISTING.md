# KDE Store listing text

Ready to paste into the "Upload Product" form. Fill fields as below.

## Title

```
Retro DIN
```

## Summary / short description

```
90s car-stereo DIN unit / hi-fi rack theme for Plasma 6 — brushed metal,
glowing teal displays, amber active states, and an animated CRT-noise
splash, lock screen, and login screen.
```

## Full description

```
A Plasma 6 global theme styled after 90s car-stereo DIN units and hi-fi
racks: brushed dark metal, recessed glowing VFD-style displays, a glowing
rotary-knob launcher, teal identity glow with amber for active/hover/focus
states, and CRT phosphor noise animating the splash, lock, and login
screens.

WHAT'S INCLUDED
- Color scheme
- Plasma Style (desktoptheme) — panel, task manager, menus, tooltips,
  OSD, pager
- Aurorae window decoration
- Icon theme — full teal recolor of Breeze Dark, plus 357 custom-drawn
  status/tray icons and 101 app icons
- Kvantum style for Qt app interiors (Dolphin, Kate, browsers)
- Animated lock-screen wallpaper (CRT noise)
- Desktop wallpaper (still charcoal/CRT composite)
- SDDM login theme (animated, derived from Breeze)
- The Global Theme package that wires all of the above together

INSTALL
This is a script-installed bundle, not a single GHNS drop-in — there's
more here than one category installs. After extracting:

    scripts/install.sh

then apply it in System Settings → Appearance → Global Themes → Retro
DIN. The login screen is a separate, optional step that needs root:

    sudo scripts/install-sddm.sh

REQUIRES
- Kvantum (install from your distro's package manager — this is what
  makes app interiors match the theme; without it they'll use whatever
  Qt style you already had)
- Python 3 (used by the install script to generate the icon theme;
  no extra packages needed)

KNOWN LIMITATIONS
- Apps installed via snap (e.g. Firefox, Thunderbird on some distros)
  reference their icon by an absolute file path, which no icon theme can
  override — they'll keep their own icon regardless of theme.
- Only about 100 apps have a hand-drawn icon in the DIN style; everything
  else falls back to a teal-recolored Breeze icon.

Full docs, source, and issue tracker: <your GitHub repo URL here>
```

## License

GPL-3.0-or-later (mention in the description that the SDDM component is
CC-BY-SA, derived from Breeze — see `NOTICE.md` in the repo).

## Tags

```
plasma6, plasma, global-theme, dark-theme, retro, icon-theme, kvantum, sddm
```

## Category

**Plasma Global Themes** (see `docs/KDE_STORE_SUBMISSION.md` if you decide
to also submit components separately under their own categories).

## CC-BY credit field

The only CC-licensed component here is the SDDM login theme (derived from
Breeze, CC-BY-SA — the rest of the repo is GPL-3.0-or-later, see
`NOTICE.md`). Paste:

```
SDDM login theme background and greeter scripts (Main.qml, Login.qml,
KeyboardButton.qml, SessionButton.qml, Messages.sh) are derived from the
Breeze SDDM theme, © 2014 David Edmundson, part of KDE Plasma
(https://invent.kde.org/plasma/breeze), licensed CC-BY-SA.
```

## Logo

Upload `assets/logo.png` (512×512, rotary-knob mark matching the theme —
source at `assets/logo.svg`).

---

Before pasting: replace `<your GitHub repo URL here>` with the actual repo
URL once it exists.
