import json

file = "version/version.json"

with open(file, "r", encoding="utf-8") as f:
    data = json.load(f)

data["url"] = (
    f"https://github.com/anhpham9/company_cleaner-tool/"
    f"releases/download/v{data['version']}/CompanyCleaner.exe"
)

with open(file, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Updated URL")