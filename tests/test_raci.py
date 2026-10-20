import pytest
from app.core.database import DatabaseManager
from app.core.seeds import seed_default_cobit_data

@pytest.fixture
def db(tmp_path):
    mgr = DatabaseManager(str(tmp_path / "test_raci.db"))
    mgr.initialize()
    seed_default_cobit_data(mgr)
    return mgr

def test_raci_role_mapping(db):
    proj_id = db.create_project("PT RACI", "COBIT5", "Audit", "2026-10-20")
    with db.get_connection() as conn:
        conn.execute(
            "INSERT INTO role_mapping (project_id, cobit_role, org_position) VALUES (?, 'Board', 'Komisaris Utama')",
            (proj_id,)
        )
        row = conn.execute("SELECT org_position FROM role_mapping WHERE project_id = ? AND cobit_role = 'Board'", (proj_id,)).fetchone()
        assert row["org_position"] == "Komisaris Utama"
