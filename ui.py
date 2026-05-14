# pip install pyinstaller customtkinter pandas openpyxl requests
# pyinstaller ^
#  --onefile ^
#  --noconsole ^
#  --icon=assets/icon.ico ^
#  main.py

# CompanyCleaner.exe

# 社内ツールのため、警告が出る場合は
# 「詳細情報」→「実行」で利用してください。



import customtkinter as ctk
from tkinter import filedialog
from processor import process_file
from logger import log_action

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("企業リストクリーナー")
        self.geometry("600x400")

        self.label = ctk.CTkLabel(self, text="企業リストクリーナー", font=("Meiryo", 20, "bold"))
        self.label.pack(pady=20)

        self.desc = ctk.CTkLabel(self, text="Excelファイルを選択またはドラッグしてください", font=("Meiryo", 14, "bold"), text_color="#333333")
        self.desc.pack()

        self.btn = ctk.CTkButton(self, text="📂 ファイル選択", font=("Meiryo", 14, "bold"), command=self.select_file)
        self.btn.pack(pady=20)

        self.progress = ctk.CTkProgressBar(self, width=400)
        self.progress.pack(pady=10)

        self.status = ctk.CTkLabel(self, text="", font=("Meiryo", 14, "bold"), text_color="#1F6AA5")
        self.status.pack(pady=10)

    def select_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel", "*.xlsx")])
        if file_path:
            self.run_process(file_path)

    def run_process(self, file_path):
        self.status.configure(text="処理中...")
        self.progress.set(0.2)

        result = process_file(file_path)

        self.progress.set(1)
        self.status.configure(
            text=f"完了：{result['removed']}件削除 / 残り{result['remain']}件\n出力ファイル：{result['output_file']}\nログファイル：{result['log_file']}"
        )

        log_action(f"Processed {file_path}")


def run():
    app = App()
    app.mainloop()