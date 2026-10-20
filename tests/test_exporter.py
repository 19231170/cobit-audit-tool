import os
import pytest
from app.core.database import DatabaseManager
from app.core.seeds import seed_default_cobit_data
from app.core.exporter import PDFReportGenerator

@pytest.fixture
def db(tmp_path):
    mgr = DatabaseManager(str(tmp_path / "test_pdf.db"))
    mgr.initialize()
    seed_default_cobit_data(mgr)
    return mgr

def test_generate_pdf_report(db, tmp_path):
    proj_id = db.create_project("PT Sejahtera Mandiri", "COBIT2019", "Audit Sistem Informasi 2026", "2026-10-20")
    
    # Add processes
    with db.get_connection() as conn:
        p_row = conn.execute("SELECT id FROM processes WHERE process_code = 'EDM01'").fetchone()
        db.add_project_process(proj_id, p_row["id"], target_level=3)
        db.save_assessment(proj_id, p_row["id"], 1, "PA1.1", "Process Performance", "F", evidence="Ada SOP")

    db.add_finding(proj_id, p_row["id"], "Kondisi temuan", "Standar EDM", "Penyebab", "high", 1, "Rekomendasi tindakan")

    output_pdf = str(tmp_path / "laporan_audit.pdf")
    gen = PDFReportGenerator(db)
    gen.generate_audit_report(proj_id, output_pdf)

    assert os.path.exists(output_pdf)
    assert os.path.getsize(output_pdf) > 2000
