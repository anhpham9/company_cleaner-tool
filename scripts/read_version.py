import json
import os

v = json.load(open("version/version.json"))["version"]

# export env cho GitHub Actions
print(f"::set-env name=VERSION::{v}")