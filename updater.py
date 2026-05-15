

import requests
import hashlib
import os
import sys
import tempfile
import subprocess


# ==============================
# 🔍 CHECK UPDATE
# ==============================
def check_update():
    """
    Call API để check version mới
    Return:
        (True, data) hoặc (False, None)
    """

    try:
        # 🔧 sửa URL API của bạn ở đây
        url = "https://raw.githubusercontent.com/anhpham9/company_cleaner-tool/master/version/version.json"

        res = requests.get(url, timeout=10)
        res.raise_for_status()

        data = res.json()

        from app_version import APP_VERSION

        if data["version"] != APP_VERSION:
            return True, data

        return False, None

    except Exception as e:
        print("Update check failed:", e)
        return False, None


# ==============================
# 📥 DOWNLOAD UPDATE
# ==============================
def download_update(url, save_path, progress_callback=None):
    """
    Download file with progress
    """

    with requests.get(url, stream=True) as r:
        r.raise_for_status()

        total_size = int(r.headers.get("content-length", 0))
        downloaded = 0

        with open(save_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)

                    if total_size > 0 and progress_callback:
                        progress = downloaded / total_size
                        progress_callback(progress)


# ==============================
# 🔐 VERIFY FILE (SHA256)
# ==============================
def verify_file(path, expected_hash):
    """
    Verify SHA256 file
    """

    sha256 = hashlib.sha256()

    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)

    file_hash = sha256.hexdigest()

    print("Downloaded hash:", file_hash)

    return file_hash.lower() == expected_hash.lower()


# ==============================
# 🚀 APPLY UPDATE (CRITICAL PART)
# ==============================
def apply_update(new_file_path):
    """
    Tạo updater script để:
    1. Chờ app hiện tại tắt
    2. Replace file exe
    3. Restart app
    """

    
    current_exe = sys.executable
    app_dir = os.path.dirname(current_exe)
    exe_name = os.path.basename(current_exe)

    backup_exe = os.path.join(app_dir, exe_name + ".bak")

    bat_path = os.path.join(tempfile.gettempdir(), "update_script.bat")

    script = f"""
    @echo off
    echo === UPDATING WITH ROLLBACK ===

    :: đợi app hiện tại tắt
    timeout /t 2 /nobreak > nul

    :: kill lại cho chắc
    taskkill /f /im "{exe_name}" > nul 2>&1

    :: ===== STEP 1: backup =====
    if exist "{backup_exe}" del "{backup_exe}"
    rename "{current_exe}" "{exe_name}.bak"

    :: ===== STEP 2: install new =====
    rename "{new_file_path}" "{exe_name}"

    :: ===== STEP 3: start new app =====
    start "" "{current_exe}"

    :: ===== STEP 4: check if app started =====
    timeout /t 5 /nobreak > nul

    tasklist | find /i "{exe_name}" > nul

    if errorlevel 1 (
        echo NEW VERSION FAILED → ROLLBACK

        :: kill nếu có process lỗi
        taskkill /f /im "{exe_name}" > nul 2>&1

        :: xóa file lỗi
        del "{current_exe}"

        :: restore backup
        rename "{backup_exe}" "{exe_name}"

        :: chạy lại bản cũ
        start "" "{current_exe}"
    ) else (
        echo UPDATE SUCCESS
        :: xóa backup
        del "{backup_exe}"
    )

    :: cleanup
    del "%~f0"
    """

    with open(bat_path, "w", encoding="utf-8") as f:
        f.write(script)

    subprocess.Popen(
        ["cmd", "/c", bat_path],
        creationflags=subprocess.CREATE_NO_WINDOW
    )

    sys.exit(0)