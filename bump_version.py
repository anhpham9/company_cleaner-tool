import json

file = "version/version.json"

with open(file, "r", encoding="utf-8") as f:
    data = json.load(f)

version = data["version"]
major, minor = map(int, version.split("."))

# tăng version (1.0 → 1.1)
minor += 1

new_version = f"{major}.{minor}"
data["version"] = new_version

with open(file, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("New version:", new_version)