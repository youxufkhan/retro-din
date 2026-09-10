#!/usr/bin/env bash
# Encode the CRT-noise loop used by the splash and the animated wallpaper.
#
# Kept at the source's native 1024px width: the earlier 384px encode had to be
# upscaled ~5x to fill a screen, which is what made the noise look soft.
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p build/assets
ffmpeg -y -loglevel error -i ~/Downloads/movie2_glow.gif \
    -vf "fps=12,scale=1024:-1" -t 3 build/assets/noise.gif

mkdir -p build/lookandfeel/com.retrodin.theme/contents/splash/images
cp build/assets/noise.gif \
    build/lookandfeel/com.retrodin.theme/contents/splash/images/noise.gif
mkdir -p build/wallpapers/com.retrodin.crtnoise/contents/images
cp build/assets/noise.gif \
    build/wallpapers/com.retrodin.crtnoise/contents/images/noise.gif
ls -lh build/assets/noise.gif
