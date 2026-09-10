#!/usr/bin/env bash
# Install the Retro DIN SDDM (login screen) theme. Needs root, because SDDM
# reads themes from /usr/share and its config from /etc.
#
# Deliberately additive: the theme is copied to a new directory and selected
# through a new 99-retrodin.conf, which sorts last and therefore wins. The
# distribution's own kde_settings.conf is left untouched, so reverting is
# "rm /etc/sddm.conf.d/99-retrodin.conf" and nothing else.
#
# The greeter runs as the sddm user and cannot read /home, so the wallpaper
# and logo are copied into the theme directory rather than referenced.
set -euo pipefail
cd "$(dirname "$0")/.."

if [ "$(id -u)" -ne 0 ]; then
    echo "Run with sudo: sudo scripts/install-sddm.sh" >&2
    exit 1
fi

SRC="$(pwd)/build/sddm/RetroDIN"
DEST=/usr/share/sddm/themes/RetroDIN

[ -d "$SRC" ] || { echo "missing $SRC" >&2; exit 1; }

echo "Installing theme to $DEST"
rm -rf "$DEST"
mkdir -p "$DEST"
cp -r "$SRC/." "$DEST/"
chown -R root:root "$DEST"
chmod -R a+rX "$DEST"

echo "Selecting it in /etc/sddm.conf.d/99-retrodin.conf"
mkdir -p /etc/sddm.conf.d
cat > /etc/sddm.conf.d/99-retrodin.conf <<'EOF'
[Theme]
Current=RetroDIN
EOF

echo
echo "Done. Verify before logging out:"
echo "  sddm-greeter-qt6 --test-mode --theme $DEST"
echo
echo "To revert:"
echo "  sudo rm /etc/sddm.conf.d/99-retrodin.conf"
