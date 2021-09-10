import sys
import os
import re
files = []

sprites = {}
functions = {}
commands = {}
# Should be ignored for command matching
yarnKeywords = [
    "call",
    "else",
    "elseif",
    "endif",
    "if",
    "pass",
    "set",
    "wait",
]

walk_dir = sys.argv[1]
walk_dir = os.path.abspath(walk_dir)

files = [os.path.join(root, file)
         for root, _, files in os.walk(walk_dir) for file in files]
r = re.compile("^.*\.yarn$")
files = list(filter(r.match, files))


rSS = re.compile(r"^<<setSprite (.+) (.+)>>$")
rCommands = re.compile(r"^<<(\w+)( .+)* *>>$")
rFunctions = re.compile(r"(\w+)\((.+)\)")
for file in files:
    with open(file) as f:
        for line in f:
            line = line.strip()
            if line[:2] == "//":
                continue
            match = rSS.match(line)
            if match:
                sprite = match.group(1)
                expression = match.group(2)

                if sprite not in sprites:
                    sprites[sprite] = {}

                if expression not in sprites[sprite]:
                    sprites[sprite][expression] = 0
                sprites[sprite][expression] += 1
            match = rCommands.match(line)
            if match:
                command = match.group(1)
                if command not in yarnKeywords:
                    if command not in commands:
                        commands[command] = 0
                    commands[command] += 1
            match = rFunctions.search(line)
            if match:
                function = match.group(1)
                function = function + \
                    "()"
                # f"({'a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z'[:len(match.groups())*2-3]})"  # lol
                if function not in functions:
                    functions[function] = 0
                functions[function] += 1


for key in sorted(sprites):
    print(f"Sprites needed for {key}:")
    print()
    for val in sorted(sprites[key]):
        print(
            f"- [ ] {val}" + (f" ({sprites[key][val]})" if sprites[key][val] > 1 else ""))
    print("\n")

print(f"Total sprites needed: {sum([len(sprites[k]) for k in sprites])}")

print("-------------\n")
print("Commands needed:\n")
for key in sorted(commands):
    print(
        f"- [ ] {key}" +
        (f" ({commands[key]})" if commands[key] > 1 else "")
    )
print(f"\nTotal commands needed: {len(commands)}\n")
print("-------------\n")
print("Functions needed:\n")
for key in sorted(functions):
    print(
        f"- [ ] {key}" +
        (f" ({functions[key]})" if functions[key] > 1 else "")
    )
print(f"\nTotal functions needed: {len(functions)}")
