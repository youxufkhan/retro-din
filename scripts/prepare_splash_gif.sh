#!/usr/bin/env bash
# scripts/prepare_splash_gif.sh
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p build/lookandfeel/com.retrodin.theme/contents/splash/images
ffmpeg -y -i ~/Downloads/movie2_glow.gif -vf "fps=10,scale=384:-1" -t 2.5 \
    build/lookandfeel/com.retrodin.theme/contents/splash/images/noise.gif
