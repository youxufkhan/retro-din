#!/usr/bin/env bash
# Install the Retro DIN SDDM (login screen) theme. Needs root, because SDDM
# reads themes from /usr/share and its config from /etc.
#
# Deliberately additive: the theme is copied to a new directory and selected
# through a drop-in, leaving the distribution's kde_settings.conf untouched,
# so reverting is one rm.
#
# The drop-in is named zz-retrodin.conf, not 99-retrodin.conf. SDDM reads
# /etc/sddm.conf.d/ in plain alphabetical order and letters sort after digits,
# so kde_settings.conf and kubuntu_settings.conf both override a 99- file.
# Only a name sorting after those actually wins.
#
# Consequence worth knowing: this then also overrides whatever System Settings
# writes into kde_settings.conf, so picking a different login theme in the GUI
# will look like it does nothing until this file is removed.
#
# The greeter runs as the sddm user and cannot read /home, so the wallpaper
# and logo are copied into the theme directory rather than referenced.
set -euo pipefail
cd "$(dirname "$0")/.."

if [ "$(id -u)" -ne 0 ]; then
    echo "Run with sudo: sudo scripts/install-sddm.sh" >&2
    exit 1
fi

SRC="$(pwd)/sddm/RetroDIN"
DEST=/usr/share/sddm/themes/RetroDIN

[ -d "$SRC" ] || { echo "missing $SRC" >&2; exit 1; }

echo "Installing theme to $DEST"
rm -rf "$DEST"
mkdir -p "$DEST"
cp -r "$SRC/." "$DEST/"
chown -R root:root "$DEST"
chmod -R a+rX "$DEST"

echo "Selecting it in /etc/sddm.conf.d/zz-retrodin.conf"
mkdir -p /etc/sddm.conf.d
rm -f /etc/sddm.conf.d/99-retrodin.conf
cat > /etc/sddm.conf.d/zz-retrodin.conf <<'EOF'
[Theme]
Current=RetroDIN
EOF

echo
echo "Done. Verify before logging out:"
echo "  sddm-greeter-qt6 --test-mode --theme $DEST"
echo
echo "To revert:"
echo "  sudo rm /etc/sddm.conf.d/zz-retrodin.conf"
