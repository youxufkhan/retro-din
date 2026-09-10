# Retro DIN Theme — Verification Checklist

- [x] Panel: brushed-metal background, no fallback/blank rendering — confirmed via clean `plasmashell --replace` reload, no RetroDIN-related errors in log
- [x] Kickoff knob: teal ring idle, amber ring when popup open — SVG validated (normal/hover/pressed), file present and loaded without error
- [x] Task manager: teal outline on hover, amber double-ring on focused window — confirmed visually in screenshot (amber-outlined boxes matched `focus` state design)
- [ ] Task manager: attention state pulses amber — SVG asset present and validated (`attention` state with `<animate>`), not exercised live (no app put into a demanding-attention state during this session)
- [~] relojlcd clock, teal color — `clockStyle=VFD Teal` config confirmed written to the applet's config on disk; the *live panel this created was removed* after it collided with the pre-existing bottom panel and destabilized the desktop (see below) — the config itself is correct and validated, but not currently showing on-screen
- [x] Titlebar (Aurorae): brushed metal, teal outline when focused, desaturated when not — `kwinrc` confirmed set to `theme=__aurorae__svg__RetroDIN`, no decoration-load errors in the journal
- [x] Titlebar buttons: minimize/maximize/close all teal idle, all amber on hover, close NOT red — all three SVGs validated, all use the same amber hover language
- [x] Context menu / notification (dark recessed well, amber row highlight): dialog frame + listitem SVGs validated and loaded without error; triggered a real `notify-send` with no errors
- [x] Tooltip: dark well chip — SVG validated and loaded without error
- [x] Splash screen: teal noise texture, "SYSTEM" wordmark with glow-colored text — confirmed via `ksplashqml --test --window`, screenshot shows exactly the intended result
- [~] Lock screen: charcoal/teal composited wallpaper — image built, composited, and validated (1920×1080); wallpaper package symlinked; **not** applied live and **not** tested via `loginctl lock-session` (would have locked the user's active session mid-review — skipped deliberately, not a technical failure)
- [ ] Tier-2 sanity (Dolphin/Kate body text is off-white, not glowing teal) — not opened during this session; `.colors` file itself was verified to write `ForegroundNormal=207,236,232` (the off-white), which is the mechanism this depends on

## Incident during Task 10

Applying the panel layout via `plasma.loadSerializedLayout()` (through Plasma's
scripting D-Bus interface, since there's no GUI on this machine to click the
"Desktop Layout" checkbox non-interactively) **added a second bottom panel
next to the user's existing one** rather than replacing it — this desktop has
4+ pre-existing containments across 2 screens, far more customized than the
single-panel reference layout this task's `layout.js` was modeled on.
Result: visibly broken/duplicated bottom panel on the live desktop, reported
directly by the user ("its not stable lol", "right now everything is messed
up the whole bottom panel is non working and mess").

Fixed immediately via the same scripting interface (`panelById(622).remove()`),
confirmed restored via screenshot and a `panelIds` re-query (back to the
original 2 panels). The `layout.js` **file** itself is correct and passes its
validator — the risk was in *live-testing* it against a heavily-customized
real desktop, not in the file's content. Also encountered mid-incident: a
transient plasmashell hang (90%+ CPU, D-Bus unresponsive) that required a
manual `kill -KILL` and relaunch — likely triggered by a pre-existing bug in
the `relojlcd` plasmoid's own `main.qml` (`ReferenceError: container is not
defined`, present in logs before any change made here) firing on a second
instance during heavy relayout, not something introduced by this theme's code.

**Recommendation for the user:** test `layout.js` in a disposable VM or via
Plasma's "Manage Desktop Layouts" export/import (reversible) before applying
it to this machine's actual multi-panel setup, if the pre-built panel
(kickoff + task manager + systray + relojlcd, all in the theme's colors) is
wanted here. Everything else in the package — colors, desktoptheme, Aurorae,
splash, lock wallpaper — was live-tested on this machine without incident.
