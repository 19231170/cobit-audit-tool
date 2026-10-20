import customtkinter as ctk
from typing import Dict, Any, List
from app.core.database import DatabaseManager
from app.themes.config import ThemeConfig, RACI_COLORS

class RaciView(ctk.CTkFrame):
    def __init__(self, master, db: DatabaseManager, project_id: int, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.db = db
        self.project_id = project_id
        self.project = self.db.get_project_by_id(project_id)
        
        self.filter_domain = "SEMUA"
        self.role_inputs = {}
        
        self._build_ui()
        self._load_raci_matrix()
        self._load_role_mappings()

    def _build_ui(self):
        header = ctk.CTkLabel(
            self, text="👥 RACI Chart & Pemetaan Jabatan", font=ctk.CTkFont(size=22, weight="bold"),
            text_color=ThemeConfig.TEXT_LIGHT
        )
        header.pack(anchor="w", padx=20, pady=(20, 5))

        # Legend & Filter
        top_bar = ctk.CTkFrame(self, fg_color="transparent")
        top_bar.pack(fill="x", padx=20, pady=(0, 15))

        legend_txt = "Legenda: 🟦 R (Responsible) | 🟥 A (Accountable) | 🟨 C (Consulted) | 🟩 I (Informed)"
        ctk.CTkLabel(top_bar, text=legend_txt, font=ctk.CTkFont(size=12), text_color=ThemeConfig.TEXT_MUTED).pack(side="left")

        self.domain_dropdown = ctk.CTkOptionMenu(
            top_bar, values=["SEMUA", "EDM", "APO", "BAI", "DSS", "MEA"],
            command=self._on_domain_filter_changed, width=120
        )
        self.domain_dropdown.pack(side="right")
        ctk.CTkLabel(top_bar, text="Filter Domain: ", font=ctk.CTkFont(size=12)).pack(side="right", padx=6)

        # Main Split
        main_split = ctk.CTkFrame(self, fg_color="transparent")
        main_split.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # Left: RACI Matrix
        matrix_frame = ctk.CTkFrame(main_split, fg_color=ThemeConfig.CARD_BG_DARK, corner_radius=10)
        matrix_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))

        ctk.CTkLabel(matrix_frame, text="Matriks RACI Per Proses", font=ctk.CTkFont(size=15, weight="bold")).pack(anchor="w", padx=16, pady=12)
        self.matrix_scroll = ctk.CTkScrollableFrame(matrix_frame, fg_color="transparent")
        self.matrix_scroll.pack(fill="both", expand=True, padx=8, pady=(0, 12))

        # Right: Role Mapping
        mapping_frame = ctk.CTkFrame(main_split, fg_color=ThemeConfig.CARD_BG_DARK, corner_radius=10, width=320)
        mapping_frame.pack(side="right", fill="y", padx=(10, 0))

        ctk.CTkLabel(mapping_frame, text="Pemetaan ke Jabatan Nyata", font=ctk.CTkFont(size=15, weight="bold")).pack(anchor="w", padx=16, pady=12)
        self.mapping_scroll = ctk.CTkScrollableFrame(mapping_frame, fg_color="transparent", width=300)
        self.mapping_scroll.pack(fill="both", expand=True, padx=8, pady=(0, 12))

        save_mapping_btn = ctk.CTkButton(
            mapping_frame, text="💾 Simpan Pemetaan Jabatan", font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=ThemeConfig.PRIMARY, hover_color=ThemeConfig.PRIMARY_HOVER,
            command=self._save_role_mappings
        )
        save_mapping_btn.pack(fill="x", padx=16, pady=12)

    def _on_domain_filter_changed(self, choice: str):
        self.filter_domain = choice
        self._load_raci_matrix()

    def _load_raci_matrix(self):
        for w in self.matrix_scroll.winfo_children():
            w.destroy()

        with self.db.get_connection() as conn:
            procs = self.db.get_project_processes(self.project_id)
            if not procs:
                procs = conn.execute("SELECT * FROM processes WHERE cobit_version = ? LIMIT 10", (self.project.cobit_version,)).fetchall()
                procs = [dict(p) for p in procs]

            if self.filter_domain != "SEMUA":
                procs = [p for p in procs if p["domain"] == self.filter_domain]

            roles = ["Board", "CEO", "CIO", "CISO", "Auditor"]

            # Header row
            h_row = ctk.CTkFrame(self.matrix_scroll, fg_color=ThemeConfig.SECONDARY)
            h_row.pack(fill="x", pady=2)
            ctk.CTkLabel(h_row, text="Proses", width=140, anchor="w", font=ctk.CTkFont(weight="bold")).pack(side="left", padx=6)
            for r in roles:
                ctk.CTkLabel(h_row, text=r, width=70, font=ctk.CTkFont(weight="bold")).pack(side="left", padx=4)

            # Data rows
            for p in procs:
                row_f = ctk.CTkFrame(self.matrix_scroll, fg_color="transparent")
                row_f.pack(fill="x", pady=2)
                ctk.CTkLabel(row_f, text=f"{p['process_code']}", width=140, anchor="w").pack(side="left", padx=6)

                raci_map = {}
                r_rows = conn.execute("SELECT role_name, raci_type FROM raci_entries WHERE process_id = ?", (p.get("process_id", p.get("id")),)).fetchall()
                for r_item in r_rows:
                    raci_map[r_item["role_name"]] = r_item["raci_type"]

                for r in roles:
                    rtype = raci_map.get(r, "-")
                    color = RACI_COLORS.get(rtype, ThemeConfig.TEXT_MUTED)
                    badge = ctk.CTkLabel(row_f, text=rtype, width=70, font=ctk.CTkFont(weight="bold"), text_color=color)
                    badge.pack(side="left", padx=4)

    def _load_role_mappings(self):
        for w in self.mapping_scroll.winfo_children():
            w.destroy()
        self.role_inputs.clear()

        cobit_roles = ["Board / Dewan Komisaris", "CEO / Direktur Utama", "CIO / Kepala Divisi IT", "CISO / IT Security Lead", "Head of IT Ops", "Head of Dev", "Internal Auditor"]

        with self.db.get_connection() as conn:
            saved = dict(conn.execute("SELECT cobit_role, org_position FROM role_mapping WHERE project_id = ?", (self.project_id,)).fetchall())

        for cr in cobit_roles:
            lbl = ctk.CTkLabel(self.mapping_scroll, text=cr, font=ctk.CTkFont(size=12), text_color=ThemeConfig.TEXT_LIGHT, anchor="w")
            lbl.pack(fill="x", padx=4, pady=(6, 2))

            entry = ctk.CTkEntry(self.mapping_scroll, placeholder_text="Jabatan di organisasi...")
            if cr in saved:
                entry.insert(0, saved[cr])
            entry.pack(fill="x", padx=4, pady=(0, 6))
            self.role_inputs[cr] = entry

    def _save_role_mappings(self):
        with self.db.get_connection() as conn:
            conn.execute("DELETE FROM role_mapping WHERE project_id = ?", (self.project_id,))
            for cr, entry in self.role_inputs.items():
                val = entry.get().strip()
                if val:
                    conn.execute("INSERT INTO role_mapping (project_id, cobit_role, org_position) VALUES (?, ?, ?)",
                                 (self.project_id, cr, val))
