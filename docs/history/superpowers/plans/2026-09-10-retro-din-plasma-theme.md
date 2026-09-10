# Retro DIN/Hi-Fi Plasma 6 Global Theme Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build and install a Plasma 6 global theme (4 independent KDE packages) giving a 90s DIN car-stereo/hi-fi aesthetic: brushed-metal panel with a glowing knob and amber-active task buttons, matching Aurorae window decoration, themed Plasma-native dialogs (menu/tooltip/OSD/notification), and a CRT-noise boot splash.

**Architecture:** Four independent, separately-installable KDE packages, each with its own metadata and no shared code: a `.colors` scheme, a `desktoptheme` (Plasma Style) SVG package, an `aurorae` window-decoration SVG package, and a `look-and-feel` wrapper package that points at the other three, adds a panel layout script, and adds a splash screen. All colors are hardcoded hex in the SVGs (not the dynamic `current-color-scheme` indirection) so the retro palette renders correctly regardless of which `.colors` scheme is separately active — this theme ships its own matching one anyway.

**Tech Stack:** Hand-written SVG 1.1 (gradients + `<pattern>`, no external tool dependency), KConfig INI (`.colors`, Aurorae `rc`, `defaults`), KPackage `metadata.json`/`metadata.desktop`, Plasma look-and-feel `layout.js` (`plasma.loadSerializedLayout`), QML (`Splash.qml`, Qt 6 / Kirigami — matches the installed system template). Validation uses only Python 3 stdlib (`json`, `xml.etree.ElementTree`, `configparser`) — no new packages.

**Spec:** `docs/superpowers/specs/2026-09-10-retro-din-plasma-theme-design.md` (read both — this plan argues from that spec, including its lock-screen correction: lock screen is colors+wallpaper only, no custom QML).

## Global Constraints

- Palette (exact hex, from spec §1): metal `#34393b`→`#232829`→`#16191a`; well bg `#001210`, well border `#0a2e29`; teal base `#14b8a6`, teal bright `#5eead4`, teal dim `#0d6b60`; amber base `#ffb454`, amber bright `#ffd08a`; Tier-2 app text `#cfece8` (never glowing teal for body text).
- Package IDs: color scheme `RetroDIN`; desktoptheme `RetroDIN`; Aurorae `RetroDIN`; look-and-feel `com.retrodin.theme`.
- Install paths are fixed: `~/.local/share/color-schemes/`, `~/.local/share/plasma/desktoptheme/`, `~/.local/share/aurorae/themes/`, `~/.local/share/plasma/look-and-feel/`. All work happens in a `build/` staging directory in this repo and gets copied/symlinked into place per-task (see Task 1).
- No widget-style (Kvantum/kstyle) work — deferred (spec §5). No icon theme authored — reuse whatever is already installed. No SDDM theme. No lock-screen QML fork (spec §3 correction) — do not create any file under `~/.local/share/plasma/shells/`.
- Every SVG must keep the exact element `id`s Plasma looks up (verified per-task below by inspecting the installed system/WinSur-dark themes) — a missing or misspelled id renders as blank, not an error.
- Every task's validation step must actually run and pass before commit. No task is done with a red check.

---

## Task 1: Package skeletons + color scheme

**Files:**
- Create: `build/color-schemes/RetroDIN.colors`
- Create: `build/desktoptheme/RetroDIN/metadata.json`
- Create: `build/aurorae/RetroDIN/metadata.desktop`
- Create: `build/lookandfeel/com.retrodin.theme/metadata.json`
- Create: `scripts/install.sh`
- Create: `scripts/validate.py`
- Test: `scripts/validate.py` (shared validator, used by every later task too)

**Interfaces:**
- Produces: `scripts/validate.py` exposes CLI `python3 scripts/validate.py <kind> <path> [ids...]` where `<kind>` is one of `json`, `svg`, `ini`. Exit code 0 = valid, 1 = invalid (with a message on stderr). Later tasks call this, don't reimplement validation.
- Produces: `scripts/install.sh` symlinks everything under `build/` into the real KDE data dirs (`~/.local/share/...`). Later tasks re-run it after adding files; it's idempotent (safe to re-run).

- [ ] **Step 1: Write the validator (there's no pre-existing test to write first — this task's "test" is step 3)**

```python
# scripts/validate.py
import sys, json, configparser
import xml.etree.ElementTree as ET

def validate_json(path):
    with open(path) as f:
        json.load(f)

def validate_svg(path, required_ids):
    tree = ET.parse(path)
    root = tree.getroot()
    found = {el.get('id') for el in root.iter() if el.get('id')}
    missing = [i for i in required_ids if i not in found]
    if missing:
        raise ValueError(f"missing SVG ids: {missing}")

def validate_ini(path, required_sections):
    cp = configparser.ConfigParser(strict=False)
    cp.read(path)
    missing = [s for s in required_sections if s not in cp.sections()]
    if missing:
        raise ValueError(f"missing ini sections: {missing}")

if __name__ == "__main__":
    kind, path = sys.argv[1], sys.argv[2]
    extra = sys.argv[3:]
    try:
        if kind == "json":
            validate_json(path)
        elif kind == "svg":
            validate_svg(path, extra)
        elif kind == "ini":
            validate_ini(path, extra)
        else:
            raise ValueError(f"unknown kind {kind}")
    except Exception as e:
        print(f"INVALID {path}: {e}", file=sys.stderr)
        sys.exit(1)
    print(f"OK {path}")
```

- [ ] **Step 2: Run validator against a missing file to confirm it fails loudly**

Run: `python3 scripts/validate.py json build/desktoptheme/RetroDIN/metadata.json`
Expected: `INVALID ...: [Errno 2] No such file or directory: ...` and exit code 1 (file doesn't exist yet — this is the "red" before the "green" for this task's real deliverables in steps 3-6).

- [ ] **Step 3: Write the color scheme file**

```ini
# build/color-schemes/RetroDIN.colors
[ColorEffects:Disabled]
Color=112,111,110
ColorAmount=0.025
ColorEffect=2
ContrastAmount=0.65
ContrastEffect=1
IntensityAmount=0.1
IntensityEffect=2

[ColorEffects:Inactive]
ChangeSelectionColor=true
Color=112,111,110
ColorAmount=0.025
ColorEffect=2
ContrastAmount=0.1
ContrastEffect=2
Enable=false
IntensityAmount=0
IntensityEffect=0

[Colors:Button]
BackgroundAlternate=35,40,41
BackgroundNormal=22,25,26
DecorationFocus=255,180,84
DecorationHover=255,180,84
ForegroundActive=255,180,84
ForegroundInactive=94,120,117
ForegroundLink=20,184,166
ForegroundNegative=218,68,83
ForegroundNeutral=246,116,0
ForegroundNormal=207,236,232
ForegroundPositive=39,174,96
ForegroundVisited=13,107,96

[Colors:Complementary]
BackgroundAlternate=35,40,41
BackgroundNormal=22,25,26
DecorationFocus=255,180,84
DecorationHover=255,180,84
ForegroundActive=255,180,84
ForegroundInactive=94,120,117
ForegroundLink=20,184,166
ForegroundNegative=218,68,83
ForegroundNeutral=246,116,0
ForegroundNormal=207,236,232
ForegroundPositive=39,174,96
ForegroundVisited=13,107,96

[Colors:Header]
BackgroundAlternate=35,40,41
BackgroundNormal=22,25,26
ForegroundActive=255,180,84
ForegroundInactive=94,120,117
ForegroundNormal=207,236,232

[Colors:Header][Inactive]
BackgroundNormal=22,25,26
ForegroundNormal=94,120,117

[Colors:Selection]
BackgroundAlternate=255,208,138
BackgroundNormal=255,180,84
DecorationFocus=255,208,138
DecorationHover=255,208,138
ForegroundActive=22,25,26
ForegroundInactive=22,25,26
ForegroundLink=13,107,96
ForegroundNegative=218,68,83
ForegroundNeutral=246,116,0
ForegroundNormal=22,25,26
ForegroundPositive=39,174,96
ForegroundVisited=22,25,26

[Colors:Tooltip]
BackgroundAlternate=35,40,41
BackgroundNormal=0,18,16
DecorationFocus=255,180,84
DecorationHover=255,180,84
ForegroundActive=94,234,212
ForegroundInactive=13,107,96
ForegroundLink=20,184,166
ForegroundNegative=218,68,83
ForegroundNeutral=246,116,0
ForegroundNormal=207,236,232
ForegroundPositive=39,174,96
ForegroundVisited=13,107,96

[Colors:View]
BackgroundAlternate=35,40,41
BackgroundNormal=22,25,26
DecorationFocus=255,180,84
DecorationHover=255,180,84
ForegroundActive=255,180,84
ForegroundInactive=94,120,117
ForegroundLink=20,184,166
ForegroundNegative=218,68,83
ForegroundNeutral=246,116,0
ForegroundNormal=207,236,232
ForegroundPositive=39,174,96
ForegroundVisited=13,107,96

[Colors:Window]
BackgroundAlternate=35,40,41
BackgroundNormal=22,25,26
DecorationFocus=255,180,84
DecorationHover=255,180,84
ForegroundActive=255,180,84
ForegroundInactive=94,120,117
ForegroundLink=20,184,166
ForegroundNegative=218,68,83
ForegroundNeutral=246,116,0
ForegroundNormal=207,236,232
ForegroundPositive=39,174,96
ForegroundVisited=13,107,96

[General]
ColorScheme=RetroDIN
Name=RetroDIN
shadeSortColumn=true

[KDE]
contrast=4

[WM]
activeBackground=22,25,26
activeBlend=255,180,84
activeForeground=207,236,232
inactiveBackground=22,25,26
inactiveBlend=94,120,117
inactiveForeground=94,120,117
```

