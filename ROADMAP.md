# Roadmap

Retro DIN is feature-complete as a daily-driver theme. What's below is
either a known limitation worth being upfront about, or an idea that never
got prioritized.

## Known limitations

- **Snap-packaged apps ignore the icon theme.** Firefox and Thunderbird, as
  installed via snap on Kubuntu, reference their icon by an absolute
  `Icon=/snap/.../foo.png` path in their `.desktop` file. An icon theme
  can't override an absolute path — only a bare icon *name* — so these two
  keep their upstream icon regardless of theme. `scripts/gen_app_icons.py`
  still generates a Retro DIN icon for them (`EXTRA_NAMES`) in case a
  non-snap install is ever added.
- **MIME-type and non-authored app icons stay Breeze-derived.** Full teal
  recolor covers every icon in Breeze Dark, but only 101 apps have a
  hand-drawn Retro DIN archetype; everything else falls back to the
  recolored Breeze artwork, which is teal-tinted but not restyled to the
  DIN look.
- **User avatar / face icon is untouched.** `sddm/RetroDIN/faces/.face.icon`
  is carried over from Breeze as-is.
- **Animated wallpapers cost more than a still one.** `com.retrodin.crtnoise`
  decodes a GIF continuously on the lock screen; on very low-power hardware
  this is worth knowing before enabling it as the *desktop* wallpaper too
  (it currently isn't — the desktop uses the still `RetroDIN-lockwall`).
- **Kvantum is a manual dependency.** It has to be installed from the
  distro's package manager separately; there's no bundling story for a
  KDE Store submission, since GHNS installs can't run package-manager
  commands. See `docs/KDE_STORE_SUBMISSION.md`.

## Ideas, not committed

- Konsole color scheme to match the palette (currently untouched — terminal
  colors are whatever profile the user already has).
- A light variant, or at least a documented "how to adjust the amber/teal
  balance" note for people who find full-teal too aggressive for Tier 2
  (app interiors) — see the two-tier rule in `README.md`.
- GTK app theming (currently out of scope entirely; Qt/Kvantum only).
- Wallpaper variety — right now there's exactly one wallpaper shipped.
- A screenshot/preview folder for the KDE Store listing and this README.
