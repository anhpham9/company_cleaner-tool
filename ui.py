import customtkinter as ctk
from tkinter import filedialog, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD

from updater import check_update, download_update, apply_update
import tempfile
import os


from processor import process_file
from logger import log_action

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class App(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()

        self.after(1000, self.check_update_ui)

        self.title("企業リストクリーナー")
        self.geometry("620x420")

        self.configure(bg="#F5F7FA")

        # ===== Title =====
        self.label = ctk.CTkLabel(
            self,
            text="企業リストクリーナー",
            font=("Meiryo", 20, "bold")
        )
        self.label.pack(pady=15)

        # ===== Description =====
        self.desc = ctk.CTkLabel(
            self,
            text="Excelファイルを選択またはドラッグしてください",
            font=("Meiryo", 13, "bold")
        )
        self.desc.pack(pady=(0, 5))

        # ===== Button =====
        self.btn = ctk.CTkButton(
            self,
            text="📂 ファイル選択",
            command=self.select_file,
            width=200,
            height=40
        )
        self.btn.pack(pady=(0, 15))

        # ===== Drop Area =====
        self.drop_area = ctk.CTkFrame(
            self,
            width=500,
            height=140,
            corner_radius=15,
            fg_color="#E3F2FD"
        )
        self.drop_area.pack(pady=10)

        self.drop_label = ctk.CTkLabel(
            self.drop_area,
            text="📥 ここにファイルをドロップ",
            font=("Meiryo", 13, "bold")
        )
        self.drop_label.place(relx=0.5, rely=0.5, anchor="center")

        # ✅ Enable Drag
        self.drop_area.drop_target_register(DND_FILES)
        self.drop_area.dnd_bind("<<Drop>>", self.drop_file)

        self.drop_area.dnd_bind("<Enter>", self.on_drag_enter)
        self.drop_area.dnd_bind("<Leave>", self.on_drag_leave)

        # ===== Progress =====
        self.progress = ctk.CTkProgressBar(self, width=400)
        self.progress.pack(pady=10)

        # ===== Status =====
        self.status = ctk.CTkLabel(
            self,
            text="",
            font=("Meiryo", 12, "bold"),
            text_color="#1F6AA5"
        )
        self.status.pack(pady=5)

    # ===== Update check on start =====
    def check_update_ui(self):
        has_update, data = check_update()

        if has_update:
            result = messagebox.askyesno(
                "アップデート",
                f"新しいバージョンがあります\n\n"
                f"最新: {data['version']}\n\n"
                f"{data['note']}\n\n"
                f"更新しますか？"
            )

            if result:
                self.perform_update(data)


    # ===== File select =====
    def select_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel", "*.xlsx")])
        if file_path:
            self.run_process(file_path)

    # ===== Drag highlight =====
    def on_drag_enter(self, event):
        self.drop_area.configure(fg_color="#BBDEFB")

    def on_drag_leave(self, event):
        self.drop_area.configure(fg_color="#E3F2FD")

    # ===== Drop handler =====
    def drop_file(self, event):
        file_path = event.data.strip("{}")

        # reset màu
        self.drop_area.configure(fg_color="#E3F2FD")

        # ✅ check extension
        if not file_path.lower().endswith(".xlsx"):
            messagebox.showerror("エラー", "Excelファイル(.xlsx)のみ対応しています")
            return

        self.run_process(file_path)

    # ===== Main process =====
    def run_process(self, file_path):

        filename = os.path.basename(file_path)

        self.status.configure(text=f"処理中：{filename}")
        self.progress.set(0.3)
        self.update_idletasks()

        try:
            result = process_file(file_path)

            self.progress.set(1)

            self.status.configure(
                text=(
                    f"✅ 完了：{result['removed']}件削除 / 残り{result['remain']}件\n"
                    f"📄 {result['output_file']}\n"
                    f"📄 {result['log_file']}\n"
                )
            )

            log_action(f"Processed {file_path}")

        except Exception as e:
            messagebox.showerror("エラー", str(e))
            self.progress.set(0)


def run():
    app = App()
    app.mainloop()