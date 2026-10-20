import sqlite3
from typing import List, Dict, Any, Optional
from app.core.models import Project, Process, Assessment, Finding

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    cobit_version TEXT NOT NULL,
    description TEXT,
    start_date TEXT NOT NULL,
    status TEXT DEFAULT 'active',
    intro_text TEXT DEFAULT '',
    conclusion_text TEXT DEFAULT '',
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS enterprise_goals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cobit_version TEXT NOT NULL,
    goal_code TEXT NOT NULL,
    description TEXT NOT NULL,
    category TEXT DEFAULT ''
);

CREATE TABLE IF NOT EXISTS alignment_goals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cobit_version TEXT NOT NULL,
    goal_code TEXT NOT NULL,
    description TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS goal_mapping (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    enterprise_goal_id INTEGER NOT NULL,
    alignment_goal_id INTEGER NOT NULL,
    relationship TEXT DEFAULT 'P',
    FOREIGN KEY (enterprise_goal_id) REFERENCES enterprise_goals(id),
    FOREIGN KEY (alignment_goal_id) REFERENCES alignment_goals(id)
);

CREATE TABLE IF NOT EXISTS processes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cobit_version TEXT NOT NULL,
    domain TEXT NOT NULL,
    process_code TEXT NOT NULL,
    name TEXT NOT NULL,
    description TEXT DEFAULT ''
);

CREATE TABLE IF NOT EXISTS goal_process_mapping (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    alignment_goal_id INTEGER NOT NULL,
    process_id INTEGER NOT NULL,
    relationship TEXT DEFAULT 'P',
    FOREIGN KEY (alignment_goal_id) REFERENCES alignment_goals(id),
    FOREIGN KEY (process_id) REFERENCES processes(id)
);

CREATE TABLE IF NOT EXISTS raci_entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    process_id INTEGER NOT NULL,
    role_name TEXT NOT NULL,
    raci_type TEXT NOT NULL,
    FOREIGN KEY (process_id) REFERENCES processes(id)
);

CREATE TABLE IF NOT EXISTS role_mapping (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    cobit_role TEXT NOT NULL,
    org_position TEXT NOT NULL,
    FOREIGN KEY (project_id) REFERENCES projects(id)
);

CREATE TABLE IF NOT EXISTS project_processes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    process_id INTEGER NOT NULL,
    target_level INTEGER DEFAULT 3,
    FOREIGN KEY (project_id) REFERENCES projects(id),
    FOREIGN KEY (process_id) REFERENCES processes(id)
);

CREATE TABLE IF NOT EXISTS project_goals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    enterprise_goal_id INTEGER NOT NULL,
    FOREIGN KEY (project_id) REFERENCES projects(id),
    FOREIGN KEY (enterprise_goal_id) REFERENCES enterprise_goals(id)
);

CREATE TABLE IF NOT EXISTS assessments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    process_id INTEGER NOT NULL,
    capability_level INTEGER NOT NULL,
    attribute_code TEXT NOT NULL,
    attribute_name TEXT NOT NULL,
    rating TEXT,
    evidence TEXT DEFAULT '',
    notes TEXT DEFAULT '',
    assessed_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects(id),
    FOREIGN KEY (process_id) REFERENCES processes(id)
);

