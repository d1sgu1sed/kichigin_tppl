from typing import Any, Dict, List
import re

class InvalidConditionError(Exception):
    pass

class MyHashMap(dict):
    def __init__(self):
        super().__init__()

    @property
    def iloc(self):
        class ILocAccessor:
            def __init__(self, parent):
                self.parent = parent

            def __getitem__(self, index):
                if not isinstance(index, int):
                    raise TypeError("Index must be an integer.")
                sorted_keys = sorted(self.parent.toSortedSet())
                if index < 0 or index >= len(sorted_keys):
                    raise IndexError("Index out of range.")
                return self.parent[sorted_keys[index]]

        return ILocAccessor(self)

    @property
    def ploc(self):
        class PLocAccessor:
            def __init__(self, parent):
                self.parent = parent

            def __getitem__(self, condition):
                return self.parent._evaluate_condition(condition)

        return PLocAccessor(self)

    def toSortedSet(self):
        return list(self.keys())

    def _evaluate_condition(self, condition: str) -> Dict[Any, Any]:
        def parse_condition(cond):
            pattern = r"([<>]=?|=|<>)\s*(-?\d+(?:\.\d+)?)"
            matches = re.findall(pattern, cond)
            if not matches:
                raise InvalidConditionError(f"Invalid condition: {cond}")
            return [(op, float(value) if '.' in value else int(value)) for op, value in matches]

        def match_conditions(key_parts, conditions):
            if len(key_parts) != len(conditions):
                return False

            for key_part, (op, value) in zip(key_parts, conditions):
                if not isinstance(key_part, (int, float)):
                    return False
                if op == "<" and not key_part < value:
                    return False
                elif op == "<=" and not key_part <= value:
                    return False
                elif op == ">" and not key_part > value:
                    return False
                elif op == ">=" and not key_part >= value:
                    return False
                elif op == "=" and not key_part == value:
                    return False
                elif op == "<>" and not key_part != value:
                    return False

            return True

        result = {}
        for key, value in self.items():
            try:
                key_parts = [float(part) if '.' in part else int(part) for part in re.findall(r"-?\d+(?:\.\d+)?", str(key))]
                conditions = parse_condition(condition)
                if match_conditions(key_parts, conditions):
                    result[key] = value
            except ValueError:
                continue

        return result
