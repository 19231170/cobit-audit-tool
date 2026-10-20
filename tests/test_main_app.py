import pytest
from app.core.database import DatabaseManager
from app.core.seeds import seed_default_cobit_data
from app.core.assessment_engine import ISO15504Engine

@pytest.fixture
def db(tmp_path):
    mgr = DatabaseManager(str(tmp_path / "test_main.db"))
    mgr.initialize()
    seed_default_cobit_data(mgr)
    return mgr

def test_project_progress_calculation(db):
    proj_id = db.create_project("PT Progress", "COBIT5", "", "2026-10-20")
    procs = db.get_project_processes(proj_id)
    assert len(procs) == 0

    # Add 2 processes
    with db.get_connection() as conn:
        p1 = conn.execute("SELECT id FROM processes WHERE process_code = 'EDM01'").fetchone()
        p2 = conn.execute("SELECT id FROM processes WHERE process_code = 'EDM02'").fetchone()
        db.add_project_process(proj_id, p1["id"])
        db.add_project_process(proj_id, p2["id"])

    # 0 assessments -> 0%
    procs = db.get_project_processes(proj_id)
    ass_count = 0
    for p in procs:
        if db.get_assessments(proj_id, p["process_id"]):
            ass_count += 1
    progress = ass_count / len(procs)
    assert progress == 0.0

    # 1 assessment done -> 50%
    db.save_assessment(proj_id, p1["id"], 1, "PA1.1", "Process Performance", "F")
    ass_count = sum(1 for p in procs if db.get_assessments(proj_id, p["process_id"]))
    progress = ass_count / len(procs)
    assert progress == 0.5
