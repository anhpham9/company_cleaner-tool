import json
import os

v = json.load(open("version/version.json"))["version"]

# ghi vào GitHub env
with open(os.environ["GITHUB_ENV"], "a") as f:
    f.write(f"VERSION={v}\n")

print("Version:", v)