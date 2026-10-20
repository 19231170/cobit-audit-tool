import customtkinter as ctk
from typing import Callable
from app.core.database import DatabaseManager
from app.widgets.project_card import ProjectCardWidget
from app.themes.config import ThemeConfig

class DashboardView(ctk.CTkFrame):
    def __init__(self, master, db: DatabaseManager, on_open_project: Callable[[int], None], **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.db = db
        self.on_open_project = on_open_project

        self._build_ui()
        self.refresh()

    def _build_ui(self):
        top_bar = ctk.CTkFrame(self, fg_color="transparent")
        top_bar.pack(fill="x", padx=20, pady=(20, 15))

        title = ctk.CTkLabel(
            top_bar, text="📊 Dashboard Proyek Audit", font=ctk.CTkFont(size=22, weight="bold"),
            text_color=ThemeConfig.TEXT_LIGHT
        )
        title.pack(side="left")

        new_proj_btn = ctk.CTkButton(
            top_bar, text="+ Buat Proyek Audit Baru", font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=ThemeConfig.PRIMARY, hover_color=ThemeConfig.PRIMARY_HOVER, height=36,
            command=self._open_new_project_dialog
        )
        new_proj_btn.pack(side="right")

        self.cards_scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.cards_scroll.pack(fill="both", expand=True, padx=20, pady=(0, 20))

    def refresh(self):
        for w in self.cards_scroll.winfo_children():
            w.destroy()

        projects = self.db.get_projects()
        if not projects:
            ctk.CTkLabel(
                self.cards_scroll, text="Belum ada proyek audit.\nKlik tombol '+ Buat Proyek Audit Baru' untuk memulai.",
                font=ctk.CTkFont(size=14), text_color=ThemeConfig.TEXT_MUTED
            ).pack(pady=40)
            return

        for p in projects:
            procs = self.db.get_project_processes(p.id)
            if procs:
                ass_done = sum(1 for item in procs if self.db.get_assessments(p.id, item["process_id"]))
                prog = ass_done / len(procs)
            else:
                prog = 0.0

            card = ProjectCardWidget(self.cards_scroll, project=p, progress=prog, on_open=self.on_open_project)
            card.pack(fill="x", pady=8)

    def _open_new_project_dialog(self):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Buat Proyek Audit Baru")
        dialog.geometry("450x380")
        dialog.grab_set()

        ctk.CTkLabel(dialog, text="Nama Organisasi / Klien:").pack(anchor="w", padx=20, pady=(20, 4))
        name_entry = ctk.CTkEntry(dialog, placeholder_text="Misal: PT Bank Sejahtera")
        name_entry.pack(fill="x", padx=20, pady=(0, 10))

        ctk.CTkLabel(dialog, text="Versi Framework COBIT:").pack(anchor="w", padx=20, pady=(4, 4))
        ver_menu = ctk.CTkOptionMenu(dialog, values=["COBIT2019", "COBIT5"])
        ver_menu.pack(fill="x", padx=20, pady=(0, 10))

        ctk.CTkLabel(dialog, text="Deskripsi Audit:").pack(anchor="w", padx=20, pady=(4, 4))
        desc_entry = ctk.CTkEntry(dialog, placeholder_text="Audit tahunan tata kelola IT...")
        desc_entry.pack(fill="x", padx=20, pady=(0, 10))

        ctk.CTkLabel(dialog, text="Tanggal Mulai (YYYY-MM-DD):").pack(anchor="w", padx=20, pady=(4, 4))
        date_entry = ctk.CTkEntry(dialog, placeholder_text="2026-10-20")
        date_entry.insert(0, "2026-10-20")
        date_entry.pack(fill="x", padx=20, pady=(0, 20))

        def create():
            name = name_entry.get().strip()
            if not name:
                return
            pid = self.db.create_project(name, ver_menu.get(), desc_entry.get().strip(), date_entry.get().strip())
            dialog.destroy()
            self.refresh()
            self.on_open_project(pid)

        create_btn = ctk.CTkButton(dialog, text="Buat Proyek", command=create, fg_color=ThemeConfig.PRIMARY)
        create_btn.pack(pady=10)
