#!/usr/bin/env bash
# scripts/install.sh — symlink build/ output into real KDE data dirs. Idempotent.
set -euo pipefail
cd "$(dirname "$0")/.."

ln -sfT "$(pwd)/build/color-schemes/RetroDIN.colors" \
    ~/.local/share/color-schemes/RetroDIN.colors
# Plasma widgets and systray glyphs read colours from the desktoptheme's own
# colors file, not kdeglobals; without it they fall back to breeze-dark white.
python3 scripts/gen_theme_colors.py
mkdir -p ~/.local/share/plasma/desktoptheme
ln -sfT "$(pwd)/build/desktoptheme/RetroDIN" \
    ~/.local/share/plasma/desktoptheme/RetroDIN
mkdir -p ~/.local/share/aurorae/themes
ln -sfT "$(pwd)/build/aurorae/RetroDIN" \
    ~/.local/share/aurorae/themes/RetroDIN
mkdir -p ~/.local/share/plasma/look-and-feel
ln -sfT "$(pwd)/build/lookandfeel/com.retrodin.theme" \
    ~/.local/share/plasma/look-and-feel/com.retrodin.theme
mkdir -p ~/.local/share/wallpapers
ln -sfT "$(pwd)/build/wallpapers/RetroDIN-lockwall" \
    ~/.local/share/wallpapers/RetroDIN-lockwall
# the icon theme is generated: DIN status glyphs first, then the recoloured
# breeze base they overlay onto
python3 scripts/gen_din_icons.py
python3 scripts/gen_app_icons.py
python3 scripts/gen_icons.py
mkdir -p ~/.local/share/plasma/wallpapers
# the animated wallpaper plugin: the lock screen renders a wallpaper plugin,
# and org.kde.image only ever draws a still frame
cp build/assets/noise.gif \
    build/wallpapers/com.retrodin.crtnoise/contents/images/noise.gif
cp build/assets/noise.gif \
    build/lookandfeel/com.retrodin.theme/contents/splash/images/noise.gif
ln -sfT "$(pwd)/build/wallpapers/com.retrodin.crtnoise" \
    ~/.local/share/plasma/wallpapers/com.retrodin.crtnoise
mkdir -p ~/.local/share/icons
ln -sfT "$(pwd)/build/icons/RetroDIN" \
    ~/.local/share/icons/RetroDIN
mkdir -p ~/.config/Kvantum
ln -sfT "$(pwd)/build/kvantum/RetroDIN" \
    ~/.config/Kvantum/RetroDIN
echo "Installed (symlinked). Run plasma-apply-colorscheme RetroDIN to test the color scheme now."
