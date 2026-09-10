# Publishing Retro DIN to the KDE Store

This is a packaging and pre-submission guide, not a click-by-click walkthrough
of store.kde.org's upload form — that UI changes over time and isn't
something to reconstruct from memory. What's below is verified against this
repo's actual package metadata; confirm category names and upload steps on
the site itself when you get there.

## Why this theme doesn't fit "one GHNS upload"

KDE's Store install mechanism (GHNS — "Get Hot New Stuff") is built around
one category installing to one destination folder. Retro DIN is nine
packages across nine different destinations (`color-schemes/`,
`desktoptheme/`, `aurorae/`, `lookandfeel/`, `icons/`, `kvantum/`,
`wallpapers/` ×2, `sddm/`). A Plasma **Global Theme** entry only installs
the look-and-feel package (`lookandfeel/com.retrodin.theme/`) — it does
**not** pull in a color scheme, desktoptheme, or window decoration that
aren't already on disk. This is a real limitation of Plasma's Global Theme
system in general, not specific to this repo: `contents/defaults` can
*reference* `ColorScheme=RetroDIN`, but if that color scheme was never
installed, Plasma just silently keeps whatever scheme was already active.

Two honest options:

1. **Multiple GHNS entries, cross-linked.** Submit the color scheme, the
   Plasma Theme (desktoptheme), the window decoration, the icon theme, the
   Kvantum theme, and the SDDM theme as separate Store entries, then submit
   the Global Theme entry with a description telling people to install the
   others first (linking each). This gets each piece proper GHNS
   discoverability and in-app one-click install, at the cost of the user
   needing several installs.
2. **Single download, install script.** Package the whole repo as one
   archive under the "Plasma Global Themes" category, with the description
   pointing at `scripts/install.sh` instead of relying on GHNS's automatic
   unpack. This is the more common pattern for multi-component themes with
   more moving parts than GHNS's per-category model assumes — several
   popular full-desktop themes on the Store ship this way, with the Store
   entry acting as a landing page/changelog rather than a literal
   auto-installer.

Given Retro DIN also needs a separately-installed dependency (Kvantum
itself) and a root-level install step (the SDDM theme), option 2 is the
realistic one: nobody can `sudo` from inside a GHNS install anyway. Use the
Store entry to point at the repo and `README.md`, the same way you'd list a
GitHub-hosted theme.

## What to check before uploading anything

Read straight from what's already in this repo — no guessing needed:

- **License must match what you declare on the Store.** Every package's
  `metadata.json`/`metadata.desktop` already says `GPL-3.0`, except the
  SDDM theme (`CC-BY-SA`, since it's a Breeze derivative — see
  `NOTICE.md`). Pick the Store's license field to match per entry if you
  go the multi-entry route; if one bundle, GPL-3.0-or-later covers the
  whole with a note in the description about the SDDM component's CC-BY-SA
  origin.
- **Version numbers.** Every `metadata.json`/`metadata.desktop` in this
  repo says `"Version": "1.0"` (or `Version=1.0`). Bump these together with
  any Store release version you set, so the two don't drift.
- **Author field.** `sddm/RetroDIN/metadata.desktop` has `Author=yousuf
  khan` already. The others don't set an author field explicitly — add one
  if the Store form requires it per package
  (`X-KDE-PluginInfo-Author=`/`"Author":`).
- **Generated assets must be built before packaging.** `icons/RetroDIN/`
  and the three GIF frames are gitignored — they don't exist until
  `scripts/install.sh` runs. A Store download of a raw `git archive` would
  be missing them. Either run the install/generator scripts and package
  the *output*, or make sure the description makes clear the user needs to
  run `scripts/install.sh` themselves (requires Python 3, no extra
  packages).

## Packaging per category (if you go the multi-entry route)

For each, the archive root should be the package folder's *contents*, not
a wrapper directory — GHNS installs whatever's in the zip directly into the
category's target folder.

| Store category (typical naming) | Repo source | Archive should contain |
|---|---|---|
| Plasma Color Schemes | `color-schemes/RetroDIN.colors` | Just the `.colors` file |
| Plasma Themes (Desktop Theme) | `desktoptheme/RetroDIN/` | Contents of `RetroDIN/`, so `metadata.json` is at the zip root |
| Window Decorations (Aurorae) | `aurorae/RetroDIN/` | Contents of `RetroDIN/` |
| Global Themes (Plasma 6) | `lookandfeel/com.retrodin.theme/` | Contents of `com.retrodin.theme/` |
| Icon Themes | `icons/RetroDIN/` (built, not `RetroDIN-src`) | Contents of `RetroDIN/` |
| Kvantum Themes | `kvantum/RetroDIN/` | Contents of `RetroDIN/` |
| Plasma Wallpapers | `wallpapers/RetroDIN-lockwall/` and/or `wallpapers/com.retrodin.crtnoise/` | Contents of each, separately — they're different plugin IDs |
| SDDM Themes | `sddm/RetroDIN/` (with `background.gif` built in) | Contents of `RetroDIN/` |

Double-check each category's exact current name and any category-specific
required fields on the site — these have been renamed before across Plasma
5 → 6 and the Store's own redesigns.

## Preview image

Every category wants at least one preview screenshot; take it from a real,
applied desktop (panel + a themed window +, ideally, a menu open) rather
than a mockup, since that's what reviewers compare against. Check the
current size/format limit on the upload form itself before exporting —
don't assume a fixed pixel size, it has changed across Store versions.

## Description checklist

Whatever you write, make sure it plainly states, since this theme is more
demanding than a single-file theme:

- Kvantum is a separate, required install for app interiors to look right.
- The SDDM login theme needs root and a separate script
  (`sudo scripts/install-sddm.sh`) — it will not appear from installing
  the Global Theme alone.
- The known gaps in `ROADMAP.md` (snap-packaged Firefox/Thunderbird icons,
  MIME/app icons outside the 101 hand-drawn ones) — so it doesn't read as
  a bug report against your own listing later.
