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
        
        fail_flag = os.path.join(tempfile.gettempdir(), "update_failed.flag")

        # ✅ nếu vừa rollback → bỏ qua 1 lần
        if os.path.exists(fail_flag):
            os.remove(fail_flag)
            return False, None

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

    import sys
    import os
    import tempfile
    import subprocess

    
    def get_real_exe_path():
            if getattr(sys, 'frozen', False):
                return sys.executable
            return os.path.abspath(sys.argv[0])

    
    current_exe = get_real_exe_path()
    app_dir = os.path.dirname(current_exe)
    exe_name = os.path.basename(current_exe)

    backup_exe = os.path.join(app_dir, exe_name + ".bak")
    bat_path = os.path.join(os.environ["TEMP"], "update_script.bat")

    script = rf"""
    @echo off

    set LOGFILE=%temp%\update_log.txt
    echo ==== START UPDATE ==== >> %LOGFILE%

    timeout /t 2 /nobreak > nul

    echo Killing old process >> %LOGFILE%
    taskkill /f /im "{exe_name}" > nul 2>&1

    :: ===== CHECK NEW FILE =====
    if not exist "{new_file_path}" (
        echo NEW FILE NOT FOUND >> %LOGFILE%
        goto rollback
    )

    :: ===== STEP 1: BACKUP =====
    echo Backup exe >> %LOGFILE%
    if exist "{backup_exe}" del "{backup_exe}"
    copy "{current_exe}" "{backup_exe}" > nul

    :: ===== STEP 2: INSTALL NEW =====
    echo Copy new exe >> %LOGFILE%
    copy /Y "{new_file_path}" "{current_exe}" > nul

    if not exist "{current_exe}" (
        echo COPY FAILED >> %LOGFILE%
        goto rollback
    )

    :: ===== STEP 3: START NEW APP =====
    echo Start new exe >> %LOGFILE%
    start "" "{current_exe}"

    timeout /t 5 /nobreak > nul

    tasklist | find /i "{exe_name}" > nul
    if errorlevel 1 (
        echo APP FAILED → ROLLBACK >> %LOGFILE%
        goto rollback
    )

    echo UPDATE SUCCESS >> %LOGFILE%
    del "{backup_exe}"
    goto end

    :rollback
    echo fail > "%temp%\update_failed.flag"
    echo ROLLBACK >> %LOGFILE%

    taskkill /f /im "{exe_name}" > nul 2>&1
    copy /Y "{backup_exe}" "{current_exe}" > nul

    start "" "{current_exe}"

    :end
    echo DONE >> %LOGFILE%
    del "%~f0"
    """

    with open(bat_path, "w", encoding="utf-8") as f:
        f.write(script)

    subprocess.Popen(
        # show cmd window for debugging
        ["cmd", "/k", bat_path]

        # change to "/c" and add CREATE_NO_WINDOW for silent mode in production
        # ["cmd", "/c", bat_path],
        # creationflags=subprocess.CREATE_NO_WINDOW
    )

    sys.exit(0)
