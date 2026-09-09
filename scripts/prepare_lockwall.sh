#!/usr/bin/env bash
# scripts/prepare_lockwall.sh
set -euo pipefail
cd "$(dirname "$0")/.."
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
