import sys

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
