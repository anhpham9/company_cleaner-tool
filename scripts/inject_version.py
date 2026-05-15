import json

with open("version/version.json", "r", encoding="utf-8") as f:
    v = json.load(f)["version"]

with open("app_version.py", "w") as f:
    f.write(f'APP_VERSION = "{v}"')

print("Injected version:", v)