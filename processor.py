import pandas as pd
import unicodedata
import os

def normalize(text):
    if pd.isna(text):
        return ""
    text = unicodedata.normalize('NFKC', str(text))
    return text.split("/")[0].strip().lower()


def process_file(file_path, blacklist_path="blacklist.xlsx"):
    df = pd.read_excel(file_path)

    df["__clean"] = df["会社名"].apply(normalize)

    # ✅ Load blacklist
    if os.path.exists(blacklist_path):
        bl = pd.read_excel(blacklist_path)
        bl["__clean"] = bl["会社名"].apply(normalize)

        df = df[~df["__clean"].isin(bl["__clean"])]

    duplicates = df[df.duplicated("__clean", keep="first")]
    df_unique = df.drop_duplicates("__clean", keep="first")

    removed = len(duplicates)
    remain = len(df_unique)

    base = os.path.splitext(file_path)[0]

    df_unique.drop(columns=["__clean"]).to_excel(base + "_clean.xlsx", index=False)
    duplicates.to_excel(base + "_log.xlsx", index=False)

    return {
        "removed": removed,
        "remain": remain
    }