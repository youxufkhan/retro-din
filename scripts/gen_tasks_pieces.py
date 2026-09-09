states = ["normal", "hover", "focus", "attention", "minimized", "progress"]
pieces = ["topleft", "top", "topright", "left", "center", "right",
          "bottomleft", "bottom", "bottomright"]
orientations = ["", "north-", "east-", "west-"]

lines = []
for state in states:
    for piece in pieces:
        base_id = f"{state}-{piece}"
        lines.append(f'  <use id="{base_id}" xlink:href="#{state}" x="0" y="0"/>')
    for orient in orientations[1:]:
        for piece in pieces:
            base_id = f"{state}-{piece}"
            lines.append(f'  <use id="{orient}{base_id}" xlink:href="#{base_id}"/>')

print("\n".join(lines))