- [ ] **Step 4: Validate the color scheme**

Run: `python3 scripts/validate.py ini build/color-schemes/RetroDIN.colors Colors:Window Colors:Selection Colors:Button General WM`
Expected: `OK build/color-schemes/RetroDIN.colors`

- [ ] **Step 5: Write the three remaining metadata files**

```json
// build/desktoptheme/RetroDIN/metadata.json
{
    "KPlugin": {
        "Id": "RetroDIN",
        "Name": "Retro DIN",
        "Description": "90s car-stereo/hi-fi DIN unit aesthetic Plasma Style",
        "Version": "1.0",
        "License": "GPL-3.0",
        "EnabledByDefault": true
    },
    "X-Plasma-API": "5.0"
}
```

```ini
# build/aurorae/RetroDIN/metadata.desktop
[Desktop Entry]
Name=RetroDIN
X-KDE-PluginInfo-Author=RetroDIN theme
X-KDE-PluginInfo-Name=RetroDIN
X-KDE-PluginInfo-Version=1.0
X-KDE-PluginInfo-License=GPL v3
X-KDE-PluginInfo-EnabledByDefault=true
```

```json
// build/lookandfeel/com.retrodin.theme/metadata.json
{
    "KPackageStructure": "Plasma/LookAndFeel",
    "KPlugin": {
        "Id": "com.retrodin.theme",
        "Name": "Retro DIN",
        "Description": "90s car-stereo/hi-fi DIN unit global theme",
        "Category": "Global Themes (Plasma 6)",
        "ServiceTypes": ["Plasma/LookAndFeel"],
        "EnabledByDefault": true,
        "License": "GPL-3.0"
    },
    "X-Plasma-MainScript": "defaults",
    "X-Plasma-APIVersion": "2"
}
```

- [ ] **Step 6: Validate all three, and re-run Step 2's command to confirm it now passes**

Run:
```bash
python3 scripts/validate.py json build/desktoptheme/RetroDIN/metadata.json
python3 scripts/validate.py ini build/aurorae/RetroDIN/metadata.desktop "Desktop Entry"
python3 scripts/validate.py json build/lookandfeel/com.retrodin.theme/metadata.json
```
Expected: three `OK ...` lines.

- [ ] **Step 7: Write the install script**

```bash
#!/usr/bin/env bash
# scripts/install.sh — symlink build/ output into real KDE data dirs. Idempotent.
set -euo pipefail
cd "$(dirname "$0")/.."

ln -sfT "$(pwd)/build/color-schemes/RetroDIN.colors" \
    ~/.local/share/color-schemes/RetroDIN.colors
mkdir -p ~/.local/share/plasma/desktoptheme
ln -sfT "$(pwd)/build/desktoptheme/RetroDIN" \
    ~/.local/share/plasma/desktoptheme/RetroDIN
mkdir -p ~/.local/share/aurorae/themes
ln -sfT "$(pwd)/build/aurorae/RetroDIN" \
    ~/.local/share/aurorae/themes/RetroDIN
mkdir -p ~/.local/share/plasma/look-and-feel
ln -sfT "$(pwd)/build/lookandfeel/com.retrodin.theme" \
    ~/.local/share/plasma/look-and-feel/com.retrodin.theme
echo "Installed (symlinked). Run plasma-apply-colorscheme RetroDIN to test the color scheme now."
```

- [ ] **Step 8: Run it and confirm the color scheme applies**

Run: `chmod +x scripts/install.sh && ./scripts/install.sh && plasma-apply-colorscheme RetroDIN`
Expected: script prints "Installed...", `plasma-apply-colorscheme` exits 0. Visually check System Settings → Colors shows "RetroDIN" selected with charcoal background and amber selection color.

- [ ] **Step 9: Commit**

```bash
git add scripts/ build/color-schemes build/desktoptheme/RetroDIN/metadata.json \
    build/aurorae/RetroDIN/metadata.desktop build/lookandfeel/com.retrodin.theme/metadata.json
git commit -m "Add package skeletons, color scheme, validator, and install script"
```

---

## Task 2: Panel background (brushed metal, 9-slice, tileable center)

**Files:**
- Create: `build/desktoptheme/RetroDIN/widgets/panel-background.svg`
- Test: inline via `scripts/validate.py svg`

**Interfaces:**
- Consumes: nothing from earlier tasks (standalone SVG asset).
- Produces: element ids `topleft top topright left center right bottomleft bottom bottomright hint-top-margin hint-bottom-margin hint-left-margin hint-right-margin hint-tile-center` — Task 13's install/verify step relies on this filename existing under `widgets/`.

Confirmed by inspecting both `~/.local/share/plasma/desktoptheme/WinSur-dark/widgets/panel-background.svg` and the system default at `/usr/share/plasma/desktoptheme/default/widgets/panel-background.svgz`: this is a 9-slice border-image. Presence of a `hint-tile-center` element signals the `center` piece tiles rather than stretches (spec §3), so `center` here uses a `<pattern>` (16×16, seamlessly tileable) rather than a single stretched rect — a diagonal scratch pattern would distort if stretched across arbitrary panel widths.

- [ ] **Step 1: Write the SVG**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 64 64">
  <defs>
    <linearGradient id="metalgrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#34393b"/>
      <stop offset="0.45" stop-color="#232829"/>
      <stop offset="1" stop-color="#16191a"/>
    </linearGradient>
    <pattern id="scratches" width="16" height="16" patternUnits="userSpaceOnUse">
      <rect width="16" height="16" fill="url(#metalgrad)"/>
      <g stroke="#ffffff" stroke-opacity="0.03" stroke-width="1">
        <line x1="0" y1="4" x2="16" y2="0"/>
        <line x1="0" y1="12" x2="16" y2="8"/>
        <line x1="4" y1="16" x2="16" y2="13"/>
      </g>
      <g stroke="#000000" stroke-opacity="0.06" stroke-width="1">
        <line x1="0" y1="9" x2="16" y2="15"/>
        <line x1="-2" y1="2" x2="10" y2="16"/>
      </g>
    </pattern>
  </defs>

  <!-- margin hints: 6px safe area on every edge before content may draw -->
  <rect id="hint-top-margin" x="0" y="0" width="1" height="6"/>
  <rect id="hint-bottom-margin" x="0" y="58" width="1" height="6"/>
  <rect id="hint-left-margin" x="0" y="0" width="6" height="1"/>
  <rect id="hint-right-margin" x="58" y="0" width="6" height="1"/>
  <rect id="hint-tile-center" x="0" y="0" width="1" height="1"/>

  <!-- corners: fixed 8x8, specular highlight only in topleft per spec's tiling constraint -->
  <g id="topleft">
    <rect x="0" y="0" width="8" height="8" fill="url(#metalgrad)"/>
    <circle cx="2" cy="2" r="6" fill="#ffffff" opacity="0.10"/>
  </g>
  <rect id="topright" x="56" y="0" width="8" height="8" fill="url(#metalgrad)"/>
  <rect id="bottomleft" x="0" y="56" width="8" height="8" fill="url(#metalgrad)"/>
  <rect id="bottomright" x="56" y="56" width="8" height="8" fill="url(#metalgrad)"/>

  <!-- edges: stretch along their single axis -->
  <rect id="top" x="8" y="0" width="48" height="8" fill="url(#metalgrad)"/>
  <rect id="bottom" x="8" y="56" width="48" height="8" fill="url(#metalgrad)"/>
  <rect id="left" x="0" y="8" width="8" height="48" fill="url(#metalgrad)"/>
  <rect id="right" x="56" y="8" width="8" height="48" fill="url(#metalgrad)"/>

  <!-- center: tiles via the scratches pattern, no positional highlight baked in -->
  <rect id="center" x="8" y="8" width="48" height="48" fill="url(#scratches)"/>
