import yaml, os, re
from dotenv import load_dotenv

load_dotenv()
# the \w indicates a string that starts and ends with a-z characters, adding the + next to the \w extends the string to accepte _ and numbers which allows to captures for example FIRST_NAME as a whole and not only the first half (FIRST)

PATTERN = re.compile(r"^%env:(\w+)%")

def resolve(node):
    if isinstance(node, dict):
        return {k:resolve(v) for k, v in node.items()}
    if isinstance(node, list):
        return [resolve(v) for v in node]
    if isinstance(node, str):
        m = PATTERN.match(node)
        if m:
            return os.environ.get(m.group(1))
    return node


with open("main.yml") as f:
    data = resolve(yaml.safe_load(f))

dt = data["target"]
for k,v in dt.items():
    print(f"{k} : {v}")

print(dt)
