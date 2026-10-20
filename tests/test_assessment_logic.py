import pytest
from app.core.assessment_engine import ISO15504Engine, PROCESS_ATTRIBUTES

def test_process_attributes_structure():
    assert len(PROCESS_ATTRIBUTES[1]) == 1  # PA 1.1
    assert len(PROCESS_ATTRIBUTES[2]) == 2  # PA 2.1, PA 2.2
    assert len(PROCESS_ATTRIBUTES[3]) == 2  # PA 3.1, PA 3.2
    assert len(PROCESS_ATTRIBUTES[4]) == 2  # PA 4.1, PA 4.2
    assert len(PROCESS_ATTRIBUTES[5]) == 2  # PA 5.1, PA 5.2

def test_level_calculation_strict_hierarchy():
    engine = ISO15504Engine()
    
    # Incomplete (No ratings or Level 1 failed)
    assert engine.calculate_capability_level({}) == 0
    assert engine.calculate_capability_level({"PA1.1": "P"}) == 0
    assert engine.calculate_capability_level({"PA1.1": "N"}) == 0

    # Level 1 achieved (PA 1.1 is L or F)
    assert engine.calculate_capability_level({"PA1.1": "L"}) == 1
    assert engine.calculate_capability_level({"PA1.1": "F"}) == 1

    # Level 2 partially passed (PA 2.1 is F, but PA 2.2 is P) -> Still Level 1
    ratings = {"PA1.1": "F", "PA2.1": "F", "PA2.2": "P"}
    assert engine.calculate_capability_level(ratings) == 1

    # Level 2 fully achieved
    ratings = {"PA1.1": "F", "PA2.1": "L", "PA2.2": "F"}
    assert engine.calculate_capability_level(ratings) == 2

    # Level 3 achieved
    ratings = {"PA1.1": "F", "PA2.1": "F", "PA2.2": "F", "PA3.1": "L", "PA3.2": "L"}
    assert engine.calculate_capability_level(ratings) == 3

def test_level_unlock_logic():
    engine = ISO15504Engine()
    # Level 1 is always unlocked
    assert engine.is_level_unlocked(1, {}) is True
    # Level 2 unlocked only if Level 1 is achieved
    assert engine.is_level_unlocked(2, {"PA1.1": "N"}) is False
    assert engine.is_level_unlocked(2, {"PA1.1": "F"}) is True
    # Level 3 unlocked only if Level 2 is achieved
    assert engine.is_level_unlocked(3, {"PA1.1": "F", "PA2.1": "F", "PA2.2": "P"}) is False
    assert engine.is_level_unlocked(3, {"PA1.1": "F", "PA2.1": "L", "PA2.2": "F"}) is True

def test_gap_calculation():
    engine = ISO15504Engine()
    assert engine.calculate_gap(actual=3, target=3) == (0, "tercapai")
    assert engine.calculate_gap(actual=2, target=3) == (-1, "gap_kecil")
    assert engine.calculate_gap(actual=1, target=3) == (-2, "gap_besar")
    assert engine.calculate_gap(actual=4, target=3) == (1, "tercapai")
