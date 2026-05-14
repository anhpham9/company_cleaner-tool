import pandas as pd
import unicodedata
import os
from openpyxl import load_workbook

# ===== normalize company name =====
def normalize(text):
    if pd.isna(text):
        return ""

    text = str(text)

    # ✅ xóa phần sau /
    text = text.split("/")[0]

    # ✅ full-width → half-width
    text = unicodedata.normalize('NFKC', text)

    # ✅ trim
    text = text.strip()

    return text.lower()


# ===== main process =====
def process_file(file_path, blacklist_path="blacklist.xlsx"):

    # ✅ read excel bằng pandas
    df = pd.read_excel(file_path)

    # ✅ FIX header "Unnamed" → ""
    df.columns = [
        "" if str(col).startswith("Unnamed") else col
        for col in df.columns
    ]

    # ✅ lưu bản gốc tên công ty để export lại
    df["会社名_original"] = df["会社名"]

    # ✅ create clean column để xử lý
    df["__clean"] = df["会社名"].apply(normalize)

    # ✅ UPDATE lại 会社名 hiển thị (clean thật)
    df["会社名"] = df["__clean"].apply(lambda x: x.strip())

    # ===== blacklist =====
    if os.path.exists(blacklist_path):
        bl = pd.read_excel(blacklist_path)
        bl["__clean"] = bl["会社名"].apply(normalize)

        df = df[~df["__clean"].isin(bl["__clean"])]

    # ===== remove duplicate =====
    duplicates = df[df.duplicated("__clean", keep="first")]
    df_unique = df.drop_duplicates("__clean", keep="first")

    removed = len(duplicates)
    remain = len(df_unique)

    # ===== drop helper columns =====
    df_unique = df_unique.drop(columns=["__clean", "会社名_original"])
    duplicates = duplicates.drop(columns=["__clean", "会社名_original"])

    base = os.path.splitext(file_path)[0]

    output_file = base + "_cleaned.xlsx"
    log_file = base + "_log.xlsx"

    # ✅ ghi data trước (chưa format)
    df_unique.to_excel(output_file, index=False)
    duplicates.to_excel(log_file, index=False)

    # ===== ✅ COPY FORMAT từ file gốc =====
    wb_src = load_workbook(file_path)
    wb_dst = load_workbook(output_file)

    ws_src = wb_src.active
    ws_dst = wb_dst.active

    # ✅ copy column width
    for col in ws_src.column_dimensions:
        ws_dst.column_dimensions[col].width = ws_src.column_dimensions[col].width

    # ✅ copy style từng ô (chỉ vùng dữ liệu)
    for row in ws_src.iter_rows():
        for cell in row:
            new_cell = ws_dst[cell.coordinate]

            if cell.has_style:
                new_cell.font = cell.font
                new_cell.border = cell.border
                new_cell.fill = cell.fill
                new_cell.number_format = cell.number_format
                new_cell.alignment = cell.alignment

    wb_dst.save(output_file)

    return {
        "removed": removed,
        "remain": remain,
        "output_file": base + "_cleaned.xlsx",
        "log_file": base + "_log.xlsx"
    }
