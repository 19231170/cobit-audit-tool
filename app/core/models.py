from dataclasses import dataclass
from typing import Optional

@dataclass
class Project:
    id: int
    name: str
    cobit_version: str
    description: str
    start_date: str
    status: str = "active"
    intro_text: str = ""
    conclusion_text: str = ""
    created_at: str = ""
    updated_at: str = ""

@dataclass
class EnterpriseGoal:
    id: int
    cobit_version: str
    goal_code: str
    description: str
    category: str = ""

@dataclass
class AlignmentGoal:
    id: int
    cobit_version: str
    goal_code: str
    description: str

@dataclass
class Process:
    id: int
    cobit_version: str
    domain: str
    process_code: str
    name: str
    description: str = ""

@dataclass
class Assessment:
    id: int
    project_id: int
    process_id: int
    capability_level: int
    attribute_code: str
    attribute_name: str
    rating: Optional[str] = None
    evidence: str = ""
    notes: str = ""
    assessed_at: str = ""

@dataclass
class Finding:
    id: int
    project_id: int
    process_id: int
    condition_text: str
    criteria_text: str
    cause_text: str
    impact_level: str
    priority: int
    recommendation: str
    created_at: str = ""
