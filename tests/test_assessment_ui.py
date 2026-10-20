import pytest
from app.core.database import DatabaseManager
from app.core.assessment_engine import ISO15504Engine

@pytest.fixture
def db(tmp_path):
    mgr = DatabaseManager(str(tmp_path / "test_ass_ui.db"))
    mgr.initialize()
    return mgr

def test_assessment_flow_persistence(db):
    proj_id = db.create_project("PT Assessment", "COBIT2019", "", "2026-10-20")
    proc_id = db.insert_process("COBIT2019", "APO", "APO12", "Managed Risk")
    db.add_project_process(proj_id, proc_id, target_level=3)

    # Save level 1 PA 1.1 = F
    db.save_assessment(proj_id, proc_id, 1, "PA1.1", "Process Performance", "F", evidence="SOP Doc")
    
    # Save level 2 PA 2.1 = L, PA 2.2 = F
    db.save_assessment(proj_id, proc_id, 2, "PA2.1", "Performance Management", "L", evidence="Review quarterly")
    db.save_assessment(proj_id, proc_id, 2, "PA2.2", "Work Product Management", "F", evidence="Work products valid")

    assessments = db.get_assessments(proj_id, proc_id)
    ratings = {a.attribute_code: a.rating for a in assessments}
    
    engine = ISO15504Engine()
    assert engine.calculate_capability_level(ratings) == 2
