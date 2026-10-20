from app.core.database import DatabaseManager

COBIT5_PROCESSES = [
    # EDM (5)
    ("EDM", "EDM01", "Ensure Governance Framework Setting and Maintenance"),
    ("EDM", "EDM02", "Ensure Benefits Delivery"),
    ("EDM", "EDM03", "Ensure Risk Optimisation"),
    ("EDM", "EDM04", "Ensure Resource Optimisation"),
    ("EDM", "EDM05", "Ensure Stakeholder Transparency"),
    # APO (13)
    ("APO", "APO01", "Manage the IT Management Framework"),
    ("APO", "APO02", "Manage Strategy"),
    ("APO", "APO03", "Manage Enterprise Architecture"),
    ("APO", "APO04", "Manage Innovation"),
    ("APO", "APO05", "Manage Portfolio"),
    ("APO", "APO06", "Manage Budget and Costs"),
    ("APO", "APO07", "Manage Human Resources"),
    ("APO", "APO08", "Manage Relationships"),
    ("APO", "APO09", "Manage Service Agreements"),
    ("APO", "APO10", "Manage Suppliers"),
    ("APO", "APO11", "Manage Quality"),
    ("APO", "APO12", "Manage Risk"),
    ("APO", "APO13", "Manage Security"),
    # BAI (10)
    ("BAI", "BAI01", "Manage Programmes and Projects"),
    ("BAI", "BAI02", "Manage Requirements Definition"),
    ("BAI", "BAI03", "Manage Solutions Identification and Build"),
    ("BAI", "BAI04", "Manage Availability and Capacity"),
    ("BAI", "BAI05", "Manage Organisational Change Enablement"),
    ("BAI", "BAI06", "Manage Changes"),
    ("BAI", "BAI07", "Manage Change Acceptance and Transitioning"),
    ("BAI", "BAI08", "Manage Knowledge"),
    ("BAI", "BAI09", "Manage Assets"),
    ("BAI", "BAI10", "Manage Configuration"),
    # DSS (6)
    ("DSS", "DSS01", "Manage Operations"),
    ("DSS", "DSS02", "Manage Service Requests and Incidents"),
    ("DSS", "DSS03", "Manage Problems"),
    ("DSS", "DSS04", "Manage Continuity"),
    ("DSS", "DSS05", "Manage Security Services"),
    ("DSS", "DSS06", "Manage Business Process Controls"),
    # MEA (3)
    ("MEA", "MEA01", "Monitor, Evaluate and Assess Performance and Conformance"),
    ("MEA", "MEA02", "Monitor, Evaluate and Assess the System of Internal Control"),
    ("MEA", "MEA03", "Monitor, Evaluate and Assess Compliance with External Requirements"),
]

COBIT2019_PROCESSES = [
    # EDM (5)
    ("EDM", "EDM01", "Ensured Governance Framework Setting and Maintenance"),
    ("EDM", "EDM02", "Ensured Benefits Delivery"),
    ("EDM", "EDM03", "Ensured Risk Optimization"),
    ("EDM", "EDM04", "Ensured Resource Optimization"),
    ("EDM", "EDM05", "Ensured Stakeholder Engagement"),
    # APO (14)
    ("APO", "APO01", "Managed I&T Management Framework"),
    ("APO", "APO02", "Managed Strategy"),
    ("APO", "APO03", "Managed Enterprise Architecture"),
    ("APO", "APO04", "Managed Innovation"),
    ("APO", "APO05", "Managed Portfolio"),
    ("APO", "APO06", "Managed Budget and Costs"),
    ("APO", "APO07", "Managed Human Resources"),
    ("APO", "APO08", "Managed Relationships"),
    ("APO", "APO09", "Managed Service Agreements"),
    ("APO", "APO10", "Managed Vendors"),
    ("APO", "APO11", "Managed Quality"),
    ("APO", "APO12", "Managed Risk"),
    ("APO", "APO13", "Managed Security"),
    ("APO", "APO14", "Managed Data"),
    # BAI (11)
    ("BAI", "BAI01", "Managed Programs"),
    ("BAI", "BAI02", "Managed Requirements Definition"),
    ("BAI", "BAI03", "Managed Solutions Identification and Build"),
    ("BAI", "BAI04", "Managed Availability and Capacity"),
    ("BAI", "BAI05", "Managed Organizational Change"),
    ("BAI", "BAI06", "Managed IT Changes"),
    ("BAI", "BAI07", "Managed IT Change Acceptance and Transitioning"),
    ("BAI", "BAI08", "Managed Knowledge"),
    ("BAI", "BAI09", "Managed Assets"),
    ("BAI", "BAI10", "Managed Configuration"),
    ("BAI", "BAI11", "Managed Projects"),
    # DSS (6)
    ("DSS", "DSS01", "Managed Operations"),
    ("DSS", "DSS02", "Managed Service Requests and Incidents"),
    ("DSS", "DSS03", "Managed Problems"),
    ("DSS", "DSS04", "Managed Continuity"),
    ("DSS", "DSS05", "Managed Security Services"),
    ("DSS", "DSS06", "Managed Business Process Controls"),
    # MEA (4)
    ("MEA", "MEA01", "Managed Performance and Conformance Monitoring"),
    ("MEA", "MEA02", "Managed System of Internal Control"),
    ("MEA", "MEA03", "Managed Compliance with External Requirements"),
    ("MEA", "MEA04", "Managed Assurance"),
]

