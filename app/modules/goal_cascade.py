import customtkinter as ctk
from typing import List, Dict, Any, Callable
from app.core.database import DatabaseManager
from app.themes.config import ThemeConfig

class GoalCascadeView(ctk.CTkFrame):
    def __init__(self, master, db: DatabaseManager, project_id: int, on_saved: Callable[[], None], **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.db = db
        self.project_id = project_id
        self.on_saved = on_saved
        self.project = self.db.get_project_by_id(project_id)

        self.eg_checkboxes = {}
        self.process_checkboxes = {}

        self._build_ui()
        self._load_enterprise_goals()

    def _build_ui(self):
        header = ctk.CTkLabel(
            self, text="🎯 Goal Cascade Helper", font=ctk.CTkFont(size=22, weight="bold"),
            text_color=ThemeConfig.TEXT_LIGHT
        )
        header.pack(anchor="w", padx=20, pady=(20, 10))

        sub = ctk.CTkLabel(
            self, text=f"Framework: {self.project.cobit_version} | Pilih Enterprise Goals untuk auto-mapping ke Alignment Goals dan Proses.",
            font=ctk.CTkFont(size=13), text_color=ThemeConfig.TEXT_MUTED
        )
        sub.pack(anchor="w", padx=20, pady=(0, 20))

        # 3-Column Layout
        self.cols_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.cols_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # Col 1: Enterprise Goals
        col1 = ctk.CTkFrame(self.cols_frame, fg_color=ThemeConfig.CARD_BG_DARK, corner_radius=10)
        col1.pack(side="left", fill="both", expand=True, padx=(0, 8))
        ctk.CTkLabel(col1, text="1. Enterprise Goals", font=ctk.CTkFont(size=15, weight="bold")).pack(anchor="w", padx=16, pady=12)
        self.eg_scroll = ctk.CTkScrollableFrame(col1, fg_color="transparent")
        self.eg_scroll.pack(fill="both", expand=True, padx=8, pady=(0, 12))

        # Col 2: Alignment Goals
        col2 = ctk.CTkFrame(self.cols_frame, fg_color=ThemeConfig.CARD_BG_DARK, corner_radius=10)
        col2.pack(side="left", fill="both", expand=True, padx=8)
        ctk.CTkLabel(col2, text="2. Alignment Goals (Auto)", font=ctk.CTkFont(size=15, weight="bold")).pack(anchor="w", padx=16, pady=12)
        self.ag_scroll = ctk.CTkScrollableFrame(col2, fg_color="transparent")
        self.ag_scroll.pack(fill="both", expand=True, padx=8, pady=(0, 12))

        # Col 3: Processes
        col3 = ctk.CTkFrame(self.cols_frame, fg_color=ThemeConfig.CARD_BG_DARK, corner_radius=10)
        col3.pack(side="left", fill="both", expand=True, padx=(8, 0))
        ctk.CTkLabel(col3, text="3. Proses Governance/Mgmt", font=ctk.CTkFont(size=15, weight="bold")).pack(anchor="w", padx=16, pady=12)
        self.proc_scroll = ctk.CTkScrollableFrame(col3, fg_color="transparent")
        self.proc_scroll.pack(fill="both", expand=True, padx=8, pady=(0, 12))

        # Action Buttons
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        save_btn = ctk.CTkButton(
            btn_frame, text="💾 Simpan Hasil Mapping ke Proyek", font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=ThemeConfig.PRIMARY, hover_color=ThemeConfig.PRIMARY_HOVER, height=40,
            command=self._save_selection
        )
        save_btn.pack(side="right")

    def _load_enterprise_goals(self):
        with self.db.get_connection() as conn:
            rows = conn.execute(
                "SELECT * FROM enterprise_goals WHERE cobit_version = ? ORDER BY goal_code",
                (self.project.cobit_version,)
            ).fetchall()

        for r in rows:
            cb = ctk.CTkCheckBox(
                self.eg_scroll, text=f"{r['goal_code']} - {r['description']}",
                font=ctk.CTkFont(size=12), command=self._on_eg_toggled
            )
            cb.pack(anchor="w", pady=6, padx=8)
            self.eg_checkboxes[r["id"]] = cb

    def _on_eg_toggled(self):
        selected_egs = [eg_id for eg_id, cb in self.eg_checkboxes.items() if cb.get() == 1]
        
        # Clear Col 2 and Col 3
        for w in self.ag_scroll.winfo_children():
            w.destroy()
        for w in self.proc_scroll.winfo_children():
            w.destroy()
        self.process_checkboxes.clear()

        if not selected_egs:
            return

        with self.db.get_connection() as conn:
            # Query AGs
            placeholders = ",".join("?" for _ in selected_egs)
            ag_rows = conn.execute(
                f"""SELECT DISTINCT ag.id, ag.goal_code, ag.description, gm.relationship
                    FROM alignment_goals ag
                    JOIN goal_mapping gm ON ag.id = gm.alignment_goal_id
                    WHERE gm.enterprise_goal_id IN ({placeholders})
                    ORDER BY ag.goal_code""",
                selected_egs
            ).fetchall()

            for ag in ag_rows:
                badge = f"[{ag['relationship']}] " if ag["relationship"] else ""
                lbl = ctk.CTkLabel(
                    self.ag_scroll, text=f"{badge}{ag['goal_code']} - {ag['description']}",
                    font=ctk.CTkFont(size=12), text_color=ThemeConfig.TEXT_LIGHT, anchor="w", wraplength=220
                )
                lbl.pack(anchor="w", pady=4, padx=8)

            # Query Processes
            ag_ids = [ag["id"] for ag in ag_rows]
            if not ag_ids:
                return
            ag_placeholders = ",".join("?" for _ in ag_ids)
            proc_rows = conn.execute(
                f"""SELECT DISTINCT p.id, p.domain, p.process_code, p.name
                    FROM processes p
                    JOIN goal_process_mapping gpm ON p.id = gpm.process_id
                    WHERE gpm.alignment_goal_id IN ({ag_placeholders})
                    ORDER BY p.process_code""",
                ag_ids
            ).fetchall()

            for p in proc_rows:
                cb = ctk.CTkCheckBox(
                    self.proc_scroll, text=f"{p['process_code']} - {p['name']}",
                    font=ctk.CTkFont(size=12)
                )
                cb.select()  # Auto-select mapped processes
                cb.pack(anchor="w", pady=4, padx=8)
                self.process_checkboxes[p["id"]] = cb

    def _save_selection(self):
        selected_procs = [pid for pid, cb in self.process_checkboxes.items() if cb.get() == 1]
        with self.db.get_connection() as conn:
            # Clean and re-insert
            conn.execute("DELETE FROM project_processes WHERE project_id = ?", (self.project_id,))
            for pid in selected_procs:
                conn.execute(
                    "INSERT INTO project_processes (project_id, process_id, target_level) VALUES (?, ?, 3)",
                    (self.project_id, pid)
                )
        self.on_saved()
