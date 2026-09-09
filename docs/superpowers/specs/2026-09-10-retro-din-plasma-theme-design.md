# Retro DIN/Hi-Fi Plasma 6 Global Theme — Design

Status: approved by user via visual companion walkthrough, 2026-09-10.

## 1. Visual language

Aesthetic: 90s car-stereo DIN unit / hi-fi rack face. Brushed dark metal
chassis, recessed glowing display wells (VFD-style), bezeled tactile
buttons, one glowing rotary knob. Confirmed against user-supplied
reference photos (Pioneer/Mitsubishi DIN units, Alpine VFD head units,
Sony/Denon hi-fi stacks) and two user-supplied CRT-noise GIFs used as
real phosphor texture on splash/lock.

### Two-tier color rule

This is the load-bearing decision for the whole theme. Widget style
(Qt app internals — Dolphin, Kate, etc.) was explicitly deferred
(user chose "Defer entirely" over Kvantum). Breeze stays the widget
style. That means `.colors` is the *only* thing reaching app
interiors, and it reaches literally everything: list text, form
fields, dialog labels.

- **Tier 1 — display surfaces**: panel, task buttons, titlebar
  (Aurorae), context menus, tooltips, OSD, notifications, splash,
  lock screen. Full teal-glow-on-black treatment, amber for
  active/focus/hover. Driven by desktoptheme SVG + Aurorae SVG, not
  by `.colors`.
- **Tier 2 — app interiors**: everything Breeze renders (menus,
  toolbars, list views, text fields) inside actual Qt apps. Flat by
  design — soft off-white text on charcoal, no glow. Driven by
  `.colors` only.

Tier 2 will **not** look like the panel/lock-screen mockups. That's
intentional, not a bug: glowing teal body text is unusable for daily
reading in a file manager or editor. State this plainly to the user
on first apply so it doesn't read as broken theming.

**Revisit-after-first-apply flag**: `.colors`' `Highlight` role is set
to amber, meaning every text selection and every selected list row in
every Qt app goes amber. User has only seen amber as a hover bar in a
small context-menu mockup, not as the global selection color. Apply
the theme, live with it a day, revisit if it's too aggressive
app-wide.

### Palette

| Role | Hex | Used for |
|---|---|---|
| Metal base (light stop) | `#34393b` | Brushed metal gradient top |
| Metal base (mid stop) | `#232829` | Brushed metal gradient mid |
| Metal base (dark stop) | `#16191a` | Brushed metal gradient bottom; also `.colors` Window/View background |
| Recessed well bg | `#001210` | Display wells: clock backdrop, menu, tooltip, OSD |
| Recessed well border | `#0a2e29` | Well border/inset |
| Teal (base) | `#14b8a6` | Identity/idle glow, `.colors` Link |
| Teal (bright/glow) | `#5eead4` | Display text, active-state glow highlight |
| Teal (dim) | `#0d6b60` | Inactive/secondary glow, menu separators |
| Amber (base) | `#ffb454` | Active/focus/hover/selected state |
| Amber (bright/glow) | `#ffd08a` | Active-state glow highlight |
| App body text (Tier 2 only) | `#cfece8` | `.colors` normal Text — soft off-white, NOT glowing teal |

## 2. Package inventory

Four packages, each independently installable:

1. **Color scheme** — `~/.local/share/color-schemes/RetroDIN.colors`
2. **Desktoptheme (Plasma Style)** — `~/.local/share/plasma/desktoptheme/RetroDIN/`
3. **Aurorae window decoration** — `~/.local/share/aurorae/themes/RetroDIN/`
4. **Look-and-feel wrapper** — `~/.local/share/plasma/look-and-feel/com.retrodin.theme/`
   (metadata.json, `contents/defaults` pointing at 1–3 plus reused
   existing icon set + Breeze widget style, `contents/layouts/...desktop-layout.js`
   for the panel, splash + lockscreen QML)

## 3. Component → package → asset map