CREATE TABLE IF NOT EXISTS findings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    process_id INTEGER NOT NULL,
    condition_text TEXT NOT NULL,
    criteria_text TEXT NOT NULL,
    cause_text TEXT DEFAULT '',
    impact_level TEXT DEFAULT 'medium',
    priority INTEGER DEFAULT 2,
    recommendation TEXT NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects(id),
    FOREIGN KEY (process_id) REFERENCES processes(id)
);
"""

class DatabaseManager:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def initialize(self):
        with self.get_connection() as conn:
            conn.executescript(SCHEMA_SQL)

    def create_project(self, name: str, cobit_version: str, description: str, start_date: str) -> int:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO projects (name, cobit_version, description, start_date)
                   VALUES (?, ?, ?, ?)""",
                (name, cobit_version, description, start_date)
            )
            return cursor.lastrowid

    def get_projects(self) -> List[Project]:
        with self.get_connection() as conn:
            rows = conn.execute("SELECT * FROM projects ORDER BY created_at DESC").fetchall()
            return [Project(**dict(r)) for r in rows]

    def get_project_by_id(self, project_id: int) -> Optional[Project]:
        with self.get_connection() as conn:
            row = conn.execute("SELECT * FROM projects WHERE id = ?", (project_id,)).fetchone()
            return Project(**dict(row)) if row else None

    def insert_process(self, cobit_version: str, domain: str, process_code: str, name: str, description: str = "") -> int:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO processes (cobit_version, domain, process_code, name, description)
                   VALUES (?, ?, ?, ?, ?)""",
                (cobit_version, domain, process_code, name, description)
            )
            return cursor.lastrowid

    def add_project_process(self, project_id: int, process_id: int, target_level: int = 3):
        with self.get_connection() as conn:
            conn.execute(
                """INSERT INTO project_processes (project_id, process_id, target_level)
                   VALUES (?, ?, ?)""",
                (project_id, process_id, target_level)
            )

    def get_project_processes(self, project_id: int) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            rows = conn.execute(
                """SELECT pp.id as mapping_id, pp.project_id, pp.process_id, pp.target_level,
                          p.domain, p.process_code, p.name, p.description
                   FROM project_processes pp
                   JOIN processes p ON pp.process_id = p.id
                   WHERE pp.project_id = ?
                   ORDER BY p.process_code""",
                (project_id,)
            ).fetchall()
            return [dict(r) for r in rows]

    def save_assessment(self, project_id: int, process_id: int, capability_level: int,
                        attribute_code: str, attribute_name: str, rating: Optional[str],
                        evidence: str = "", notes: str = ""):
        with self.get_connection() as conn:
            existing = conn.execute(
                """SELECT id FROM assessments 
                   WHERE project_id = ? AND process_id = ? AND attribute_code = ?""",
                (project_id, process_id, attribute_code)
            ).fetchone()
            if existing:
                conn.execute(
                    """UPDATE assessments 
                       SET capability_level = ?, attribute_name = ?, rating = ?, evidence = ?, notes = ?, assessed_at = CURRENT_TIMESTAMP
                       WHERE id = ?""",
                    (capability_level, attribute_name, rating, evidence, notes, existing["id"])
                )
            else:
                conn.execute(
                    """INSERT INTO assessments 
                       (project_id, process_id, capability_level, attribute_code, attribute_name, rating, evidence, notes)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    (project_id, process_id, capability_level, attribute_code, attribute_name, rating, evidence, notes)
                )

    def get_assessments(self, project_id: int, process_id: int) -> List[Assessment]:
        with self.get_connection() as conn:
            rows = conn.execute(
                """SELECT * FROM assessments 
                   WHERE project_id = ? AND process_id = ? 
                   ORDER BY capability_level, attribute_code""",
                (project_id, process_id)
            ).fetchall()
            return [Assessment(**dict(r)) for r in rows]

    def add_finding(self, project_id: int, process_id: int, condition_text: str,
                    criteria_text: str, cause_text: str, impact_level: str,
                    priority: int, recommendation: str) -> int:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO findings (project_id, process_id, condition_text, criteria_text, cause_text, impact_level, priority, recommendation)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (project_id, process_id, condition_text, criteria_text, cause_text, impact_level, priority, recommendation)
            )
            return cursor.lastrowid

    def get_findings(self, project_id: int, process_id: Optional[int] = None) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            query = """SELECT f.*, p.process_code, p.name as process_name, p.domain
                       FROM findings f
                       JOIN processes p ON f.process_id = p.id
                       WHERE f.project_id = ?"""
            params = [project_id]
            if process_id:
                query += " AND f.process_id = ?"
                params.append(process_id)
            query += " ORDER BY f.priority ASC, f.created_at DESC"
            rows = conn.execute(query, params).fetchall()
            return [dict(r) for r in rows]
