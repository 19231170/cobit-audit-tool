import customtkinter as ctk
from typing import Dict, Any, Callable
from app.core.database import DatabaseManager
from app.core.assessment_engine import ISO15504Engine, PROCESS_ATTRIBUTES
from app.widgets.rating_selector import RatingSelectorWidget
from app.themes.config import ThemeConfig

class AssessmentView(ctk.CTkFrame):
    def __init__(self, master, db: DatabaseManager, project_id: int, on_updated: Callable[[], None], **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.db = db
        self.project_id = project_id
        self.on_updated = on_updated
        self.engine = ISO15504Engine()

        self.selected_process_id = None
        self.current_ratings = {}
        self.evidence_inputs = {}
        self.notes_inputs = {}

        self._build_ui()
        self._load_processes()

    def _build_ui(self):
        header = ctk.CTkLabel(
            self, text="📋 Assessment Kapabilitas (ISO/IEC 15504)", font=ctk.CTkFont(size=22, weight="bold"),
            text_color=ThemeConfig.TEXT_LIGHT
        )
        header.pack(anchor="w", padx=20, pady=(20, 15))

        split = ctk.CTkFrame(self, fg_color="transparent")
        split.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # Left Panel: Process List
        left_panel = ctk.CTkFrame(split, fg_color=ThemeConfig.CARD_BG_DARK, corner_radius=10, width=280)
        left_panel.pack(side="left", fill="y", padx=(0, 10))

        ctk.CTkLabel(left_panel, text="Daftar Proses Audit", font=ctk.CTkFont(size=15, weight="bold")).pack(anchor="w", padx=16, pady=12)
        self.proc_scroll = ctk.CTkScrollableFrame(left_panel, fg_color="transparent", width=260)
        self.proc_scroll.pack(fill="both", expand=True, padx=8, pady=(0, 12))

        # Right Panel: Assessment Form
        self.right_panel = ctk.CTkFrame(split, fg_color=ThemeConfig.CARD_BG_DARK, corner_radius=10)
        self.right_panel.pack(side="right", fill="both", expand=True, padx=(10, 0))

        self.form_header = ctk.CTkLabel(self.right_panel, text="Pilih proses di sebelah kiri untuk memulai assessment.",
                                        font=ctk.CTkFont(size=15), text_color=ThemeConfig.TEXT_MUTED)
        self.form_header.pack(pady=40)

        self.form_scroll = ctk.CTkScrollableFrame(self.right_panel, fg_color="transparent")

    def _load_processes(self):
        for w in self.proc_scroll.winfo_children():
            w.destroy()

        procs = self.db.get_project_processes(self.project_id)
        if not procs:
            ctk.CTkLabel(self.proc_scroll, text="Belum ada proses terpilih.\nSilakan gunakan Goal Cascade terlebih dahulu.",
                         font=ctk.CTkFont(size=12), text_color=ThemeConfig.TEXT_MUTED).pack(pady=20)
            return

        for p in procs:
            # Check capability level
            existing_ass = self.db.get_assessments(self.project_id, p["process_id"])
            ratings = {a.attribute_code: a.rating for a in existing_ass}
            cap_lvl = self.engine.calculate_capability_level(ratings)

            btn = ctk.CTkButton(
                self.proc_scroll, text=f"{p['process_code']} (Lvl {cap_lvl}/{p['target_level']})",
                font=ctk.CTkFont(size=13), anchor="w", fg_color="transparent",
                hover_color=ThemeConfig.SECONDARY, height=36,
                command=lambda pid=p["process_id"], code=p["process_code"], name=p["name"], target=p["target_level"]: self._select_process(pid, code, name, target)
            )
            btn.pack(fill="x", pady=3)

    def _select_process(self, process_id: int, code: str, name: str, target_level: int):
        self.selected_process_id = process_id
        if self.form_header.winfo_exists():
            self.form_header.pack_forget()
        self.form_scroll.pack(fill="both", expand=True, padx=16, pady=16)

        for w in self.form_scroll.winfo_children():
            w.destroy()

        # Load saved ratings
        existing_ass = self.db.get_assessments(self.project_id, process_id)
        self.current_ratings = {a.attribute_code: a.rating for a in existing_ass}
        evidence_saved = {a.attribute_code: a.evidence for a in existing_ass}

        # Header Info
        header_f = ctk.CTkFrame(self.form_scroll, fg_color="transparent")
        header_f.pack(fill="x", pady=(0, 16))

        ctk.CTkLabel(header_f, text=f"{code} - {name}", font=ctk.CTkFont(size=18, weight="bold"),
                     text_color=ThemeConfig.TEXT_LIGHT).pack(anchor="w")
        ctk.CTkLabel(header_f, text=f"Target Capability Level: {target_level}", font=ctk.CTkFont(size=13),
                     text_color=ThemeConfig.PRIMARY).pack(anchor="w")

        # Level 1 to 5 Sections
        for lvl in range(1, 6):
            is_unlocked = self.engine.is_level_unlocked(lvl, self.current_ratings)
            lvl_frame = ctk.CTkFrame(self.form_scroll, fg_color=ThemeConfig.SECONDARY if is_unlocked else "#141B24", corner_radius=8)
            lvl_frame.pack(fill="x", pady=8, padx=4)

            lvl_title = f"Level {lvl} {'(Terkunci 🔒)' if not is_unlocked else ''}"
            ctk.CTkLabel(lvl_frame, text=lvl_title, font=ctk.CTkFont(size=14, weight="bold"),
                         text_color=ThemeConfig.TEXT_LIGHT if is_unlocked else ThemeConfig.TEXT_MUTED).pack(anchor="w", padx=12, pady=(10, 6))

            if is_unlocked:
                for pa_code, pa_name in PROCESS_ATTRIBUTES[lvl]:
                    attr_f = ctk.CTkFrame(lvl_frame, fg_color="transparent")
                    attr_f.pack(fill="x", padx=12, pady=6)

                    ctk.CTkLabel(attr_f, text=f"{pa_code}: {pa_name}", font=ctk.CTkFont(size=13), anchor="w").pack(anchor="w")

                    # Rating Selector
                    cur_r = self.current_ratings.get(pa_code)
                    sel = RatingSelectorWidget(
                        attr_f, current_rating=cur_r,
                        on_change=lambda r, code=pa_code: self._on_rating_selected(code, r)
                    )
                    sel.pack(anchor="w", pady=(4, 6))

                    # Evidence input
                    ctk.CTkLabel(attr_f, text="Bukti Audit (Evidence):", font=ctk.CTkFont(size=11), text_color=ThemeConfig.TEXT_MUTED).pack(anchor="w")
                    ev_entry = ctk.CTkEntry(attr_f, placeholder_text="Dokumen SOP / Screenshot / Wawancara...")
                    if pa_code in evidence_saved:
                        ev_entry.insert(0, evidence_saved[pa_code])
                    ev_entry.pack(fill="x", pady=(2, 6))
                    self.evidence_inputs[pa_code] = ev_entry

        # Bottom Bar: Capability Level summary & Save
        calc_lvl = self.engine.calculate_capability_level(self.current_ratings)
        bottom_f = ctk.CTkFrame(self.form_scroll, fg_color="transparent")
        bottom_f.pack(fill="x", pady=16)

        ctk.CTkLabel(bottom_f, text=f"Tingkat Kapabilitas Tercapai: Level {calc_lvl}",
                     font=ctk.CTkFont(size=16, weight="bold"), text_color=ThemeConfig.ACCENT_GREEN).pack(side="left")

        save_btn = ctk.CTkButton(
            bottom_f, text="💾 Simpan Hasil Assessment", font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=ThemeConfig.PRIMARY, hover_color=ThemeConfig.PRIMARY_HOVER,
            command=self._save_assessment
        )
        save_btn.pack(side="right")

    def _on_rating_selected(self, pa_code: str, rating: str):
        self.current_ratings[pa_code] = rating

    def _save_assessment(self):
        if not self.selected_process_id:
            return

        for lvl, pas in PROCESS_ATTRIBUTES.items():
            for pa_code, pa_name in pas:
                rating = self.current_ratings.get(pa_code)
                ev = self.evidence_inputs[pa_code].get().strip() if pa_code in self.evidence_inputs else ""
                self.db.save_assessment(
                    self.project_id, self.selected_process_id, lvl, pa_code, pa_name, rating, evidence=ev
                )

        self._load_processes()
        self.on_updated()