| Component | Package | Asset | States |
|---|---|---|---|
| Panel background | desktoptheme | `widgets/panel-background.svg(z)` | single (no per-state theming; panel bg is static) |
| Panel clock | *(not themed by us)* | relojlcd plasmoid, placed by layout.js | configured via relojlcd's own settings, see §4 |
| Task manager buttons | desktoptheme | `widgets/tasks.svg(z)` | `normal`, `hover`, `focus` (=active window, confirmed by inspecting installed Breeze/WinSur-dark theme), `attention`, `minimized`, `progress` — each 9-sliced, duplicated per panel edge (`north-`/`east-`/`west-`/unprefixed) |
| Kickoff knob (app launcher) | desktoptheme | `widgets/button.svg` or dedicated launcher graphic | normal / hover / pressed |
| Titlebar + buttons | Aurorae | theme SVG + `<Name>rc` config | focused / unfocused; button hover = amber |
| Context menu | desktoptheme | `dialogs/background.svg(z)` + menu item styling | item normal / hover(amber) |
| Tooltip | desktoptheme | `widgets/tooltip.svg` | static |
| OSD (volume/brightness) | desktoptheme | OSD dialog background + custom bar rendering | level segments teal, current segment amber |
| Notification popup | desktoptheme | `dialogs/background.svg(z)` (notification variant) | static, amber left-edge accent for urgent |
| Splash screen | look-and-feel | `contents/splash/Splash.qml` | boot animation, CRT-gif overlay |
| Lock screen | look-and-feel | `contents/lockscreen/LockScreenUi.qml` (or similar) | CRT-gif overlay, big VFD clock, recessed password field |

### Panel-background tiling constraint (confirmed via asset inspection)

Inspected both `WinSur-dark` and system default (Breeze)
`panel-background.svg(z)`: it's a 9-slice border-image
(topleft/top/topright/left/center/right/bottomleft/bottom/bottomright
+ `hint-*-margin` + `hint-tile-center` + separate `shadow-*` layer +
`mask-*` rounding layer). The `center` piece tiles or stretches per
`hint-tile-center` — for a brushed-metal texture with diagonal
micro-scratches, stretching would distort the scratch angle across
different panel widths, so **the center tile must be authored as a
small seamlessly-tileable pattern**, not a single full-width image.
Consequence for asset authoring: put any position-specific effect
(specular highlight corner) only in the fixed-size `topleft` corner
piece; keep `center` a uniform, seamlessly-tiling scratch+speckle
pattern with no directional "sheen" baked in. This was the one
technical unknown flagged before spec-writing — resolved, no design
change needed, just an authoring constraint.

## 4. relojlcd integration

The panel's VFD clock in every approved mockup is the already-installed
`com.gitlab.corral1976.relojlcd` plasmoid, not a theme-drawn element.
Confirmed by inspection: it bundles its own DSEG7Classic TTF fonts and
renders with `Plasmoid.backgroundHints: NoBackground`, fully
independent of desktoptheme. Its glow/digit color is set through its
own config (`contents/config/main.xml` + `colorUtils.js`), not through
our `.colors` or desktoptheme.

Implication: our look-and-feel layout.js places relojlcd on the panel
and can pre-seed its config keys to the teal palette above, but a
future relojlcd update could reset those keys — this is an external
dependency, not something our package fully owns. Desktoptheme's job
is only the recessed-well *frame* around it, if any; relojlcd draws
its own digits.

## 5. Explicit out of scope

- **Widget style (Kvantum/kstyle)** — user chose to defer entirely.
  Qt-app menus/toolbars/scrollbars stay flat Breeze, recolored via
  `.colors` (Tier 2, §1). Revisit as a separate future project if
  wanted.
- **Icon theme** — reuse existing installed set (e.g. `NTLegacyIcons`
  or `WhiteSur-dark`), no custom icons authored.
- **SDDM login theme** — separate package type, not applied by
  `plasma-apply-lookandfeel`. Not built.

## 6. Open items (non-blocking, revisit after first apply)

- Amber as global `.colors` `Highlight`/`DecorationFocus` — user has
  only seen it in a small mockup context, not app-wide. Flagged in §1.
- The two user-supplied GIFs (`movie2_glow.gif` ~4.8MB, `movie8_f_glow.gif`
  ~5.3MB, both 1024×256) are used as splash/lock phosphor-noise
  texture at 28% opacity, screen-blend. Ship re-encoded/shortened
  versions in the final package, not these originals — target a few
  hundred KB, short seamless loop.
- Distribution: personal use only, not KDE Store. Skips license file
  polish, screenshot set, store metadata. Revisit if user wants to
  publish later.

## 7. Testing

- `plasma-apply-colorscheme RetroDIN`
- `plasma-apply-desktoptheme RetroDIN`
- `kpackagetool6 -t Plasma/LookAndFeel -i com.retrodin.theme` (or `-u` to upgrade)
- `plasmashell --replace &` to reload SVG changes without full logout
- `kwin_x11 --replace &` / `kwin_wayland --replace &` (session-dependent) after Aurorae changes
- **layout.js only runs if the user ticks "desktop layout" in the
  Global Theme apply dialog** — the panel/relojlcd placement will not
  happen on a plain "apply look-and-feel" unless that box is checked.
  Must document this for the user at apply time, not just at install
  time.
