import pytest
from app.core.database import DatabaseManager
from app.core.importer import ExcelImporter
from app.core.seeds import seed_default_cobit_data

@pytest.fixture
def db(tmp_path):
    manager = DatabaseManager(str(tmp_path / "test_import.db"))
    manager.initialize()
    return manager

def test_seed_default_cobit_data(db):
    seed_default_cobit_data(db)
    with db.get_connection() as conn:
        c5_count = conn.execute("SELECT COUNT(*) as c FROM processes WHERE cobit_version = 'COBIT5'").fetchone()["c"]
        c2019_count = conn.execute("SELECT COUNT(*) as c FROM processes WHERE cobit_version = 'COBIT2019'").fetchone()["c"]
        eg_count = conn.execute("SELECT COUNT(*) as c FROM enterprise_goals").fetchone()["c"]
        ag_count = conn.execute("SELECT COUNT(*) as c FROM alignment_goals").fetchone()["c"]
        raci_count = conn.execute("SELECT COUNT(*) as c FROM raci_entries").fetchone()["c"]
    
    assert c5_count == 37
    assert c2019_count == 40
    assert eg_count >= 17
    assert ag_count >= 13
    assert raci_count > 0

def test_excel_importer_custom_processes(db, tmp_path):
    import openpyxl
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Processes"
    ws.append(["domain", "process_code", "name", "description"])
    ws.append(["EDM", "EDM01", "Ensured Governance Framework", "Setting governance"])
    ws.append(["APO", "APO01", "Managed I&T Framework", "Managing framework"])
    file_path = str(tmp_path / "custom_processes.xlsx")
    wb.save(file_path)

    importer = ExcelImporter(db)
    imported = importer.import_processes_excel(file_path, cobit_version="COBIT5")
    assert imported == 2
