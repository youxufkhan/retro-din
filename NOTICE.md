# Third-party attribution

Retro DIN is licensed GPL-3.0-or-later (see `LICENSE`) except for the
components below, which are derived from other GPL-compatible KDE assets and
keep their original licensing.

## SDDM login theme (`sddm/RetroDIN/`)

Derived from the **Breeze** SDDM theme, © 2014 David Edmundson, part of
[KDE Plasma](https://invent.kde.org/plasma/breeze). Licensed
**CC-BY-SA**, per `sddm/RetroDIN/metadata.desktop`. `Main.qml`,
`Login.qml`, `KeyboardButton.qml`, `SessionButton.qml`, and
`Messages.sh` are copied unmodified; only `Background.qml` (swapped to
`AnimatedImage`) and `theme.conf` were changed.

## Kvantum app-interior theme (`kvantum/RetroDIN/`)

Colour-remapped from **KvDark** by Tsu Jan, part of the
[Kvantum](https://github.com/tsujan/Kvantum) project. `RetroDIN.svg` is
KvDark's artwork with every colour remapped through a luminance ramp
(see `scripts/gen_kvantum.py`); `RetroDIN.kvconfig` is KvDark's config
with the `[GeneralColors]` block and `author=`/`comment=` lines
replaced. Kvantum itself is LGPL-2.1-or-later; check your Kvantum
package's license for the base theme's exact terms if redistributing
the generated files outside this repo.

## Icon theme (`icons/RetroDIN/`)

Built by recolouring a full copy of **Breeze Dark**
(`/usr/share/icons/breeze-dark`), part of KDE Plasma, licensed
LGPL-3.0. See `scripts/gen_icons.py`. Hand-authored and generated
status/tray/app icons in `icons/RetroDIN-src/` are original work under
this repo's GPL-3.0-or-later.
