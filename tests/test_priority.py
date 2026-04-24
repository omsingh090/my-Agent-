"""
Tests for the priority engine scoring and ranking.
"""

import pytest

from src.decisions.priority import Decision, PriorityEngine


# --- Priority score edge cases ---

def test_priority_score_zero_impact_zero_value():
    d = Decision("Z", "d", impact=0, effort=10, business_value=0)
    # effort_inv = 0, impact_norm = 0, value_norm = 0 → 0
    assert d.calculate_priority() == pytest.approx(0.0)


def test_priority_score_max():
    d = Decision("Max", "d", impact=10, effort=0, business_value=10)
    assert d.calculate_priority() == pytest.approx(10.0)


def test_priority_score_custom_weights():
    d = Decision("W", "d", impact=10, effort=0, business_value=0)
    # With all weight on impact: score = (1.0 * 1.0 + 0 + 0) * 10 = 10
    score = d.calculate_priority(impact_weight=1.0, effort_weight=0.0, value_weight=0.0)
    assert score == pytest.approx(10.0)


def test_priority_score_effort_inverted():
    low_effort = Decision("LE", "d", impact=5, effort=1, business_value=5)
    high_effort = Decision("HE", "d", impact=5, effort=9, business_value=5)
    assert low_effort.calculate_priority() > high_effort.calculate_priority()


# --- Rank stability ---

def test_rank_is_deterministic():
    decisions = [
        Decision(f"D{i}", "d", impact=i, effort=10 - i, business_value=i)
        for i in range(1, 6)
    ]
    ranked_a = PriorityEngine.rank_decisions(decisions)
    ranked_b = PriorityEngine.rank_decisions(decisions)
    assert [d["title"] for d in ranked_a] == [d["title"] for d in ranked_b]


def test_rank_returns_dicts():
    decisions = [Decision("T", "d", impact=5, effort=5, business_value=5)]
    ranked = PriorityEngine.rank_decisions(decisions)
    assert isinstance(ranked[0], dict)


# --- Threshold behaviour ---

def test_high_priority_threshold_default():
    high = Decision("H", "d", impact=10, effort=1, business_value=10)
    low = Decision("L", "d", impact=1, effort=10, business_value=1)
    assert high.is_high_priority()
    assert not low.is_high_priority()


def test_high_priority_custom_threshold():
    d = Decision("M", "d", impact=6, effort=5, business_value=6)
    score = d.calculate_priority()
    assert d.is_high_priority(threshold=score - 0.1)
    assert not d.is_high_priority(threshold=score + 0.1)


# --- do_this_first flag in to_dict ---

def test_do_this_first_flag_true():
    d = Decision("DoFirst", "d", impact=10, effort=1, business_value=10)
    result = d.to_dict()
    assert result["do_this_first"] is True


def test_do_this_first_flag_false():
    d = Decision("Later", "d", impact=1, effort=10, business_value=1)
    result = d.to_dict()
    assert result["do_this_first"] is False
