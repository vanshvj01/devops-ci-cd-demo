import pytest
from app import average, grade, remark, result


def test_average():
    assert average([80, 90, 70]) == 80


def test_average_empty():
    with pytest.raises(ValueError):
        average([])


@pytest.mark.parametrize("avg,expected", [(92, "O"), (78, "A"), (65, "B"), (45, "C"), (30, "F")])
def test_grade(avg, expected):
    assert grade(avg) == expected


def test_grade_out_of_range():
    with pytest.raises(ValueError):
        grade(120)


def test_result():
    r = result("Arjun", [40, 50, 60])
    assert r == {"name": "Arjun", "average": 50, "grade": "C", "passed": True, "distinction": False,
                 "remark": "Pass"}


def test_distinction():
    assert result("Vedant", [80, 90, 85])["distinction"] is True


def test_remark():
    assert remark("O") == "Outstanding"
    assert remark("F") == "Needs improvement"
