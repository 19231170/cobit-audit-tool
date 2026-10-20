import os
import customtkinter as ctk
from tkinter import filedialog, messagebox
from app.core.database import DatabaseManager
from app.core.exporter import PDFReportGenerator
from app.widgets.chart_widget import generate_bar_chart, generate_radar_chart, EmbeddedChartWidget
from app.core.assessment_engine import ISO15504Engine
from app.themes.config import ThemeConfig

class ReportsView(ctk.CTkFrame):
    def __init__(self, master, db: DatabaseManager, project_id: int, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.db = db
        self.project_id = project_id
        self.engine = ISO15504Engine()

        self._build_ui()

    def _build_ui(self):
        header = ctk.CTkLabel(
            self, text="📈 Laporan & Visualisasi Audit", font=ctk.CTkFont(size=22, weight="bold"),
            text_color=ThemeConfig.TEXT_LIGHT
        )
        header.pack(anchor="w", padx=20, pady=(20, 10))

        # Action Bar: Export PDF
        action_bar = ctk.CTkFrame(self, fg_color="transparent")
        action_bar.pack(fill="x", padx=20, pady=(0, 15))

        pdf_btn = ctk.CTkButton(
            action_bar, text="📄 Export Laporan Lengkap ke PDF", font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=ThemeConfig.PRIMARY, hover_color=ThemeConfig.PRIMARY_HOVER, height=38,
            command=self._export_pdf
        )
        pdf_btn.pack(side="right")

        # Scrollable charts & stats
        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # Data resolution
        procs = self.db.get_project_processes(self.project_id)
        codes, actuals, targets = [], [], []
        domain_map = {"EDM": [], "APO": [], "BAI": [], "DSS": [], "MEA": []}

        for p in procs:
            ass = self.db.get_assessments(self.project_id, p["process_id"])
            ratings = {a.attribute_code: a.rating for a in ass}
            act = self.engine.calculate_capability_level(ratings)
            codes.append(p["process_code"])
            actuals.append(act)
            targets.append(p["target_level"])
            d = p.get("domain", "APO")
            if d in domain_map:
                domain_map[d].append(act)

        # Bar chart
        if codes:
            b_frame = ctk.CTkFrame(scroll, fg_color=ThemeConfig.CARD_BG_DARK, corner_radius=10)
            b_frame.pack(fill="x", pady=8)
            ctk.CTkLabel(b_frame, text="Perbandingan Capability Level (Aktual vs Target)", font=ctk.CTkFont(size=15, weight="bold")).pack(anchor="w", padx=16, pady=12)
            fig_bar = generate_bar_chart(codes, actuals, targets)
            embed_b = EmbeddedChartWidget(b_frame, fig_bar)
            embed_b.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        # Radar chart
        domains = list(domain_map.keys())
        domain_acts = [float(sum(v)/len(v)) if v else 0.0 for v in domain_map.values()]
        domain_targs = [3.0] * len(domains)

        r_frame = ctk.CTkFrame(scroll, fg_color=ThemeConfig.CARD_BG_DARK, corner_radius=10)
        r_frame.pack(fill="x", pady=8)
        ctk.CTkLabel(r_frame, text="Radar Tingkat Kapabilitas Per Domain", font=ctk.CTkFont(size=15, weight="bold")).pack(anchor="w", padx=16, pady=12)
        fig_radar = generate_radar_chart(domains, domain_acts, domain_targs)
        embed_r = EmbeddedChartWidget(r_frame, fig_radar)
        embed_r.pack(fill="both", expand=True, padx=12, pady=(0, 12))

    def _export_pdf(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF Document", "*.pdf")],
            title="Simpan Laporan Audit"
        )
        if not file_path:
            return

        try:
            gen = PDFReportGenerator(self.db)
            gen.generate_audit_report(self.project_id, file_path)
            messagebox.showinfo("Berhasil", f"Laporan audit PDF berhasil disimpan ke:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Gagal", f"Terjadi kesalahan saat membuat PDF:\n{str(e)}")
