import sys
import os
import re
files = []

sprites = {}

walk_dir = sys.argv[1]
walk_dir = os.path.abspath(walk_dir)

files = [os.path.join(root, file)
         for root, _, files in os.walk(walk_dir) for file in files]
r = re.compile("^.*\.yarn$")
files = list(filter(r.match, files))


r = re.compile("^<<setSprite (.+) (.+)>>$")
for file in files:
    with open(file) as f:
        for line in f:
            line = line.strip()
            match = r.match(line)
            if match:
                sprite = match.group(1)
                expression = match.group(2)

                if sprite not in sprites:
                    sprites[sprite] = []

                if expression not in sprites[sprite]:
                    sprites[sprite].append(expression)


for key in sorted(sprites):
    print(f"Sprites needed for {key}:")
    print()
    for val in sorted(sprites[key]):
        print(f"- [ ] {val}")
    print("\n")