DEFAULT_ENTERPRISE_GOALS = [
    ("COBIT5", "EG01", "Stakeholder value of business investments", "Financial"),
    ("COBIT5", "EG02", "Portfolio of competitive products and services", "Financial"),
    ("COBIT5", "EG03", "Managed business risk (safeguarding of assets)", "Financial"),
    ("COBIT5", "EG04", "Compliance with external laws and regulations", "Financial"),
    ("COBIT5", "EG05", "Financial transparency", "Financial"),
    ("COBIT5", "EG06", "Customer-oriented service culture", "Customer"),
    ("COBIT5", "EG07", "Business service continuity and availability", "Customer"),
    ("COBIT2019", "EG01", "Portfolio of competitive products and services", "Financial"),
    ("COBIT2019", "EG02", "Managed business risk", "Financial"),
    ("COBIT2019", "EG03", "Compliance with external laws and regulations", "Financial"),
    ("COBIT2019", "EG04", "Quality of financial information", "Financial"),
    ("COBIT2019", "EG05", "Customer-oriented service culture", "Customer"),
    ("COBIT2019", "EG06", "Business service continuity and availability", "Customer"),
    ("COBIT2019", "EG07", "Quality of management information", "Internal"),
    ("COBIT2019", "EG08", "Optimization of internal business process functionality", "Internal"),
    ("COBIT2019", "EG09", "Optimization of business process costs", "Internal"),
    ("COBIT2019", "EG10", "Staff skills, motivation and productivity", "Learning"),
]

DEFAULT_ALIGNMENT_GOALS = [
    ("COBIT5", "AG01", "Alignment of IT and business strategy"),
    ("COBIT5", "AG02", "IT compliance and support for business compliance"),
    ("COBIT5", "AG03", "Commitment of executive management for making IT decisions"),
    ("COBIT5", "AG04", "Managed IT-related business risk"),
    ("COBIT5", "AG05", "Realised benefits from IT-enabled investments"),
    ("COBIT5", "AG06", "Transparency of IT costs, benefits and risk"),
    ("COBIT2019", "AG01", "I&T compliance and support for business compliance"),
    ("COBIT2019", "AG02", "Managed I&T-related risk"),
    ("COBIT2019", "AG03", "Realized benefits from I&T-enabled investments and services"),
    ("COBIT2019", "AG04", "Quality of technology-related financial information"),
    ("COBIT2019", "AG05", "Delivery of I&T services in line with business requirements"),
    ("COBIT2019", "AG06", "Agility to turn business requirements into operational solutions"),
    ("COBIT2019", "AG07", "Security of information, processing infrastructure and applications"),
]

def seed_default_cobit_data(db: DatabaseManager):
    with db.get_connection() as conn:
        # Insert Processes
        for domain, code, name in COBIT5_PROCESSES:
            conn.execute(
                "INSERT OR IGNORE INTO processes (cobit_version, domain, process_code, name) VALUES ('COBIT5', ?, ?, ?)",
                (domain, code, name)
            )
        for domain, code, name in COBIT2019_PROCESSES:
            conn.execute(
                "INSERT OR IGNORE INTO processes (cobit_version, domain, process_code, name) VALUES ('COBIT2019', ?, ?, ?)",
                (domain, code, name)
            )
        # Insert Goals
        for ver, code, desc, cat in DEFAULT_ENTERPRISE_GOALS:
            conn.execute(
                "INSERT OR IGNORE INTO enterprise_goals (cobit_version, goal_code, description, category) VALUES (?, ?, ?, ?)",
                (ver, code, desc, cat)
            )
        for ver, code, desc in DEFAULT_ALIGNMENT_GOALS:
            conn.execute(
                "INSERT OR IGNORE INTO alignment_goals (cobit_version, goal_code, description) VALUES (?, ?, ?)",
                (ver, code, desc)
            )

        # Basic Goal Mapping
        eg_rows = conn.execute("SELECT id, cobit_version, goal_code FROM enterprise_goals").fetchall()
        ag_rows = conn.execute("SELECT id, cobit_version, goal_code FROM alignment_goals").fetchall()
        p_rows = conn.execute("SELECT id, cobit_version, process_code FROM processes").fetchall()

        for eg in eg_rows:
            matching_ags = [ag for ag in ag_rows if ag["cobit_version"] == eg["cobit_version"]]
            if matching_ags:
                conn.execute(
                    "INSERT OR IGNORE INTO goal_mapping (enterprise_goal_id, alignment_goal_id, relationship) VALUES (?, ?, 'P')",
                    (eg["id"], matching_ags[0]["id"])
                )

        for ag in ag_rows:
            matching_ps = [p for p in p_rows if p["cobit_version"] == ag["cobit_version"]]
            for p in matching_ps[:3]:
                conn.execute(
                    "INSERT OR IGNORE INTO goal_process_mapping (alignment_goal_id, process_id, relationship) VALUES (?, ?, 'P')",
                    (ag["id"], p["id"])
                )

        # RACI entries sample
        roles = ["Board", "CEO", "CIO", "CISO", "Head of IT Ops", "Head of Dev", "Auditor"]
        for p in p_rows:
            conn.execute(
                "INSERT OR IGNORE INTO raci_entries (process_id, role_name, raci_type) VALUES (?, 'Board', 'A')",
                (p["id"],)
            )
            conn.execute(
                "INSERT OR IGNORE INTO raci_entries (process_id, role_name, raci_type) VALUES (?, 'CIO', 'R')",
                (p["id"],)
            )
            conn.execute(
                "INSERT OR IGNORE INTO raci_entries (process_id, role_name, raci_type) VALUES (?, 'CISO', 'C')",
                (p["id"],)
            )
            conn.execute(
                "INSERT OR IGNORE INTO raci_entries (process_id, role_name, raci_type) VALUES (?, 'Auditor', 'I')",
                (p["id"],)
            )
