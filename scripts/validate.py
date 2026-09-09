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
