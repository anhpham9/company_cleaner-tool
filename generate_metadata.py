import hashlib
import os
import json

file_path = "dist/CompanyCleaner.exe"
version_file = "version/version.json"

# ===== SHA256 =====
sha256 = hashlib.sha256()

with open(file_path, "rb") as f:
    for chunk in iter(lambda: f.read(4096), b""):
        sha256.update(chunk)

hash_value = sha256.hexdigest()

# ===== size =====
size_mb = os.path.getsize(file_path) / (1024 * 1024)
size_str = f"{size_mb:.1f} MB"

# ===== update version.json =====
with open(version_file, "r", encoding="utf-8") as f:
    data = json.load(f)

data["sha256"] = hash_value
data["size"] = size_str

with open(version_file, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Updated metadata")