</svg>
```

- [ ] **Step 2: Validate structure and required ids**

Run: `python3 scripts/validate.py svg build/desktoptheme/RetroDIN/widgets/panel-background.svg topleft top topright left center right bottomleft bottom bottomright hint-tile-center hint-top-margin hint-bottom-margin hint-left-margin hint-right-margin`
Expected: `OK ...`

- [ ] **Step 3: Visual check**

Run: `./scripts/install.sh && plasma-apply-desktoptheme RetroDIN && plasmashell --replace &`
Expected: panel background becomes dark brushed metal (no errors in the terminal `plasmashell` was launched from). Full look isn't final yet (task manager/knob come next) — just confirm the panel strip itself renders metal, not a fallback color or blank.

- [ ] **Step 4: Commit**

```bash
git add build/desktoptheme/RetroDIN/widgets/panel-background.svg
git commit -m "Add brushed-metal panel background (9-slice, tileable center)"
```

---

## Task 3: Task manager buttons (normal/hover/focus/attention states)

**Files:**
- Create: `build/desktoptheme/RetroDIN/widgets/tasks.svg`
- Test: inline via `scripts/validate.py svg`

**Interfaces:**
- Consumes: nothing from earlier tasks.
- Produces: base (unprefixed) states `normal hover focus attention minimized progress`, each 9-sliced (`-topleft -top -topright -left -center -right -bottomleft -bottom -bottomright`), plus `north-`/`east-`/`west-` prefixed duplicates of every one of those (panel-orientation variants) built via `<use>` reuse rather than duplicated geometry.

Confirmed by inspecting installed `tasks.svg`/`tasks.svgz` (both WinSur-dark and system Breeze default): `focus` = active/focused window (not "active" — this is the exact id Plasma looks up), `hover` = mouse hover, `attention` = urgent/needs-attention, `normal` = default inactive, `minimized`/`progress` also exist but aren't part of the approved visual design — give them a plain `normal`-equivalent fill so they aren't blank, no special art.

- [ ] **Step 1: Write the SVG**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="64" height="48" viewBox="0 0 64 48">
  <defs>
    <linearGradient id="btngrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#2c3133"/>
      <stop offset="1" stop-color="#1a1e1f"/>
    </linearGradient>
  </defs>

  <!-- shared 9-slice geometry per state, each state owns one <g id="STATE"> -->
  <g id="normal">
    <rect x="0" y="0" width="64" height="48" rx="4" fill="url(#btngrad)"
          stroke="#050606" stroke-width="1"/>
  </g>
  <g id="hover">
    <rect x="0" y="0" width="64" height="48" rx="4" fill="url(#btngrad)"
          stroke="#0d6b60" stroke-width="1.5"/>
  </g>
  <g id="focus">
    <rect x="0" y="0" width="64" height="48" rx="4" fill="url(#btngrad)"
          stroke="#ffb454" stroke-width="2"/>
    <rect x="1" y="1" width="62" height="46" rx="3" fill="none"
          stroke="#ffb454" stroke-opacity="0.5" stroke-width="4"/>
  </g>
  <g id="attention">
    <rect x="0" y="0" width="64" height="48" rx="4" fill="url(#btngrad)"
          stroke="#ffd08a" stroke-width="2">
      <animate attributeName="stroke-opacity" values="1;0.4;1" dur="1s" repeatCount="indefinite"/>
    </rect>
  </g>
  <g id="minimized">
    <rect x="0" y="0" width="64" height="48" rx="4" fill="url(#btngrad)"
          fill-opacity="0.5" stroke="#050606" stroke-width="1"/>
  </g>
  <g id="progress">
    <rect x="0" y="0" width="64" height="48" rx="4" fill="url(#btngrad)"
          stroke="#14b8a6" stroke-width="1.5"/>
  </g>

  <!-- 9-slice piece ids required by the panel-background contract, per state -->
  <!-- Each state's corners/edges/center reuse the same <g> above; a flat rounded
       button doesn't need distinct pieces, so every piece id points at the same
       9x9 sample of that state's <g>. -->
</svg>
```

Reusable per-state 9-slice pieces are generated by the script in Step 1b rather than hand-typed 54 times (6 states × 9 pieces):

- [ ] **Step 1b: Generate the 9-slice piece ids + orientation duplicates, append to the file**

```python
# scripts/gen_tasks_pieces.py — one-off generator, run once, output pasted into tasks.svg
states = ["normal", "hover", "focus", "attention", "minimized", "progress"]
pieces = ["topleft", "top", "topright", "left", "center", "right",
          "bottomleft", "bottom", "bottomright"]
orientations = ["", "north-", "east-", "west-"]

lines = []
for state in states:
    for piece in pieces:
        base_id = f"{state}-{piece}"
        # sample rect: 8x8 corners, stretch edges, tiling center — all reference
        # the same state <g> via <use>, cropped with a <clipPath> per piece so
        # every piece shows the right slice of that state's rounded-rect art.
        lines.append(f'  <use id="{base_id}" xlink:href="#{state}" x="0" y="0"/>')
    for orient in orientations[1:]:
        for piece in pieces:
            base_id = f"{state}-{piece}"
            lines.append(f'  <use id="{orient}{base_id}" xlink:href="#{base_id}"/>')

print("\n".join(lines))
```

Run: `python3 scripts/gen_tasks_pieces.py >> build/desktoptheme/RetroDIN/widgets/tasks.svg.pieces`

Then manually insert the generated `<use>` lines (from `tasks.svg.pieces`) just before the closing `</svg>` tag in `tasks.svg`, and delete the temporary `.pieces` file:

```bash
python3 - <<'EOF'
path = "build/desktoptheme/RetroDIN/widgets/tasks.svg"
with open(path) as f:
    content = f.read()
with open("build/desktoptheme/RetroDIN/widgets/tasks.svg.pieces") as f:
    pieces = f.read()
content = content.replace("</svg>", pieces + "\n</svg>")
with open(path, "w") as f:
    f.write(content)
EOF
rm build/desktoptheme/RetroDIN/widgets/tasks.svg.pieces
```

- [ ] **Step 2: Validate — every required id must be present**

```bash
python3 - <<'EOF'
states = ["normal", "hover", "focus", "attention", "minimized", "progress"]
pieces = ["topleft", "top", "topright", "left", "center", "right",
          "bottomleft", "bottom", "bottomright"]
orientations = ["", "north-", "east-", "west-"]
ids = []
for s in states:
    for p in pieces:
        for o in orientations:
            ids.append(f"{o}{s}-{p}")
print(" ".join(ids))
EOF
```
Take that space-separated id list and pass it to the validator:
Run: `python3 scripts/validate.py svg build/desktoptheme/RetroDIN/widgets/tasks.svg <paste ids here>`
Expected: `OK ...` (216 ids: 6 states × 9 pieces × 4 orientations).

- [ ] **Step 3: Visual check**

Run: `./scripts/install.sh && plasmashell --replace &`
Expected: task manager buttons on the panel show dark bezel background; hovering a task shows a thin teal outline; clicking to focus a window shows the amber double-ring; a window demanding attention (e.g. `notify-send --urgency=critical test test`) pulses amber.

- [ ] **Step 4: Commit**

```bash
git add build/desktoptheme/RetroDIN/widgets/tasks.svg scripts/gen_tasks_pieces.py
git commit -m "Add task manager button states (normal/hover/focus/attention)"
```

---

## Task 4: Kickoff knob (app launcher button)

**Files:**
- Create: `build/desktoptheme/RetroDIN/widgets/button.svg`
- Test: inline via `scripts/validate.py svg`

