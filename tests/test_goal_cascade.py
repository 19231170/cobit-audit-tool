import pytest
from app.core.database import DatabaseManager
from app.core.seeds import seed_default_cobit_data

@pytest.fixture
def db(tmp_path):
    mgr = DatabaseManager(str(tmp_path / "test_gc.db"))
    mgr.initialize()
    seed_default_cobit_data(mgr)
    return mgr

def test_goal_cascade_mapping_flow(db):
    proj_id = db.create_project("PT Test", "COBIT2019", "Desc", "2026-10-20")
    with db.get_connection() as conn:
        egs = conn.execute("SELECT id FROM enterprise_goals WHERE cobit_version = 'COBIT2019'").fetchall()
        selected_eg_ids = [egs[0]["id"]]
        
        # Resolve AGs
        ag_ids = [r["alignment_goal_id"] for r in conn.execute(
            f"SELECT DISTINCT alignment_goal_id FROM goal_mapping WHERE enterprise_goal_id IN ({','.join(map(str, selected_eg_ids))})"
        ).fetchall()]
        assert len(ag_ids) > 0

        # Resolve Processes
        p_ids = [r["process_id"] for r in conn.execute(
            f"SELECT DISTINCT process_id FROM goal_process_mapping WHERE alignment_goal_id IN ({','.join(map(str, ag_ids))})"
        ).fetchall()]
        assert len(p_ids) > 0
