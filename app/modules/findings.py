import customtkinter as ctk
from typing import Dict, Any, List
from app.core.database import DatabaseManager
from app.core.assessment_engine import ISO15504Engine
from app.themes.config import ThemeConfig

class FindingsView(ctk.CTkFrame):
    def __init__(self, master, db: DatabaseManager, project_id: int, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.db = db
        self.project_id = project_id
        self.engine = ISO15504Engine()

        self._build_ui()
        self._load_gap_analysis()
        self._load_findings()

    def _build_ui(self):
        header = ctk.CTkLabel(
            self, text="🔍 Temuan Audit & Gap Analysis", font=ctk.CTkFont(size=22, weight="bold"),
            text_color=ThemeConfig.TEXT_LIGHT
        )
        header.pack(anchor="w", padx=20, pady=(20, 15))

        self.tabview = ctk.CTkTabview(self, fg_color=ThemeConfig.CARD_BG_DARK)
        self.tabview.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        self.tab_gap = self.tabview.add("📊 Analisis Gap")
        self.tab_findings = self.tabview.add("📝 Daftar Temuan")

        # Gap Tab
        self.gap_scroll = ctk.CTkScrollableFrame(self.tab_gap, fg_color="transparent")
        self.gap_scroll.pack(fill="both", expand=True, padx=12, pady=12)

        # Findings Tab Header
        top_f = ctk.CTkFrame(self.tab_findings, fg_color="transparent")
        top_f.pack(fill="x", padx=12, pady=12)

        add_btn = ctk.CTkButton(
            top_f, text="+ Tambah Temuan Baru", font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=ThemeConfig.PRIMARY, hover_color=ThemeConfig.PRIMARY_HOVER,
            command=self._open_add_finding_dialog
        )
        add_btn.pack(side="right")

        self.findings_scroll = ctk.CTkScrollableFrame(self.tab_findings, fg_color="transparent")
        self.findings_scroll.pack(fill="both", expand=True, padx=12, pady=(0, 12))

    def _load_gap_analysis(self):
        for w in self.gap_scroll.winfo_children():
            w.destroy()

        procs = self.db.get_project_processes(self.project_id)
        if not procs:
            ctk.CTkLabel(self.gap_scroll, text="Belum ada proses yang di-audit.", text_color=ThemeConfig.TEXT_MUTED).pack(pady=20)
            return

        # Header Row
        h_row = ctk.CTkFrame(self.gap_scroll, fg_color=ThemeConfig.SECONDARY)
        h_row.pack(fill="x", pady=2)
        ctk.CTkLabel(h_row, text="Proses", width=180, anchor="w", font=ctk.CTkFont(weight="bold")).pack(side="left", padx=8)
        ctk.CTkLabel(h_row, text="Aktual", width=80, font=ctk.CTkFont(weight="bold")).pack(side="left", padx=4)
        ctk.CTkLabel(h_row, text="Target", width=80, font=ctk.CTkFont(weight="bold")).pack(side="left", padx=4)
        ctk.CTkLabel(h_row, text="Gap", width=80, font=ctk.CTkFont(weight="bold")).pack(side="left", padx=4)
        ctk.CTkLabel(h_row, text="Status", width=120, font=ctk.CTkFont(weight="bold")).pack(side="left", padx=4)

        for p in procs:
            ass = self.db.get_assessments(self.project_id, p["process_id"])
            ratings = {a.attribute_code: a.rating for a in ass}
            actual = self.engine.calculate_capability_level(ratings)
            target = p["target_level"]
            gap, status = self.engine.calculate_gap(actual, target)

            status_color = ThemeConfig.ACCENT_GREEN if status == "tercapai" else (
                ThemeConfig.ACCENT_YELLOW if status == "gap_kecil" else ThemeConfig.ACCENT_RED
            )
            status_label = "🟢 Tercapai" if status == "tercapai" else (
                "🟡 Gap Kecil" if status == "gap_kecil" else "🔴 Gap Besar"
            )

            row = ctk.CTkFrame(self.gap_scroll, fg_color="transparent")
            row.pack(fill="x", pady=2)
            ctk.CTkLabel(row, text=f"{p['process_code']} - {p['name']}", width=180, anchor="w").pack(side="left", padx=8)
            ctk.CTkLabel(row, text=str(actual), width=80).pack(side="left", padx=4)
            ctk.CTkLabel(row, text=str(target), width=80).pack(side="left", padx=4)
            ctk.CTkLabel(row, text=str(gap), width=80, text_color=status_color, font=ctk.CTkFont(weight="bold")).pack(side="left", padx=4)
            ctk.CTkLabel(row, text=status_label, width=120, text_color=status_color).pack(side="left", padx=4)

    def _load_findings(self):
        for w in self.findings_scroll.winfo_children():
            w.destroy()

        all_f = self.db.get_findings(self.project_id)
        if not all_f:
            ctk.CTkLabel(self.findings_scroll, text="Belum ada temuan yang dicatat.", text_color=ThemeConfig.TEXT_MUTED).pack(pady=20)
            return

        for f in all_f:
            card = ctk.CTkFrame(self.findings_scroll, fg_color=ThemeConfig.SECONDARY, corner_radius=8)
            card.pack(fill="x", pady=6, padx=4)

            prio_color = ThemeConfig.ACCENT_RED if f["priority"] == 1 else (
                ThemeConfig.ACCENT_YELLOW if f["priority"] == 2 else ThemeConfig.PRIMARY
            )
            ctk.CTkLabel(card, text=f"Prioritas {f['priority']} | {f['process_code']} - Dampak: {f['impact_level'].upper()}",
                         font=ctk.CTkFont(size=13, weight="bold"), text_color=prio_color).pack(anchor="w", padx=12, pady=(10, 4))

            ctk.CTkLabel(card, text=f"Kondisi: {f['condition_text']}", font=ctk.CTkFont(size=12), anchor="w", wraplength=700).pack(anchor="w", padx=12, pady=2)
            ctk.CTkLabel(card, text=f"Kriteria: {f['criteria_text']}", font=ctk.CTkFont(size=12, slant="italic"), text_color=ThemeConfig.TEXT_MUTED, anchor="w", wraplength=700).pack(anchor="w", padx=12, pady=2)
            ctk.CTkLabel(card, text=f"Rekomendasi: {f['recommendation']}", font=ctk.CTkFont(size=12, weight="bold"), text_color=ThemeConfig.TEXT_LIGHT, anchor="w", wraplength=700).pack(anchor="w", padx=12, pady=(4, 10))

    def _open_add_finding_dialog(self):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Tambah Temuan Audit")
        dialog.geometry("600x580")
        dialog.grab_set()

        procs = self.db.get_project_processes(self.project_id)
        proc_options = [f"{p['process_code']} - {p['name']}" for p in procs] or ["Umum"]

        ctk.CTkLabel(dialog, text="Proses:").pack(anchor="w", padx=20, pady=(15, 2))
        proc_menu = ctk.CTkOptionMenu(dialog, values=proc_options)
        proc_menu.pack(fill="x", padx=20, pady=(0, 8))

        ctk.CTkLabel(dialog, text="Kondisi Saat Ini:").pack(anchor="w", padx=20, pady=(4, 2))
        cond_entry = ctk.CTkEntry(dialog, placeholder_text="Fakta aktual di lapangan...")
        cond_entry.pack(fill="x", padx=20, pady=(0, 8))

        ctk.CTkLabel(dialog, text="Kriteria (Standar COBIT):").pack(anchor="w", padx=20, pady=(4, 2))
        crit_entry = ctk.CTkEntry(dialog, placeholder_text="Ketentuan standar seharusnya...")
        crit_entry.pack(fill="x", padx=20, pady=(0, 8))

        ctk.CTkLabel(dialog, text="Sebab:").pack(anchor="w", padx=20, pady=(4, 2))
        cause_entry = ctk.CTkEntry(dialog, placeholder_text="Penyebab akar masalah...")
        cause_entry.pack(fill="x", padx=20, pady=(0, 8))

        ctk.CTkLabel(dialog, text="Prioritas:").pack(anchor="w", padx=20, pady=(4, 2))
        prio_menu = ctk.CTkOptionMenu(dialog, values=["1 - Kritis", "2 - Tinggi", "3 - Sedang", "4 - Rendah"])
        prio_menu.pack(fill="x", padx=20, pady=(0, 8))

        ctk.CTkLabel(dialog, text="Rekomendasi:").pack(anchor="w", padx=20, pady=(4, 2))
        rec_entry = ctk.CTkEntry(dialog, placeholder_text="Solusi konkret perbaikan...")
        rec_entry.pack(fill="x", padx=20, pady=(0, 16))

        def save():
            selected_txt = proc_menu.get()
            proc_code = selected_txt.split(" - ")[0]
            with self.db.get_connection() as conn:
                p_row = conn.execute("SELECT id FROM processes WHERE process_code = ?", (proc_code,)).fetchone()
                pid = p_row["id"] if p_row else procs[0]["process_id"]

            prio = int(prio_menu.get().split(" - ")[0])
            self.db.add_finding(
                self.project_id, pid, cond_entry.get().strip(), crit_entry.get().strip(),
                cause_entry.get().strip(), "high" if prio <= 2 else "medium", prio, rec_entry.get().strip()
            )
            dialog.destroy()
            self._load_findings()

        save_btn = ctk.CTkButton(dialog, text="Simpan Temuan", command=save, fg_color=ThemeConfig.PRIMARY)
        save_btn.pack(pady=10)
