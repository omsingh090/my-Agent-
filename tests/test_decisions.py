"""
Tests for the decision engine module.
"""

import pytest

from src.decisions.priority import Decision, PriorityEngine


def test_decision_priority_formula():
    d = Decision(
        title="Test",
        description="desc",
        impact=10,
        effort=0,
        business_value=10,
    )
    score = d.calculate_priority()
    # impact=1.0, effort_inv=1.0, value=1.0 → (1*0.4 + 1*0.3 + 1*0.3)*10 = 10.0
    assert score == pytest.approx(10.0)


def test_low_effort_boosts_priority():
    high_effort = Decision("H", "d", impact=8, effort=9, business_value=7)
    low_effort = Decision("L", "d", impact=8, effort=1, business_value=7)
    assert low_effort.calculate_priority() > high_effort.calculate_priority()


def test_is_high_priority():
    d = Decision("H", "d", impact=9, effort=2, business_value=9)
    assert d.is_high_priority(threshold=7.5)


def test_is_not_high_priority():
    d = Decision("L", "d", impact=3, effort=9, business_value=3)
    assert not d.is_high_priority(threshold=7.5)


def test_to_dict_keys():
    d = Decision("T", "desc", impact=7, effort=4, business_value=6)
    result = d.to_dict()
    assert "priority_score" in result
    assert "do_this_first" in result
    assert "title" in result


def test_rank_decisions_order():
    decisions = [
        Decision("Low", "d", impact=2, effort=8, business_value=2),
        Decision("High", "d", impact=9, effort=1, business_value=9),
        Decision("Mid", "d", impact=5, effort=5, business_value=5),
    ]
    ranked = PriorityEngine.rank_decisions(decisions)
    assert ranked[0]["title"] == "High"
    assert ranked[-1]["title"] == "Low"


def test_generate_decisions_from_trends():
    analysis = {
        "trends": [{"column": "revenue", "direction": "increasing", "magnitude": 20}],
        "correlations": [],
        "anomalies": {},
    }
    decisions = PriorityEngine.generate_decisions(analysis)
    assert len(decisions) >= 1
    assert any("revenue" in d.title.lower() for d in decisions)


def test_generate_decisions_from_correlations():
    analysis = {
        "trends": [],
        "correlations": [
            {
                "column1": "price",
                "column2": "revenue",
                "correlation": 0.85,
                "strength": "strong",
            }
        ],
        "anomalies": {},
    }
    decisions = PriorityEngine.generate_decisions(analysis)
    assert len(decisions) >= 1


def test_generate_decisions_from_anomalies():
    analysis = {
        "trends": [],
        "correlations": [],
        "anomalies": {"revenue": {"count": 5, "indices": [1, 2, 3, 4, 5]}},
    }
    decisions = PriorityEngine.generate_decisions(analysis)
    assert any("revenue" in d.title.lower() for d in decisions)


def test_get_top_decisions():
    decisions = [
        Decision(f"D{i}", "d", impact=i, effort=5, business_value=i)
        for i in range(1, 8)
    ]
    top = PriorityEngine.get_top_decisions(decisions, count=3)
    assert len(top) == 3
