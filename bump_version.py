import json
import argparse

FILE = "version/version.json"


def load_data():
    with open(FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_data(data):
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def bump_version(version):
    major, minor = map(int, version.split("."))
    minor += 1
    return f"{major}.{minor}"


def main():
    parser = argparse.ArgumentParser(description="Bump version and update release note")

    parser.add_argument(
        "--note",
        type=str,
        default="",
        help="Release note (e.g. アイコン変更)"
    )

    parser.add_argument(
        "--major",
        action="store_true",
        help="Increase major version (e.g. 2.3 → 3.0)"
    )

    args = parser.parse_args()

    data = load_data()

    current_version = data["version"]

    # ✅ bump version
    if args.major:
        major, _ = map(int, current_version.split("."))
        new_version = f"{major + 1}.0"
    else:
        new_version = bump_version(current_version)

    data["version"] = new_version

    # ✅ update note nếu có
    if args.note:
        data["note"] = args.note

    save_data(data)

    print(f"Version updated: {current_version} → {new_version}")

    if args.note:
        print(f"Note updated: {args.note}")


if __name__ == "__main__":
    main()