import pytest
from myhashmap.myhashmap import MyHashMap, InvalidConditionError

def test_iloc():
    map = MyHashMap()
    map["value1"] = 1
    map["value2"] = 2
    map["value3"] = 3
    map["1"] = 10
    map["2"] = 20
    map["3"] = 30
    map["1, 5"] = 100
    map["5, 5"] = 200
    map["10, 5"] = 300

    assert map.iloc[0] == 10
    assert map.iloc[2] == 300
    assert map.iloc[5] == 200
    assert map.iloc[8] == 3
    with pytest.raises(TypeError):
        _ = map.iloc["not an int"]
    with pytest.raises(IndexError):
        _ = map.iloc[100]

def test_ploc_single_condition():
    map = MyHashMap()
    map["1"] = 10
    map["2"] = 20
    map["3"] = 30
    map["4"] = 40

    assert map.ploc[">=1"] == {"1": 10, "2": 20, "3": 30, "4": 40}
    assert map.ploc["<3"] == {"1": 10, "2": 20}

def test_ploc_multiple_conditions():
    map = MyHashMap()
    map["1, 5"] = 100
    map["5, 5"] = 200
    map["10, 5"] = 300
    map["1, 5, 3"] = 400
    map["5, 5, 4"] = 500
    map["10, 5, 5"] = 600

    assert map.ploc[">0, >0"] == {"1, 5": 100, "5, 5": 200, "10, 5": 300}
    assert map.ploc[">=10, >0"] == {"10, 5": 300}
    assert map.ploc["<5, >=5, >=3"] == {"1, 5, 3": 400}

def test_invalid_condition():
    map = MyHashMap()
    map["1"] = 10
    map["2"] = 20
    with pytest.raises(InvalidConditionError):
        map.ploc["invalid"]
    with pytest.raises(InvalidConditionError):
        map.ploc["="]
    with pytest.raises(InvalidConditionError):
        map.ploc[">not_a_number"]

def test_non_matching_key():
        map = MyHashMap()
        map["text"] = 1
        map["another_key"] = 2
        assert map.ploc[">0"] == {}

def test_key_part_not_int_or_float():
    map = MyHashMap()
    map["text"] = 1
    map["another_key"] = 2
    map["1, text"] = 100
    assert map.ploc[">0, >0"] == {}

def test_all_operators():
    map = MyHashMap()
    map["1"] = 10
    map["2"] = 20
    map["3"] = 30

    assert map.ploc[">1"] == {"2": 20, "3": 30}
    assert map.ploc[">=2"] == {"2": 20, "3": 30}
    assert map.ploc["<3"] == {"1": 10, "2": 20}
    assert map.ploc["<=2"] == {"1": 10, "2": 20}
    assert map.ploc["=2"] == {"2": 20}
    assert map.ploc["<>2"] == {"1": 10, "3": 30}

def test_key_parts_and_conditions_length_mismatch():
    map = MyHashMap()
    map["1, 2"] = 10
    assert map.ploc[">1"] == {}
