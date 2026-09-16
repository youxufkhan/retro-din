# KDE Store: quick steps

Short version of `KDE_STORE_SUBMISSION.md`. Follow this top to bottom, in
order. Each step is one action.

This packages Retro DIN as **one download** (the "single bundle" option),
not nine separate store listings — simplest path, and the one that fits a
theme with a root-only install step (SDDM) and an external dependency
(Kvantum).

## 1. Build everything

```bash
cd /home/yousuf/apps/plasma
scripts/install.sh
```

This generates the icon tree, the desktoptheme colors file, and the noise
GIFs — all gitignored, so they don't exist until this runs. Skipping this
step means the zip you upload is missing files and the theme won't work
for anyone who downloads it.

## 2. Check the version number

Every package's `metadata.json` / `metadata.desktop` says `"Version":
"1.0"` right now. If this is a new release, bump them together — otherwise
leave as-is for a first upload. (Files: `aurorae/RetroDIN/metadata.desktop`,
`desktoptheme/RetroDIN/metadata.json`, `lookandfeel/com.retrodin.theme/metadata.json`,
`sddm/RetroDIN/metadata.desktop`, both `wallpapers/*/metadata.json`.)

## 3. Take a screenshot

Apply the theme on your own desktop (System Settings → Appearance → Global
Themes → Retro DIN), then screenshot something that shows it off: panel +
a themed window + a menu open. This is the preview image for the listing.
Save it somewhere outside the repo, e.g. `~/Pictures/retro-din-preview.png`.

## 4. Make the zip

From one level above the repo, so the zip's top-level folder is the repo
itself:

```bash
cd /home/yousuf/apps
zip -rq retro-din.zip plasma \
    -x 'plasma/.git/*' -x 'plasma/.superpowers/*' -x '*__pycache__*'
```

Check it's not empty-handed on the generated stuff:

```bash
unzip -l retro-din.zip | grep -c 'icons/RetroDIN/'
```

Should print a large number (thousands) — if it prints 0, step 1 didn't
run before you zipped.

## 5. Go to store.kde.org and log in

Log in with your KDE Store account (or create one — it uses the same
account system as most KDE services).

## 6. Start a new upload

Click **Upload Product** (top of the site). Pick a category — for this
theme, **"Plasma Global Themes"** is the right one, since that's the
component most people will search for.

## 7. Fill in the listing

- **Title**: Retro DIN
- **Description**: paste the intro from `README.md` (the first paragraph
  plus the "What's in it" table), then add a line telling people to run
  `scripts/install.sh` after extracting — this is not a one-click GHNS
  install, it's a script-installed bundle. Mention Kvantum is a separate
  required dependency, and that the SDDM login theme needs
  `sudo scripts/install-sddm.sh` as an extra step.
- **License**: GPL-3.0-or-later (there's a dropdown). Note the SDDM
  component's CC-BY-SA origin in the description text — see `NOTICE.md`.
- **Tags**: plasma, plasma6, theme, global theme, dark, retro (whatever's
  offered/relevant).

## 8. Upload the files

- Upload `retro-din.zip` as the product file.
- Upload your screenshot as the preview image.

## 9. Publish

Submit. KDE Store review timing varies — check back on the listing status.

## 10. Later updates

When you change something: repeat steps 1, 4, and 8 (rebuild, re-zip,
upload as a new file version on the same listing) instead of making a new
listing. Bump the version numbers first (step 2) so the listing's version
history makes sense.

---

Need more detail on any step (category naming, multi-entry vs. bundle
tradeoffs, per-package packaging) — see `docs/KDE_STORE_SUBMISSION.md`.
