import os
import pytest
from app.core.database import DatabaseManager
from app.core.models import Project, Process, Assessment, Finding

@pytest.fixture
def db(tmp_path):
    db_file = tmp_path / "test_cobit.db"
    manager = DatabaseManager(str(db_file))
    manager.initialize()
    return manager

def test_initialize_and_create_project(db):
    project_id = db.create_project(
        name="PT Bank Sejahtera",
        cobit_version="COBIT2019",
        description="Audit IT Tahunan 2026",
        start_date="2026-10-20"
    )
    assert project_id > 0
    projects = db.get_projects()
    assert len(projects) == 1
    assert projects[0].name == "PT Bank Sejahtera"
    assert projects[0].cobit_version == "COBIT2019"

def test_crud_processes_and_assessments(db):
    proj_id = db.create_project(name="Org A", cobit_version="COBIT5", description="", start_date="2026-10-20")
    proc_id = db.insert_process(cobit_version="COBIT5", domain="APO", process_code="APO12", name="Managed Risk", description="Risk management")
    assert proc_id > 0

    db.add_project_process(project_id=proj_id, process_id=proc_id, target_level=3)
    p_procs = db.get_project_processes(proj_id)
    assert len(p_procs) == 1
    assert p_procs[0]["process_code"] == "APO12"
    assert p_procs[0]["target_level"] == 3

    # Add assessment
    db.save_assessment(
        project_id=proj_id,
        process_id=proc_id,
        capability_level=1,
        attribute_code="PA1.1",
        attribute_name="Process Performance",
        rating="F",
        evidence="SOP Risk rev 2",
        notes="Lengkap"
    )
    assessments = db.get_assessments(project_id=proj_id, process_id=proc_id)
    assert len(assessments) == 1
    assert assessments[0].rating == "F"
