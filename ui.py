import customtkinter as ctk
from tkinter import filedialog, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD

import tempfile
import os
import threading

from updater import check_update, download_update, apply_update, verify_file
from processor import process_file
from logger import log_action
from app_version import APP_VERSION

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class App(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()

        self.is_updating = False

        self.after(1000, self.check_update_ui)

        self.title(f"企業リストクリーナー - Version: {APP_VERSION}")
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

        # Drag & Drop
        self.drop_area.drop_target_register(DND_FILES)
        self.drop_area.dnd_bind("<<Drop>>", self.drop_file)
        self.drop_area.dnd_bind("<Enter>", self.on_drag_enter)
        self.drop_area.dnd_bind("<Leave>", self.on_drag_leave)

        # ===== Progress =====
        self.progress = ctk.CTkProgressBar(self, width=400)
        self.progress.pack(pady=10)
        self.progress.set(0)

        # ===== Status =====
        self.status = ctk.CTkLabel(
            self,
            text="",
            font=("Meiryo", 12, "bold"),
            text_color="#1F6AA5"
        )
        self.status.pack(pady=5)

    # =========================
    # 🔒 UI ENABLE / DISABLE
    # =========================
    def set_ui_state(self, enable: bool):
        if enable:
            self.btn.configure(state="normal")
            self.drop_area.drop_target_register(DND_FILES)
        else:
            self.btn.configure(state="disabled")
            self.drop_area.drop_target_unregister()

    # =========================
    # 🔄 CHECK UPDATE
    # =========================
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

    # =========================
    # 🚀 START UPDATE
    # =========================
    def perform_update(self, data):
        self.is_updating = True
        self.set_ui_state(False)

        thread = threading.Thread(
            target=self.download_and_update,
            args=(data,),
            daemon=True
        )
        thread.start()

    # =========================
    # 📥 DOWNLOAD + INSTALL
    # =========================
    def download_and_update(self, data):
        try:
            temp_path = os.path.join(tempfile.gettempdir(), "new_app.exe")

            self.after(0, lambda: self.progress.set(0))
            self.after(0, lambda: self.status.configure(text="アップデート中..."))

            if os.path.exists(temp_path):
                os.remove(temp_path)

            # download
            download_update(
                data["url"],
                temp_path,
                progress_callback=self.update_progress
            )

            # verify
            if not verify_file(temp_path, data["sha256"]):
                raise Exception("ファイル検証に失敗しました")

            self.after(0, lambda: self.status.configure(text="インストール中..."))

            # ⚠️ IMPORTANT: sẽ exit app tại đây
            apply_update(temp_path)

        except Exception as e:
            self.after(0, lambda: messagebox.showerror("エラー", str(e)))
            self.after(0, lambda: self.progress.set(0))
            self.after(0, lambda: self.set_ui_state(True))
            self.is_updating = False

    # =========================
    # 📊 PROGRESS UPDATE
    # =========================
    def update_progress(self, value):
        percent = int(value * 100)

        def update():
            self.progress.set(value)
            self.status.configure(text=f"ダウンロード中... {percent}%")

        self.after(0, update)

    # =========================
    # 📂 SELECT FILE
    # =========================
    def select_file(self):
        if self.is_updating:
            messagebox.showwarning("注意", "アップデート中は操作できません")
            return

        file_path = filedialog.askopenfilename(filetypes=[("Excel", "*.xlsx")])
        if file_path:
            self.run_process(file_path)

    # =========================
    # 🎯 DRAG UI EFFECT
    # =========================
    def on_drag_enter(self, event):
        if not self.is_updating:
            self.drop_area.configure(fg_color="#BBDEFB")

    def on_drag_leave(self, event):
        self.drop_area.configure(fg_color="#E3F2FD")

    # =========================
    # 📥 DROP FILE
    # =========================
    def drop_file(self, event):
        if self.is_updating:
            messagebox.showwarning("注意", "アップデート中は操作できません")
            return

        file_path = event.data.strip("{}")
        self.drop_area.configure(fg_color="#E3F2FD")

        if not file_path.lower().endswith(".xlsx"):
            messagebox.showerror("エラー", "Excelファイル(.xlsx)のみ対応しています")
            return

        self.run_process(file_path)

    # =========================
    # ⚙️ MAIN PROCESS
    # =========================
    def run_process(self, file_path):
        filename = os.path.basename(file_path)

        self.status.configure(text=f"処理中：{filename}")
        self.progress.set(0.3)

        try:
            result = process_file(file_path)

            self.progress.set(1)

            if hasattr(self, "output_label"):
                self.output_label.destroy()

            if hasattr(self, "log_label"):
                self.log_label.destroy()

            self.status.configure(
                text=f"✅ 完了：{result['removed']}件削除 / 残り{result['remain']}件"
            )

            # file result
            self.output_label = ctk.CTkLabel(
                self,
                text=f"📄 {result['output_file']}",
                text_color="blue",
                cursor="hand2"
            )
            self.output_label.pack()

            self.output_label.bind(
                "<Button-1>",
                lambda e, p=result['output_file']: self.open_file(p)
            )

            # log file
            self.log_label = ctk.CTkLabel(
                self,
                text=f"📄 {result['log_file']}",
                text_color="blue",
                cursor="hand2"
            )
            self.log_label.pack()

            self.log_label.bind(
                "<Button-1>",
                lambda e, p=result['log_file']: self.open_file(p)
            )

            log_action(f"Processed {file_path}")

        except Exception as e:
            messagebox.showerror("エラー", str(e))
            self.progress.set(0)

    # =========================
    # 📂 OPEN FILE
    # =========================
    def open_file(self, path):
        try:
            if not os.path.exists(path):
                messagebox.showerror("エラー", "ファイルが存在しません")
                return

            os.startfile(path)

        except Exception as e:
            messagebox.showerror("エラー", str(e))


def run():
    app = App()
    app.mainloop()