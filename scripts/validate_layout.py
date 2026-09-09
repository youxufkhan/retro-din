import sys, re, json

path = sys.argv[1]
with open(path) as f:
    src = f.read()
match = re.search(r"var layout = (\{.*?\});", src, re.DOTALL)
if not match:
    print("INVALID: no `var layout = {...};` block found", file=sys.stderr)
    sys.exit(1)
json.loads(match.group(1))  # raises if malformed
print(f"OK {path}")
