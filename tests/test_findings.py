import pytest
from app.core.database import DatabaseManager

@pytest.fixture
def db(tmp_path):
    mgr = DatabaseManager(str(tmp_path / "test_findings.db"))
    mgr.initialize()
    return mgr

def test_findings_crud(db):
    proj_id = db.create_project("PT Findings", "COBIT2019", "", "2026-10-20")
    proc_id = db.insert_process("COBIT2019", "APO", "APO12", "Managed Risk")
    
    fid = db.add_finding(
        project_id=proj_id,
        process_id=proc_id,
        condition_text="Kebijakan risiko belum ditinjau berkala",
        criteria_text="COBIT APO12.01 mewajibkan review risiko berkala",
        cause_text="Keterbatasan staf",
        impact_level="high",
        priority=1,
        recommendation="Bentuk komite risiko dan jadwalkan review tiap 6 bulan"
    )
    assert fid > 0
    all_f = db.get_findings(proj_id)
    assert len(all_f) == 1
    assert all_f[0]["priority"] == 1
    assert all_f[0]["process_code"] == "APO12"
