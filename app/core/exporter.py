import os
import tempfile
from fpdf import FPDF
from fpdf.enums import XPos, YPos
from app.core.database import DatabaseManager
from app.core.assessment_engine import ISO15504Engine
from app.widgets.chart_widget import generate_radar_chart, generate_bar_chart

class AuditPDF(FPDF):
    def header(self):
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 8, 'COBIT Audit Tool - Laporan Hasil Audit Sistem Informasi', 
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='R')
        self.line(10, 16, 200, 16)
        self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Halaman {self.page_no()}', 
                  new_x=XPos.RIGHT, new_y=YPos.TOP, align='C')

class PDFReportGenerator:
    def __init__(self, db: DatabaseManager):
        self.db = db
        self.engine = ISO15504Engine()

    def generate_audit_report(self, project_id: int, output_path: str):
        proj = self.db.get_project_by_id(project_id)
        if not proj:
            raise ValueError("Proyek tidak ditemukan")

        pdf = AuditPDF(orientation='P', unit='mm', format='A4')
        pdf.set_margins(15, 15, 15)
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()

        epw = pdf.epw  # Effective page width (180mm)

        # Cover Title
        pdf.set_font("Helvetica", "B", 20)
        pdf.set_text_color(30, 144, 255)
        pdf.cell(epw, 15, "LAPORAN AUDIT TATA KELOLA IT", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
        
        pdf.set_font("Helvetica", "B", 15)
        pdf.set_text_color(40, 40, 40)
        pdf.cell(epw, 9, f"Organisasi: {proj.name}", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
        
        pdf.set_font("Helvetica", "", 11)
        pdf.set_text_color(100, 100, 100)
        pdf.cell(epw, 8, f"Framework: {proj.cobit_version} | Tanggal: {proj.start_date}", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
        pdf.ln(10)

        # 1. Ruang Lingkup
        pdf.set_font("Helvetica", "B", 13)
        pdf.set_text_color(30, 144, 255)
        pdf.cell(epw, 9, "1. Pendahuluan & Ruang Lingkup", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="L")
        
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(50, 50, 50)
        intro = proj.intro_text or (
            f"Laporan audit ini disusun sebagai hasil asesmen kapabilitas proses tata kelola dan manajemen teknologi "
            f"informasi pada {proj.name} berdasarkan kerangka kerja {proj.cobit_version} dan model asesmen ISO/IEC 15504."
        )
        pdf.multi_cell(epw, 6, intro)
        pdf.ln(6)

        # 2. Hasil Assessment & Charts
        pdf.set_font("Helvetica", "B", 13)
        pdf.set_text_color(30, 144, 255)
        pdf.cell(epw, 9, "2. Hasil Asesmen Kapabilitas Proses", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="L")
        
        procs = self.db.get_project_processes(project_id)
        codes, actuals, targets = [], [], []

        for p in procs:
            ass = self.db.get_assessments(project_id, p["process_id"])
            ratings = {a.attribute_code: a.rating for a in ass}
            act = self.engine.calculate_capability_level(ratings)
            codes.append(p["process_code"])
            actuals.append(act)
            targets.append(p["target_level"])

        # Create temporary bar chart
        with tempfile.TemporaryDirectory() as tmp_dir:
            if codes:
                chart_path = os.path.join(tmp_dir, "bar.png")
                generate_bar_chart(codes, actuals, targets, chart_path)
                pdf.image(chart_path, x=15, w=epw)
                pdf.ln(6)

            # Table Assessment (sum: 25 + 80 + 25 + 25 + 25 = 180 = epw)
            pdf.set_font("Helvetica", "B", 9)
            pdf.set_fill_color(240, 244, 248)
            pdf.cell(25, 8, "Kode", 1, new_x=XPos.RIGHT, new_y=YPos.TOP, align="C", fill=True)
            pdf.cell(80, 8, "Nama Proses", 1, new_x=XPos.RIGHT, new_y=YPos.TOP, align="L", fill=True)
            pdf.cell(25, 8, "Aktual", 1, new_x=XPos.RIGHT, new_y=YPos.TOP, align="C", fill=True)
            pdf.cell(25, 8, "Target", 1, new_x=XPos.RIGHT, new_y=YPos.TOP, align="C", fill=True)
            pdf.cell(25, 8, "Gap", 1, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C", fill=True)

            pdf.set_font("Helvetica", "", 9)
            for idx, p in enumerate(procs):
                gap = actuals[idx] - targets[idx]
                pdf.cell(25, 7, p["process_code"], 1, new_x=XPos.RIGHT, new_y=YPos.TOP, align="C")
                pdf.cell(80, 7, p["name"][:38], 1, new_x=XPos.RIGHT, new_y=YPos.TOP, align="L")
                pdf.cell(25, 7, str(actuals[idx]), 1, new_x=XPos.RIGHT, new_y=YPos.TOP, align="C")
                pdf.cell(25, 7, str(targets[idx]), 1, new_x=XPos.RIGHT, new_y=YPos.TOP, align="C")
                pdf.cell(25, 7, str(gap), 1, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")

        pdf.ln(8)

        # 3. Temuan & Rekomendasi
        pdf.set_font("Helvetica", "B", 13)
        pdf.set_text_color(30, 144, 255)
        pdf.cell(epw, 9, "3. Temuan Audit & Rekomendasi", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="L")

        findings = self.db.get_findings(project_id)
        if not findings:
            pdf.set_font("Helvetica", "I", 10)
            pdf.set_text_color(100, 100, 100)
            pdf.cell(epw, 8, "Tidak ada temuan signifikan yang dicatat.", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="L")
        else:
            for idx, f in enumerate(findings, 1):
                pdf.set_font("Helvetica", "B", 10)
                pdf.set_text_color(40, 40, 40)
                pdf.cell(epw, 6, f"Temuan {idx} - Proses {f['process_code']} (Prioritas {f['priority']})", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="L")

                pdf.set_font("Helvetica", "", 9)
                pdf.set_text_color(60, 60, 60)
                pdf.multi_cell(epw, 5, f"Kondisi: {f['condition_text']}")
                pdf.multi_cell(epw, 5, f"Kriteria: {f['criteria_text']}")
                pdf.multi_cell(epw, 5, f"Rekomendasi: {f['recommendation']}")
                pdf.ln(3)

        # 4. Kesimpulan
        pdf.ln(4)
        pdf.set_font("Helvetica", "B", 13)
        pdf.set_text_color(30, 144, 255)
        pdf.cell(epw, 9, "4. Kesimpulan", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="L")
        
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(50, 50, 50)
        conclusion = proj.conclusion_text or "Secara umum, penerapan tata kelola IT telah berjalan namun memerlukan penguatan pada proses-proses yang masih memiliki gap tingkat kapabilitas."
        pdf.multi_cell(epw, 6, conclusion)

        pdf.output(output_path)
