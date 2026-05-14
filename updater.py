import requests
import os
import subprocess
import sys
import hashlib


CURRENT_VERSION = "1.0"

def verify_file(path, expected_hash):
    sha256 = hashlib.sha256()

    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)

    return sha256.hexdigest() == expected_hash

def check_update():
    try:
        url = "https://raw.githubusercontent.com/anhpham9/company_cleaner-tool/master/version/version.json"
        data = requests.get(url).json()

        latest_version = data["version"]

        if latest_version != CURRENT_VERSION:
            return True, data

        return False, None
    except:
        return False, None


def download_update(url, save_path):
    r = requests.get(url, stream=True)
    with open(save_path, "wb") as f:
        for chunk in r.iter_content(1024):
            if chunk:
                f.write(chunk)


def apply_update(new_exe_path):
    current_exe = sys.executable

    bat_path = os.path.join(os.path.dirname(current_exe), "update.bat")

    with open(bat_path, "w") as f:
        f.write(f"""
            timeout /t 2 /nobreak >nul
            del "{current_exe}"
            rename "{new_exe_path}" "{os.path.basename(current_exe)}"
            start "" "{current_exe}"
            del "%~f0"
            """)

    subprocess.Popen(bat_path, shell=True)
    sys.exit()