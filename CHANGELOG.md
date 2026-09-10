# Changelog

Format loosely follows [Keep a Changelog](https://keepachangelog.com/).
This theme has shipped once, incrementally, straight to a working desktop —
so there's a single `1.0.0` entry grouped by area rather than a version per
commit.

## [1.0.0] — 2026-09-10

### Added

- Package skeletons for color scheme, desktoptheme, Aurorae, and the
  look-and-feel wrapper, plus an install script and an SVG/INI validator.
- Brushed-metal panel background, kickoff knob launcher, task-manager button
  states (normal/hover/focus/attention), recessed-well menu/dialog/tooltip
  frames, and an Aurorae titlebar with amber-hover minimize/maximize/close.
- Panel layout: kickoff, task manager, systray, clock.
- CRT-noise animated boot splash (`Splash.qml`).
- Full desktoptheme completeness sweep: all 43 widget assets present and
  verified against the default theme's element list via QtSvg, including
  glyphs (arrows, checkmarks, switches, sliders), figures (clock, timer,
  analog meter), and previously-missing frames (`button.svg` had never
  shipped a 9-slice set, so every ordinary Plasma button had no frame at
  all until this).
- Kvantum app-interior style, colour-remapped from KvDark via a luminance
  ramp rather than a blind hex substitution (KvDark's artwork is pure
  greyscale, so remapping preserves shading structure).
- RetroDIN icon theme: full teal recolor of Breeze Dark, a custom launcher
  glyph (fixes the icon theme silently reverting and showing another
  theme's logo in the launcher), 357 parametrically-generated status/tray
  icons (battery, wireless, volume, bluetooth, media, etc. across 4 sizes),
  and 101 app icons classified from `.desktop` file categories into 29
  hand-drawn archetypes.
- Animated CRT-noise wallpaper plugin (`com.retrodin.crtnoise`) for the
  lock screen — required because the stock `org.kde.image` wallpaper plugin
  only ever renders a still frame, no matter what image it's given.
- SDDM login theme, derived from Breeze, with the noise background animated
  the same way as the splash and lock screen.

### Fixed

- **9-slice geometry stacking**: every `<state>-<piece>` element was a
  `<use>` of the *entire* widget canvas instead of its own slice, so panel,
  task, and dialog textures rendered visibly doubled/stacked. Rewrote the
  slice emission through a shared `scripts/svgslice.py` module.
- **Panel gradient banding**: the metal gradient used `objectBoundingBox`
  units, which replays the full gradient ramp inside each 9-slice piece's
  own bounding box. Switched to `userSpaceOnUse`.
- **Panel texture artifacts**: an early fix for tiling seams (removing
  `hint-tile-center`, drawing explicit streak lines) traded seams for
  visible hard stripes across a wide panel. Fixed by using many more,
  finer, lower-opacity streaks instead of a few opaque ones.
- **Pager showing default-theme blue boxes**: no `pager.svg` was shipped,
  so `org.kde.plasma.pager` silently fell back to the upstream theme.
- **Task-switcher icons rendering tiny**: `tasks.svg` had no explicit
  margin hints, so FrameSvg derived margins from 8px corner art, wasting
  16px per axis on a 48px canvas. Added explicit 2px margin hints.
  (`ecb79af`)
- **SDDM theme installed but never actually active**: the theme's
  `/etc/sddm.conf.d/99-retrodin.conf` drop-in was silently overridden,
  because SDDM reads that directory in plain alphabetical order and
  digit-prefixed filenames sort *before* the distro's own
  `kde_settings.conf`. Renamed to `zz-retrodin.conf`. (`ee7b7e2`)
- Duplicate 3.4MB noise-loop binary tracked under three separate package
  paths; kept one canonical copy and had `install.sh` copy it out at
  install time. (`a6cc7dd`)

## Known limitations

See `ROADMAP.md`.
