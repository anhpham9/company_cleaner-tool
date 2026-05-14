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

        self.desc = ctk.CTkLabel(self, text="Excelファイルを選択またはドラッグしてください")
        self.desc.pack()

        self.btn = ctk.CTkButton(self, text="📂 ファイル選択", command=self.select_file)
        self.btn.pack(pady=20)

        self.progress = ctk.CTkProgressBar(self, width=400)
        self.progress.pack(pady=10)

        self.status = ctk.CTkLabel(self, text="")
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
            text=f"完了：{result['removed']}件削除 / 残り{result['remain']}件"
        )

        log_action(f"Processed {file_path}")


def run():
    app = App()
    app.mainloop()