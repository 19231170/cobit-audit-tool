from typing import Dict, Tuple, List

PROCESS_ATTRIBUTES = {
    1: [("PA1.1", "Process Performance")],
    2: [("PA2.1", "Performance Management"), ("PA2.2", "Work Product Management")],
    3: [("PA3.1", "Process Definition"), ("PA3.2", "Process Deployment")],
    4: [("PA4.1", "Quantitative Analysis"), ("PA4.2", "Quantitative Control")],
    5: [("PA5.1", "Process Innovation"), ("PA5.2", "Process Optimization")],
}

# ISO/IEC 15504 Ratings:
# N: Not achieved (0-15%)
# P: Partially achieved (15-50%)
# L: Largely achieved (50-85%)
# F: Fully achieved (85-100%)
PASSED_RATINGS = {"L", "F"}

class ISO15504Engine:
    @staticmethod
    def is_level_passed(level: int, ratings: Dict[str, str]) -> bool:
        pas = PROCESS_ATTRIBUTES.get(level, [])
        if not pas:
            return False
        for code, _ in pas:
            r = ratings.get(code)
            if not r or r.upper() not in PASSED_RATINGS:
                return False
        return True

    def calculate_capability_level(self, ratings: Dict[str, str]) -> int:
        achieved = 0
        for lvl in range(1, 6):
            if self.is_level_passed(lvl, ratings):
                achieved = lvl
            else:
                break
        return achieved

    def is_level_unlocked(self, target_level: int, ratings: Dict[str, str]) -> bool:
        if target_level <= 1:
            return True
        for prev_lvl in range(1, target_level):
            if not self.is_level_passed(prev_lvl, ratings):
                return False
        return True

    @staticmethod
    def calculate_gap(actual: int, target: int) -> Tuple[int, str]:
        diff = actual - target
        if diff >= 0:
            return (diff, "tercapai")
        elif diff == -1:
            return (diff, "gap_kecil")
        else:
            return (diff, "gap_besar")