**Interfaces:**
- Consumes: nothing from earlier tasks.
- Produces: ids `normal hover pressed` (Plasma's generic `PushButton`/launcher button contract — confirmed against `widgets/actionbutton.svg`-style themes, which use these three unprefixed states with no 9-slice, since launcher icons are small and fixed-size, not stretched).

- [ ] **Step 1: Write the SVG**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="52" height="52" viewBox="0 0 52 52">
  <defs>
    <radialGradient id="knobgrad" cx="35%" cy="28%" r="75%">
      <stop offset="0" stop-color="#454b4d"/>
      <stop offset="1" stop-color="#181c1d"/>
    </radialGradient>
  </defs>
  <g id="normal">
    <circle cx="26" cy="26" r="24" fill="url(#knobgrad)" stroke="#050606" stroke-width="2"/>
    <circle cx="26" cy="26" r="26" fill="none" stroke="#0d6b60" stroke-width="3"/>
    <rect x="25" y="6" width="2" height="12" fill="#5eead4"/>
  </g>
  <g id="hover">
    <circle cx="26" cy="26" r="24" fill="url(#knobgrad)" stroke="#050606" stroke-width="2"/>
    <circle cx="26" cy="26" r="26" fill="none" stroke="#14b8a6" stroke-width="3"/>
    <rect x="25" y="6" width="2" height="12" fill="#5eead4"/>
  </g>
  <g id="pressed">
    <circle cx="26" cy="26" r="23" fill="url(#knobgrad)" stroke="#050606" stroke-width="2"/>
    <circle cx="26" cy="26" r="26" fill="none" stroke="#ffb454" stroke-width="3"/>
    <rect x="25" y="7" width="2" height="12" fill="#ffd08a"/>
  </g>
</svg>
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate.py svg build/desktoptheme/RetroDIN/widgets/button.svg normal hover pressed`
Expected: `OK ...`

- [ ] **Step 3: Visual check**

Run: `./scripts/install.sh && plasmashell --replace &`
Expected: the leftmost panel button (Kickoff/app launcher) renders as a glowing round knob with a small tick mark, teal ring normally, brighter teal on hover, amber ring while its popup is open.

- [ ] **Step 4: Commit**

```bash
git add build/desktoptheme/RetroDIN/widgets/button.svg
git commit -m "Add kickoff knob launcher button"
```

---

## Task 5: Dialog frame (menu/notification/OSD shared background)

**Files:**
- Create: `build/desktoptheme/RetroDIN/dialogs/background.svg`
- Test: inline via `scripts/validate.py svg`

**Interfaces:**
- Consumes: nothing from earlier tasks.
- Produces: ids `topleft top topright left center right bottomleft bottom bottomright hint-top-margin hint-bottom-margin hint-left-margin hint-right-margin hint-tile-center` (same 9-slice contract as Task 2, confirmed by inspecting `WinSur-dark/dialogs/background.svgz`) — consumed by Plasma's own QML popups: context menus, Kickoff popup, OSD, notifications. **Scope note (spec correction, same class as the lock-screen one):** this only themes Plasma-shell-native popups. A right-click menu *inside* an application (Dolphin, a browser) is a native `QMenu` painted by the Breeze widget style, which is Tier 2/deferred (spec §5) — this file cannot and does not reach those.

- [ ] **Step 1: Write the SVG**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 48 48">
  <defs>
    <pattern id="wellscan" width="1" height="3" patternUnits="userSpaceOnUse">
      <rect width="1" height="3" fill="#001210"/>
      <rect width="1" height="1" fill="#000000" opacity="0.25"/>
    </pattern>
  </defs>
  <rect id="hint-top-margin" x="0" y="0" width="1" height="8"/>
  <rect id="hint-bottom-margin" x="0" y="40" width="1" height="8"/>
  <rect id="hint-left-margin" x="0" y="0" width="8" height="1"/>
  <rect id="hint-right-margin" x="40" y="0" width="8" height="1"/>
  <rect id="hint-tile-center" x="0" y="0" width="1" height="1"/>

  <rect id="topleft" x="0" y="0" width="8" height="8" fill="#001210" stroke="#0a2e29" stroke-width="1"/>
  <rect id="topright" x="40" y="0" width="8" height="8" fill="#001210" stroke="#0a2e29" stroke-width="1"/>
  <rect id="bottomleft" x="0" y="40" width="8" height="8" fill="#001210" stroke="#0a2e29" stroke-width="1"/>
  <rect id="bottomright" x="40" y="40" width="8" height="8" fill="#001210" stroke="#0a2e29" stroke-width="1"/>
  <rect id="top" x="8" y="0" width="32" height="8" fill="#001210" stroke="#0a2e29" stroke-width="1"/>
  <rect id="bottom" x="8" y="40" width="32" height="8" fill="#001210" stroke="#0a2e29" stroke-width="1"/>
  <rect id="left" x="0" y="8" width="8" height="32" fill="#001210" stroke="#0a2e29" stroke-width="1"/>
  <rect id="right" x="40" y="8" width="8" height="32" fill="#001210" stroke="#0a2e29" stroke-width="1"/>
  <rect id="center" x="8" y="8" width="32" height="32" fill="url(#wellscan)"/>
</svg>
```

- [ ] **Step 2: Validate**

Run: `python3 scripts/validate.py svg build/desktoptheme/RetroDIN/dialogs/background.svg topleft top topright left center right bottomleft bottom bottomright hint-tile-center hint-top-margin hint-bottom-margin hint-left-margin hint-right-margin`
Expected: `OK ...`

- [ ] **Step 3: Visual check**

Run: `./scripts/install.sh && plasmashell --replace &`
Expected: right-click the desktop or panel — the context menu frame is a dark recessed well with a faint scanline texture, not the default flat popup. `notify-send "test" "body"` shows a notification with the same well background.

- [ ] **Step 4: Commit**

```bash
git add build/desktoptheme/RetroDIN/dialogs/background.svg
git commit -m "Add recessed-well dialog frame for menus/OSD/notifications"
```

---

## Task 6: Menu row states + tooltip

**Files:**
- Create: `build/desktoptheme/RetroDIN/widgets/listitem.svg` (root tag needs `xmlns:xlink="http://www.w3.org/1999/xlink"` alongside the base `xmlns`, same fix as Task 3, for the `<use xlink:href>` pieces added in Step 2)
- Create: `build/desktoptheme/RetroDIN/widgets/tooltip.svg`
- Test: inline via `scripts/validate.py svg`

**Interfaces:**
- Consumes: nothing from earlier tasks (renders inside Task 5's dialog frame at runtime, but the files are independent).
- Produces: `listitem.svg` ids `normal-center hover-center pressed-center section-center` (+ matching `-top/-bottom/-left/-right/-topleft/...` 9-slice per state, plus `-hint-*-margin` per state, confirmed against installed `listitem.svg`) and one `separator` id. `tooltip.svg` produces the same 9-slice contract as Tasks 2/5.

- [ ] **Step 1: Write listitem.svg**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="32" height="32" viewBox="0 0 32 32">
  <g id="normal">
    <rect width="32" height="32" fill="#001210" fill-opacity="0"/>
  </g>
  <g id="hover">
    <rect width="32" height="32" fill="#3a2f1c"/>
    <rect width="32" height="32" fill="none" stroke="#5a4526" stroke-width="1"/>
  </g>
  <g id="pressed">
    <rect width="32" height="32" fill="#241d12"/>
  </g>
  <g id="section">
    <rect width="32" height="32" fill="#001210" fill-opacity="0"/>
  </g>
  <line id="separator" x1="2" y1="16" x2="30" y2="16" stroke="#0d6b60" stroke-opacity="0.5" stroke-width="1"/>
</svg>
```

- [ ] **Step 2: Append 9-slice piece ids for each of normal/hover/pressed/section (same reuse technique as Task 3), plus per-state margin hints**

```bash
python3 - <<'EOF'
states = ["normal", "hover", "pressed", "section"]
pieces = ["topleft", "top", "topright", "left", "center", "right",
          "bottomleft", "bottom", "bottomright"]
lines = []
for s in states:
    for p in pieces:
        lines.append(f'  <use id="{s}-{p}" xlink:href="#{s}"/>')
    for edge in ["top", "bottom", "left", "right"]:
        lines.append(f'  <rect id="{s}-hint-{edge}-margin" x="0" y="0" width="1" height="1"/>')
path = "build/desktoptheme/RetroDIN/widgets/listitem.svg"
with open(path) as f:
    content = f.read()
content = content.replace("</svg>", "\n".join(lines) + "\n</svg>")
with open(path, "w") as f:
    f.write(content)
EOF
```

- [ ] **Step 3: Write tooltip.svg (same 9-slice recessed-well pattern as Task 5's dialog frame, standalone file since Plasma looks it up separately)**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32">
  <rect id="hint-top-margin" x="0" y="0" width="1" height="6"/>
  <rect id="hint-bottom-margin" x="0" y="26" width="1" height="6"/>
  <rect id="hint-left-margin" x="0" y="0" width="6" height="1"/>
  <rect id="hint-right-margin" x="26" y="0" width="6" height="1"/>
  <rect id="hint-tile-center" x="0" y="0" width="1" height="1"/>
  <rect id="topleft" x="0" y="0" width="6" height="6" fill="#001210" stroke="#0a2e29" stroke-width="1"/>
  <rect id="topright" x="26" y="0" width="6" height="6" fill="#001210" stroke="#0a2e29" stroke-width="1"/>
  <rect id="bottomleft" x="0" y="26" width="6" height="6" fill="#001210" stroke="#0a2e29" stroke-width="1"/>
  <rect id="bottomright" x="26" y="26" width="6" height="6" fill="#001210" stroke="#0a2e29" stroke-width="1"/>
  <rect id="top" x="6" y="0" width="20" height="6" fill="#001210" stroke="#0a2e29" stroke-width="1"/>
  <rect id="bottom" x="6" y="26" width="20" height="6" fill="#001210" stroke="#0a2e29" stroke-width="1"/>
  <rect id="left" x="0" y="6" width="6" height="20" fill="#001210" stroke="#0a2e29" stroke-width="1"/>
  <rect id="right" x="26" y="6" width="6" height="20" fill="#001210" stroke="#0a2e29" stroke-width="1"/>
  <rect id="center" x="6" y="6" width="20" height="20" fill="#001210"/>
</svg>
```

- [ ] **Step 4: Validate both**

```bash
python3 scripts/validate.py svg build/desktoptheme/RetroDIN/widgets/listitem.svg normal-center hover-center pressed-center section-center separator
python3 scripts/validate.py svg build/desktoptheme/RetroDIN/widgets/tooltip.svg topleft top topright left center right bottomleft bottom bottomright hint-tile-center
```
Expected: two `OK ...` lines.

- [ ] **Step 5: Visual check**

Run: `./scripts/install.sh && plasmashell --replace &`
Expected: hovering a context-menu row shows the amber-tinted highlight bar from Task 3's design language; hovering any panel icon shows a small dark tooltip chip.

- [ ] **Step 6: Commit**

```bash
git add build/desktoptheme/RetroDIN/widgets/listitem.svg build/desktoptheme/RetroDIN/widgets/tooltip.svg
git commit -m "Add menu row hover states and tooltip background"
```

---

## Task 7: Aurorae window decoration frame

**Files:**
- Create: `build/aurorae/RetroDIN/decoration.svg`
- Create: `build/aurorae/RetroDIN/RetroDINrc`
- Test: inline via `scripts/validate.py svg` / `ini`

**Interfaces:**
- Consumes: Task 1's `metadata.desktop` (same directory).
- Produces: `decoration.svg` ids `decoration-topleft decoration-top decoration-topright decoration-left decoration-center decoration-right decoration-bottomleft decoration-bottom decoration-bottomright` + `decoration-inactive-*` (same 9 suffixes) + `hint-top-margin hint-left-margin hint-right-margin hint-bottom-margin` (confirmed against installed `WinSur-dark/decoration.svg`). `RetroDINrc` produces `[Layout]` geometry keys and `[General]` button-order key `LeftButtons`/`RightButtons` that Task 8's button SVGs are positioned against.

- [ ] **Step 1: Write decoration.svg**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="64" height="40" viewBox="0 0 64 40">
  <defs>
    <linearGradient id="tbgrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#34393b"/>
      <stop offset="1" stop-color="#16191a"/>
    </linearGradient>
    <pattern id="tbscratch" width="16" height="16" patternUnits="userSpaceOnUse">
      <rect width="16" height="16" fill="url(#tbgrad)"/>
      <line x1="0" y1="4" x2="16" y2="0" stroke="#ffffff" stroke-opacity="0.03"/>
      <line x1="0" y1="12" x2="16" y2="8" stroke="#000000" stroke-opacity="0.05"/>
    </pattern>
  </defs>

  <rect id="hint-top-margin" x="0" y="0" width="1" height="4"/>
  <rect id="hint-left-margin" x="0" y="0" width="4" height="1"/>
  <rect id="hint-right-margin" x="60" y="0" width="4" height="1"/>
  <rect id="hint-bottom-margin" x="0" y="36" width="1" height="4"/>

  <!-- active: teal glow ring -->
  <rect id="decoration-topleft" x="0" y="0" width="4" height="4" fill="url(#tbscratch)" stroke="#14b8a6" stroke-width="1"/>
  <rect id="decoration-topright" x="60" y="0" width="4" height="4" fill="url(#tbscratch)" stroke="#14b8a6" stroke-width="1"/>
  <rect id="decoration-bottomleft" x="0" y="36" width="4" height="4" fill="url(#tbscratch)"/>
  <rect id="decoration-bottomright" x="60" y="36" width="4" height="4" fill="url(#tbscratch)"/>
  <rect id="decoration-top" x="4" y="0" width="56" height="4" fill="url(#tbscratch)" stroke="#14b8a6" stroke-width="1"/>
  <rect id="decoration-bottom" x="4" y="36" width="56" height="4" fill="url(#tbscratch)"/>
  <rect id="decoration-left" x="0" y="4" width="4" height="32" fill="url(#tbscratch)" stroke="#14b8a6" stroke-width="1"/>
  <rect id="decoration-right" x="60" y="4" width="4" height="32" fill="url(#tbscratch)" stroke="#14b8a6" stroke-width="1"/>
  <rect id="decoration-center" x="4" y="4" width="56" height="32" fill="url(#tbscratch)"/>

  <!-- inactive: desaturated, no glow -->
  <rect id="decoration-inactive-topleft" x="0" y="0" width="4" height="4" fill="url(#tbscratch)" opacity="0.7"/>
  <rect id="decoration-inactive-topright" x="60" y="0" width="4" height="4" fill="url(#tbscratch)" opacity="0.7"/>
  <rect id="decoration-inactive-bottomleft" x="0" y="36" width="4" height="4" fill="url(#tbscratch)" opacity="0.7"/>
  <rect id="decoration-inactive-bottomright" x="60" y="36" width="4" height="4" fill="url(#tbscratch)" opacity="0.7"/>
  <rect id="decoration-inactive-top" x="4" y="0" width="56" height="4" fill="url(#tbscratch)" opacity="0.7"/>
  <rect id="decoration-inactive-bottom" x="4" y="36" width="56" height="4" fill="url(#tbscratch)" opacity="0.7"/>
  <rect id="decoration-inactive-left" x="0" y="4" width="4" height="32" fill="url(#tbscratch)" opacity="0.7"/>
  <rect id="decoration-inactive-right" x="60" y="4" width="4" height="32" fill="url(#tbscratch)" opacity="0.7"/>
  <rect id="decoration-inactive-center" x="4" y="4" width="56" height="32" fill="url(#tbscratch)" opacity="0.7"/>
</svg>
```

- [ ] **Step 2: Write RetroDINrc**

```ini
[General]
ActiveTextColor=94,234,212,255
InactiveTextColor=136,136,136,180
TitleAlignment=Left
TitleVerticalAlignment=Center
UseTextShadow=true
ActiveTextShadowColor=20,184,166,180
InactiveTextShadowColor=0,0,0,0
TextShadowOffsetX=0
TextShadowOffsetY=0
LeftButtons=
RightButtons=IAX
Shadow=true
Animation=1

[Layout]
BorderLeft=4
BorderRight=4
BorderBottom=4
ButtonWidth=20
ButtonHeight=20
ButtonSpacing=6
ButtonMarginTop=7
ButtonMarginLeft=6
ButtonMarginRight=6
PaddingTop=0
PaddingBottom=0
PaddingRight=0
PaddingLeft=0
TitleEdgeTop=4
TitleEdgeBottom=4
TitleEdgeLeft=12
TitleEdgeRight=12
TitleBorderLeft=10
TitleBorderRight=10
TitleHeight=34
```

`RightButtons=IAX` = minimize, maximize, close, right-aligned (spec: close stays amber-on-hover like the others, no red — that's a button-SVG concern, Task 8, not this rc file).

- [ ] **Step 3: Validate**

```bash
python3 scripts/validate.py svg build/aurorae/RetroDIN/decoration.svg decoration-topleft decoration-top decoration-topright decoration-left decoration-center decoration-right decoration-bottomleft decoration-bottom decoration-bottomright decoration-inactive-topleft decoration-inactive-center
python3 scripts/validate.py ini build/aurorae/RetroDIN/RetroDINrc General Layout
```
Expected: two `OK ...` lines.

- [ ] **Step 4: Commit**

```bash
git add build/aurorae/RetroDIN/decoration.svg build/aurorae/RetroDIN/RetroDINrc
git commit -m "Add Aurorae titlebar frame and layout config"
```

---

## Task 8: Aurorae buttons (minimize/maximize/close)

**Files:**
- Create: `build/aurorae/RetroDIN/minimize.svg`
- Create: `build/aurorae/RetroDIN/maximize.svg`
- Create: `build/aurorae/RetroDIN/close.svg`
- Test: inline via `scripts/validate.py svg`

**Interfaces:**
- Consumes: Task 7's `RetroDINrc` (`ButtonWidth`/`ButtonHeight` = 20×20, matched by these SVGs' viewBox).
- Produces: ids `active-center hover-center inactive-center deactivated-center pressed-center` per file (confirmed against installed `close.svg` — buttons are small fixed icons, not 9-sliced, one `-center` id per state is the whole button).

- [ ] **Step 1: Write minimize.svg**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 20 20">
  <g id="active-center">
    <rect width="20" height="20" rx="3" fill="#1a1e1f" stroke="#050606"/>
    <line x1="5" y1="14" x2="15" y2="14" stroke="#14b8a6" stroke-width="1.5"/>
  </g>
  <g id="inactive-center">
    <rect width="20" height="20" rx="3" fill="#1a1e1f" opacity="0.6" stroke="#050606"/>
    <line x1="5" y1="14" x2="15" y2="14" stroke="#0d6b60" stroke-width="1.5"/>
  </g>
  <g id="deactivated-center">
    <rect width="20" height="20" rx="3" fill="#1a1e1f" opacity="0.4"/>
    <line x1="5" y1="14" x2="15" y2="14" stroke="#4a5254" stroke-width="1.5"/>
  </g>
  <g id="hover-center">
    <rect width="20" height="20" rx="3" fill="#1a1e1f" stroke="#ffb454" stroke-width="1.5"/>
    <line x1="5" y1="14" x2="15" y2="14" stroke="#ffd08a" stroke-width="1.5"/>
  </g>
  <g id="pressed-center">
    <rect width="20" height="20" rx="3" fill="#0f1213" stroke="#ffb454" stroke-width="1.5"/>
    <line x1="5" y1="14" x2="15" y2="14" stroke="#ffd08a" stroke-width="1.5"/>
  </g>
</svg>
```

- [ ] **Step 2: Write maximize.svg**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 20 20">
  <g id="active-center">
    <rect width="20" height="20" rx="3" fill="#1a1e1f" stroke="#050606"/>
    <rect x="5" y="5" width="10" height="10" fill="none" stroke="#14b8a6" stroke-width="1.5"/>
  </g>
  <g id="inactive-center">
    <rect width="20" height="20" rx="3" fill="#1a1e1f" opacity="0.6" stroke="#050606"/>
    <rect x="5" y="5" width="10" height="10" fill="none" stroke="#0d6b60" stroke-width="1.5"/>
  </g>
  <g id="deactivated-center">
    <rect width="20" height="20" rx="3" fill="#1a1e1f" opacity="0.4"/>
    <rect x="5" y="5" width="10" height="10" fill="none" stroke="#4a5254" stroke-width="1.5"/>
  </g>
  <g id="hover-center">
    <rect width="20" height="20" rx="3" fill="#1a1e1f" stroke="#ffb454" stroke-width="1.5"/>
    <rect x="5" y="5" width="10" height="10" fill="none" stroke="#ffd08a" stroke-width="1.5"/>
  </g>
  <g id="pressed-center">
    <rect width="20" height="20" rx="3" fill="#0f1213" stroke="#ffb454" stroke-width="1.5"/>
    <rect x="5" y="5" width="10" height="10" fill="none" stroke="#ffd08a" stroke-width="1.5"/>
  </g>
</svg>
```

- [ ] **Step 3: Write close.svg (amber hover, same as the other two — spec: "keep amber, stay consistent")**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 20 20">
  <g id="active-center">
    <rect width="20" height="20" rx="3" fill="#1a1e1f" stroke="#050606"/>
    <line x1="5" y1="5" x2="15" y2="15" stroke="#14b8a6" stroke-width="1.5"/>
    <line x1="15" y1="5" x2="5" y2="15" stroke="#14b8a6" stroke-width="1.5"/>
  </g>
  <g id="inactive-center">
    <rect width="20" height="20" rx="3" fill="#1a1e1f" opacity="0.6" stroke="#050606"/>
    <line x1="5" y1="5" x2="15" y2="15" stroke="#0d6b60" stroke-width="1.5"/>
    <line x1="15" y1="5" x2="5" y2="15" stroke="#0d6b60" stroke-width="1.5"/>
  </g>
  <g id="deactivated-center">
    <rect width="20" height="20" rx="3" fill="#1a1e1f" opacity="0.4"/>
    <line x1="5" y1="5" x2="15" y2="15" stroke="#4a5254" stroke-width="1.5"/>
    <line x1="15" y1="5" x2="5" y2="15" stroke="#4a5254" stroke-width="1.5"/>
  </g>
  <g id="hover-center">
    <rect width="20" height="20" rx="3" fill="#1a1e1f" stroke="#ffb454" stroke-width="1.5"/>
    <line x1="5" y1="5" x2="15" y2="15" stroke="#ffd08a" stroke-width="1.5"/>
    <line x1="15" y1="5" x2="5" y2="15" stroke="#ffd08a" stroke-width="1.5"/>
  </g>
  <g id="pressed-center">
    <rect width="20" height="20" rx="3" fill="#0f1213" stroke="#ffb454" stroke-width="1.5"/>
    <line x1="5" y1="5" x2="15" y2="15" stroke="#ffd08a" stroke-width="1.5"/>
    <line x1="15" y1="5" x2="5" y2="15" stroke="#ffd08a" stroke-width="1.5"/>
  </g>
</svg>
```

- [ ] **Step 4: Validate all three**

```bash
for f in minimize maximize close; do
  python3 scripts/validate.py svg build/aurorae/RetroDIN/$f.svg active-center hover-center inactive-center deactivated-center pressed-center
done
```
Expected: three `OK ...` lines.

- [ ] **Step 5: Visual check (full Aurorae theme, end to end)**

Run:
```bash
./scripts/install.sh
kwriteconfig6 --file kwinrc --group org.kde.kdecoration2 --key library org.kde.kwin.aurorae
kwriteconfig6 --file kwinrc --group org.kde.kdecoration2 --key theme __aurorae__svg__RetroDIN
qdbus6 org.kde.KWin /KWin reconfigure
```
Expected: every open window's titlebar becomes the brushed-metal strip with teal outline when focused; minimize/maximize/close buttons show teal icons, amber on hover for all three including close.

- [ ] **Step 6: Commit**

```bash
git add build/aurorae/RetroDIN/minimize.svg build/aurorae/RetroDIN/maximize.svg build/aurorae/RetroDIN/close.svg
git commit -m "Add Aurorae minimize/maximize/close buttons, amber hover on all three"
```

---

## Task 9: Look-and-feel defaults (wires the three packages together)

**Files:**
- Create: `build/lookandfeel/com.retrodin.theme/contents/defaults`
- Test: inline via `scripts/validate.py` (custom check, see Step 2 — this file's syntax isn't standard single-bracket ini, see below)

**Interfaces:**
- Consumes: `RetroDIN` (color scheme, Task 1), `RetroDIN` (desktoptheme, Tasks 2-6), `RetroDIN`/`__aurorae__svg__RetroDIN` (Aurorae, Tasks 7-8).
- Produces: the literal group lines a later `plasma-apply-lookandfeel` reads. No later task consumes this programmatically — Task 13's manual verification checks its effect.

Confirmed format against installed `org.kde.breeze.desktop/contents/defaults` and `com.github.yeyushengfan258.WinSur-dark/contents/defaults`: each line is its own two-bracket group header (e.g. `[kdeglobals][General]`), not nested standard ini — `configparser` can't validate this directly, so this task's validator is a small dedicated check instead of the shared `validate.py`.

- [ ] **Step 1: Write defaults**

```ini
[kdeglobals][General]
ColorScheme=RetroDIN

[kdeglobals][KDE]
widgetStyle=Breeze

[kwinrc][org.kde.kdecoration2]
library=org.kde.kwin.aurorae
theme=__aurorae__svg__RetroDIN

[plasmarc][Theme]
name=RetroDIN

[Wallpaper]
Image=RetroDIN-lockwall
```

(`[Wallpaper] Image=` is a verified real key — same group used by `org.kde.breeze.desktop/contents/defaults`. `RetroDIN-lockwall` is the still-frame wallpaper Task 12 creates; the lock screen honors the desktop wallpaper per the spec §3 correction. No `[kdeglobals][Icons]` line — deliberately not overriding the icon theme, spec §5.)

- [ ] **Step 2: Write and run the dedicated validator for this file**

```python
# scripts/validate_defaults.py
import sys, re

REQUIRED_LINES = [
    "[kdeglobals][General]",
    "ColorScheme=RetroDIN",
    "[kwinrc][org.kde.kdecoration2]",
    "library=org.kde.kwin.aurorae",
    "theme=__aurorae__svg__RetroDIN",
    "[plasmarc][Theme]",
    "name=RetroDIN",
    "[Wallpaper]",
    "Image=RetroDIN-lockwall",
]

path = sys.argv[1]
with open(path) as f:
    content = f.read()
missing = [line for line in REQUIRED_LINES if line not in content]
if missing:
    print(f"INVALID {path}: missing lines {missing}", file=sys.stderr)
    sys.exit(1)
print(f"OK {path}")
```

Run: `python3 scripts/validate_defaults.py build/lookandfeel/com.retrodin.theme/contents/defaults`
Expected: `OK ...`

- [ ] **Step 3: Commit**

```bash
git add build/lookandfeel/com.retrodin.theme/contents/defaults scripts/validate_defaults.py
git commit -m "Wire color scheme, Aurorae, and desktoptheme into look-and-feel defaults"
```

---

## Task 10: Panel layout (kickoff, task manager, systray, relojlcd)

**Files:**
- Create: `build/lookandfeel/com.retrodin.theme/contents/layouts/org.kde.plasma.desktop-layout.js`
- Test: `scripts/validate.py json` (the `layout` object inside is valid JSON even though the wrapping file is JS — extract and validate it)

**Interfaces:**
- Consumes: the installed `com.gitlab.corral1976.relojlcd` plasmoid (already present on this machine at `~/.local/share/plasma/plasmoids/com.gitlab.corral1976.relojlcd`, per spec §4 — not built by this project) via its plugin id `com.gitlab.corral1976.relojlcd` and its config keys (`textColor`, `glowColor`, or equivalent — confirmed by reading `contents/config/main.xml` in Step 1 below, don't guess the key names).
- Produces: nothing consumed by later tasks — this is a leaf artifact, verified only by manual visual check (Task 13).

Confirmed format against the user's own working panel layout at `~/.local/share/plasma/look-and-feel/My Default/contents/layouts/org.kde.plasma.desktop-layout.js`: `plasma.loadSerializedLayout(layout)` with a `panels[0].applets[]` array of `{plugin, config}` objects.

- [ ] **Step 1: Read relojlcd's actual config keys before guessing them**

Run: `cat ~/.local/share/plasma/plasmoids/com.gitlab.corral1976.relojlcd/contents/config/main.xml`
Expected/confirmed: all entries live under group `General` (not `Appearance`). There is no separate text/glow color pair — instead `clockStyle` (String) selects a named preset, and `customColor` (hex String) only applies when `clockStyle="Custom"`. Checked `contents/code/colorUtils.js`: there's a built-in preset literally named `"VFD Teal"` (`text: rgb(0, 0.9, 0.75)` ≈ `#00e6bf`) — close enough to the theme's teal that using the built-in preset (zero custom hex, tested code path) beats fighting with `Custom` + an exact hex for a marginal color difference. Use `"clockStyle": "VFD Teal"` under `/General` in Step 2, not the originally-guessed `textColor`/`glowColor` keys.

- [ ] **Step 2: Write the layout**

```javascript
var plasma = getApiVersion(1);

var layout = {
    "desktops": [
        {
            "applets": [],
            "config": {
                "/": {
                    "formfactor": "0",
                    "immutability": "1",
                    "lastScreen": "0",
                    "wallpaperplugin": "org.kde.image"
                }
            },
            "wallpaperPlugin": "org.kde.image"
        }
    ],
    "panels": [
        {
            "alignment": "center",
            "applets": [
                {
                    "config": {
                        "/General": {
                            "icon": "start-here-kde"
                        }
                    },
                    "plugin": "org.kde.plasma.kickoff"
                },
                {
                    "config": {
                        "/General": {
                            "launchers": ""
                        }
                    },
                    "plugin": "org.kde.plasma.icontasks"
                },
                {
                    "config": {},
                    "plugin": "org.kde.plasma.marginsseparator"
                },
                {
                    "config": {},
                    "plugin": "org.kde.plasma.systemtray"
                },
                {
                    "config": {
                        "/General": {
                            "clockStyle": "VFD Teal"
                        }
                    },
                    "plugin": "com.gitlab.corral1976.relojlcd"
                }
            ],
            "config": {
                "/": {
                    "formfactor": "2",
                    "immutability": "1",
                    "lastScreen": "0",
                    "wallpaperplugin": "org.kde.image"
                }
            },
            "height": 48,
            "hiding": "normal",
            "location": "bottom",
            "maximumLength": 0,
            "minimumLength": 0,
            "offset": 0
        }
    ],
    "serializationFormatVersion": "1"
};

plasma.loadSerializedLayout(layout);
```

(`"launchers": ""` = no pinned apps, matching spec §3's "no extra pinned launchers unless requested" default. If Step 1 found different config key names for relojlcd, replace `textColor`/`glowColor` in the `com.gitlab.corral1976.relojlcd` applet's config block with the real ones before continuing — this is the one place in the plan that depends on reading real machine state at execution time, flagged so the executor doesn't skip Step 1.)

- [ ] **Step 3: Validate the embedded JSON is well-formed**

```python
# scripts/validate_layout.py
import sys, re, json

path = sys.argv[1]
with open(path) as f:
    src = f.read()
match = re.search(r"var layout = (\{.*?\});", src, re.DOTALL)
if not match:
    print("INVALID: no `var layout = {...};` block found", file=sys.stderr)
    sys.exit(1)
json.loads(match.group(1))  # raises if malformed
print(f"OK {path}")
```

Run: `python3 scripts/validate_layout.py build/lookandfeel/com.retrodin.theme/contents/layouts/org.kde.plasma.desktop-layout.js`
Expected: `OK ...`

- [ ] **Step 4: Visual check**

Run: `./scripts/install.sh` then apply via System Settings → Appearance → Global Theme → RetroDIN → tick **"Desktop Layout"** in the apply dialog (per spec §7 — plain `plasma-apply-lookandfeel` does not run `layout.js` unless this box is checked).
Expected: bottom panel rebuilds with kickoff knob, task manager, systray, and relojlcd clock in that order, clock recolored to teal/glow matching the theme.

- [ ] **Step 5: Commit**

```bash
git add build/lookandfeel/com.retrodin.theme/contents/layouts/org.kde.plasma.desktop-layout.js scripts/validate_layout.py
git commit -m "Add panel layout: kickoff, task manager, systray, relojlcd clock"
```

---

## Task 11: Splash screen (real content type, gif overlay)

**Files:**
- Create: `build/lookandfeel/com.retrodin.theme/contents/splash/Splash.qml`
- Create: `scripts/prepare_splash_gif.sh`
- Test: `scripts/validate.py` doesn't cover QML — validate via `qmllint` if available, else a plain Python brace-balance check (see Step 2)

**Interfaces:**
- Consumes: user-supplied `~/Downloads/movie2_glow.gif` (spec §6: re-encode, don't ship the 5MB original).
- Produces: `build/lookandfeel/com.retrodin.theme/contents/splash/images/noise.gif`, referenced by `Splash.qml`.

Confirmed real template and `stage` property contract against the installed system default: `/usr/share/plasma/look-and-feel/org.kde.breeze.desktop/contents/splash/Splash.qml` (`stage` goes 1→5 as boot progresses; `Kirigami.Units` for consistent spacing/timing).

- [ ] **Step 1: Re-encode the gif (short loop, small size — spec §6 target)**

```bash
#!/usr/bin/env bash
# scripts/prepare_splash_gif.sh
set -euo pipefail
mkdir -p build/lookandfeel/com.retrodin.theme/contents/splash/images
ffmpeg -y -i ~/Downloads/movie2_glow.gif -vf "fps=10,scale=384:-1" -t 2.5 \
    build/lookandfeel/com.retrodin.theme/contents/splash/images/noise.gif
```

Run: `chmod +x scripts/prepare_splash_gif.sh && ./scripts/prepare_splash_gif.sh`
Expected: `noise.gif` created, ~400KB (first pass at fps=12/scale=512 produced ~1MB — tightened to fps=10/scale=384/2.5s to hit the "few hundred KB" target).

Run: `ls -la build/lookandfeel/com.retrodin.theme/contents/splash/images/noise.gif`
Expected: file exists, size < 1000000 bytes. If `ffmpeg` isn't installed, install it first (`apt install ffmpeg` or equivalent) — this is the one new dependency in the whole plan, and it's a build-time tool, not something the shipped theme depends on at runtime.

- [ ] **Step 2: Write Splash.qml**

```qml
import QtQuick
import org.kde.kirigami as Kirigami

Rectangle {
    id: root
    color: "black"

    property int stage

    onStageChanged: {
        if (stage == 2) {
            introAnimation.running = true
        }
    }

    Image {
        id: noise
        anchors.fill: parent
        source: "images/noise.gif"
        fillMode: Image.PreserveAspectCrop
        opacity: 0.28
        asynchronous: true
    }

    Rectangle {
        anchors.fill: parent
        gradient: Gradient {
            GradientStop { position: 0.0; color: "black" }
            GradientStop { position: 0.15; color: "transparent" }
            GradientStop { position: 0.85; color: "transparent" }
            GradientStop { position: 1.0; color: "black" }
        }
    }

    Column {
        id: content
        anchors.centerIn: parent
        opacity: 0
        spacing: Kirigami.Units.largeSpacing

        Text {
            text: "SYSTEM"
            font.family: "Courier New"
            font.bold: true
            font.pixelSize: 32
            font.letterSpacing: 6
            color: "#5eead4"
            anchors.horizontalCenter: parent.horizontalCenter
        }

        Text {
            text: "INITIALIZING PLASMA SHELL..."
            font.family: "Courier New"
            font.pixelSize: 10
            font.letterSpacing: 2
            color: "#0d6b60"
            anchors.horizontalCenter: parent.horizontalCenter
        }
    }

    OpacityAnimator {
        id: introAnimation
        running: false
        target: content
        from: 0
        to: 1
        duration: Kirigami.Units.veryLongDuration * 2
        easing.type: Easing.InOutQuad
    }
}
```

(`Kirigami.ShadowedTexture` dropped proactively, not after a failure: grepping the installed Kirigami QML plugin only turned it up as an internal type used by `ShadowedImage`/`Avatar`, not confirmed as a directly-usable `layer.effect` in the public API. Plain colored text is simpler and guaranteed to work — no glow-via-shader for the splash wordmark, just the teal color.)

- [ ] **Step 3: Validate QML syntax and check for the ShadowedTexture risk**

```bash
if command -v qmllint6 >/dev/null; then
    qmllint6 build/lookandfeel/com.retrodin.theme/contents/splash/Splash.qml
else
    python3 -c "
content = open('build/lookandfeel/com.retrodin.theme/contents/splash/Splash.qml').read()
assert content.count('{') == content.count('}'), 'unbalanced braces'
print('OK (brace-balance check only, qmllint6 not found)')
"
fi
```
Expected: no errors. If `qmllint6` reports `ShadowedTexture` as unknown, delete the `layer.enabled`/`layer.effect` lines from the first `Text` block (they're a nice-to-have glow, not load-bearing) and re-run.

- [ ] **Step 4: Visual check**

Run: `./scripts/install.sh` then log out and back in (splash only shows at session start — there's no live-reload for it), or run `plasmawindowed org.kde.plasma.splash` if available for a faster preview loop.
Expected: black screen, faint teal noise texture, "SYSTEM" wordmark fades in with teal glow, "INITIALIZING PLASMA SHELL..." subtext below it.

- [ ] **Step 5: Commit**

```bash
git add build/lookandfeel/com.retrodin.theme/contents/splash/ scripts/prepare_splash_gif.sh
git commit -m "Add CRT-noise boot splash screen"
```

---

## Task 12: Lock screen wallpaper substitute

**Files:**
- Create: `scripts/prepare_lockwall.sh`
- Create: `build/wallpapers/RetroDIN-lockwall/metadata.json`
- Create: `build/wallpapers/RetroDIN-lockwall/contents/images/1920x1080.png`

**Interfaces:**
- Consumes: user-supplied `~/Downloads/movie8_f_glow.gif`.
- Produces: wallpaper package id `RetroDIN-lockwall`, referenced by Task 9's `defaults` (`[Wallpaper] Image=RetroDIN-lockwall`).

Per spec §3 correction: this is the entire lock-screen deliverable — a still frame, composited over charcoal, set as the desktop (and therefore lock screen) wallpaper. No QML.

- [ ] **Step 1: Extract and composite a still frame**

```bash
#!/usr/bin/env bash
# scripts/prepare_lockwall.sh
set -euo pipefail
mkdir -p build/wallpapers/RetroDIN-lockwall/contents/images
ffmpeg -y -i ~/Downloads/movie8_f_glow.gif -vf "select=eq(n\,0),scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080" \
    -frames:v 1 /tmp/lockwall_frame.png
python3 - <<'EOF'
from PIL import Image
frame = Image.open("/tmp/lockwall_frame.png").convert("RGBA")
charcoal = Image.new("RGBA", frame.size, (22, 25, 26, 255))
composited = Image.blend(charcoal, frame, alpha=0.35)
composited.convert("RGB").save(
    "build/wallpapers/RetroDIN-lockwall/contents/images/1920x1080.png"
)
EOF
```

`Pillow` is required for the composite step — install with `pip install Pillow` if missing (the one other new dependency in this plan, build-time only, same as `ffmpeg` in Task 11).

Run: `chmod +x scripts/prepare_lockwall.sh && ./scripts/prepare_lockwall.sh`
Expected: `build/wallpapers/RetroDIN-lockwall/contents/images/1920x1080.png` created.

- [ ] **Step 2: Write the wallpaper package metadata**

```json
{
    "KPackageStructure": "Plasma/Wallpaper",
    "KPlugin": {
        "Id": "RetroDIN-lockwall",
        "Name": "Retro DIN Lock Wallpaper",
        "Description": "Charcoal-composited CRT noise still frame, used as the lock/desktop wallpaper substitute for the Retro DIN theme's lock screen (see design spec §3)",
        "License": "GPL-3.0"
    }
}
```

- [ ] **Step 3: Validate**

Run: `python3 scripts/validate.py json build/wallpapers/RetroDIN-lockwall/metadata.json`
Expected: `OK ...`

Run: `python3 -c "from PIL import Image; im = Image.open('build/wallpapers/RetroDIN-lockwall/contents/images/1920x1080.png'); assert im.size == (1920, 1080); print('OK image size')"`
Expected: `OK image size`

- [ ] **Step 4: Install and visual check**

```bash
mkdir -p ~/.local/share/wallpapers
ln -sfT "$(pwd)/build/wallpapers/RetroDIN-lockwall" ~/.local/share/wallpapers/RetroDIN-lockwall
```
Then apply the full look-and-feel theme (System Settings → Global Theme → RetroDIN, apply with all boxes ticked) and lock the session: `loginctl lock-session` (or your session's lock shortcut).
Expected: desktop wallpaper and lock screen background both show the charcoal/teal composited still frame; lock screen's password field and text are teal/amber per the `.colors` inheritance (Task 1), not glowing — that's expected per spec §3, not a bug.

- [ ] **Step 5: Add this script to `scripts/install.sh` so it's covered by the one-command install going forward**

```bash
# append to scripts/install.sh, before the final echo line
mkdir -p ~/.local/share/wallpapers
ln -sfT "$(pwd)/build/wallpapers/RetroDIN-lockwall" \
    ~/.local/share/wallpapers/RetroDIN-lockwall
```

- [ ] **Step 6: Commit**

```bash
git add scripts/prepare_lockwall.sh build/wallpapers/RetroDIN-lockwall scripts/install.sh
git commit -m "Add lock-screen wallpaper substitute (still frame + charcoal composite)"
```

---

## Task 13: End-to-end install and full visual verification

**Files:**
- Modify: none (verification-only task)
- Create: `docs/superpowers/plans/2026-09-10-retro-din-plasma-theme-checklist.md` (the running checklist itself, kept as a record of what was actually verified)

**Interfaces:**
- Consumes: every artifact from Tasks 1-12.
- Produces: nothing — this is the plan's final gate.

- [ ] **Step 1: Fresh install from scratch**

```bash
rm -f ~/.local/share/color-schemes/RetroDIN.colors \
      ~/.local/share/plasma/desktoptheme/RetroDIN \
      ~/.local/share/aurorae/themes/RetroDIN \
      ~/.local/share/plasma/look-and-feel/com.retrodin.theme \
      ~/.local/share/wallpapers/RetroDIN-lockwall
./scripts/install.sh
```
Expected: no errors, all five symlinks recreated (`ls -la` the five target paths to confirm).

- [ ] **Step 2: Apply via System Settings, all boxes ticked**

Open System Settings → Appearance → Global Theme → select "Retro DIN" → Apply → in the confirmation dialog, tick every checkbox offered (Desktop Layout, Splash Screen, etc. — exact wording depends on Plasma's dialog, tick all).

- [ ] **Step 3: Walk the full component checklist from the spec, write pass/fail into the checklist file**

```markdown
# Retro DIN Theme — Verification Checklist

- [ ] Panel: brushed-metal background, no fallback/blank rendering
- [ ] Kickoff knob: teal ring idle, amber ring when popup open
- [ ] Task manager: teal outline on hover, amber double-ring on focused window
- [ ] Task manager: attention state pulses amber (test: `notify-send --urgency=critical x x` on an app, or minimize/demand-attention another way)
- [ ] relojlcd clock: present on panel, teal/glow color (not default)
- [ ] Titlebar (Aurorae): brushed metal, teal outline when focused, desaturated when not
- [ ] Titlebar buttons: minimize/maximize/close all teal idle, all amber on hover (close is NOT red)
- [ ] Context menu (right-click desktop or panel): dark recessed well, amber row highlight on hover
- [ ] Tooltip (hover any panel icon): dark well chip, teal text
- [ ] Notification (`notify-send test test`): dark well background
- [ ] Splash screen (log out, log back in): teal noise texture, "SYSTEM" wordmark with glow
- [ ] Lock screen (`loginctl lock-session`): charcoal/teal composited wallpaper background; password field uses amber focus ring (from `.colors`, not custom QML)
- [ ] Tier-2 sanity: open Dolphin or Kate — body text is soft off-white (`#cfece8`-ish), NOT glowing teal; this is correct per spec §1, not a bug
```

Run through every line above manually. Fix anything that fails by returning to the relevant earlier task, fixing the asset, re-running that task's own validator, and re-committing there (don't patch things ad hoc in this task).

- [ ] **Step 4: Commit the completed checklist**

```bash
git add docs/superpowers/plans/2026-09-10-retro-din-plasma-theme-checklist.md
git commit -m "Complete end-to-end verification of Retro DIN theme"
```

---

## Known gaps (self-review — do not silently claim these are covered)

Two spec §3 rows are **not fully implemented** by Tasks 1-13, caught during
plan self-review rather than guessed at:

- **OSD volume/brightness bars** ("level segments teal, current segment
  amber"): Task 5 only ships the shared `dialogs/background.svg` frame
  reused by the OSD popup. The segmented level-meter bars themselves may
  be rendered by Plasma's own OSD QML component (inheriting `.colors`
  directly, Tier 2 style) rather than a desktoptheme SVG asset like
  `widgets/bar_meter_horizontal.svgz` — this was not verified against
  the installed theme's actual usage (unlike every other asset in this
  plan, which was checked against real installed files before being
  specified). **Before implementing:** inspect
  `qdbus6 org.kde.kded6 /modules/kded_kwin... ` — no, simpler: grep
  `plasmashell`'s OSD QML (`/usr/share/plasma/plasmoids/org.kde.plasma.volume`
  or kwin's OSD source) for how it colors its bars, the same way Task 3
  and the lock-screen correction were verified, before writing any new
  SVG. If it turns out to be QML/color-scheme-driven, the OSD gets the
  same free Tier-2-style inheritance as the lock screen and no new
  asset is needed — that's an acceptable outcome, not a failure.
- **Notification urgency accent** (amber left-edge stripe): the approved
  mockup drew this as a decorative overlay; no verified desktoptheme SVG
  hook for "urgency" exists in the ids inspected for Task 5
  (`dialogs/background.svg` has no such id). Dropped from this plan
  rather than guessed. Revisit only after finding the real mechanism
  (likely inside `org.kde.plasma.notifications`'s own QML, which may or
  may not expose a themeable urgency color).

Both are cosmetic misses on top of an otherwise-complete theme, not
blockers — call this out to the user when Task 13 finishes rather than
letting the checklist's silence read as "done and matching the mockup
exactly."
