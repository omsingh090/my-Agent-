"""
Tests for the statistical analysis module.
"""

import pytest
import pandas as pd
import numpy as np

from src.analysis.statistical import StatisticalAnalyzer


@pytest.fixture
def trending_df():
    """Return a dataframe with clear upward trend in revenue."""
    return pd.DataFrame(
        {
            "revenue": [100, 110, 120, 130, 140, 150, 160, 170, 180, 190],
            "quantity": [1, 2, 1, 2, 1, 2, 1, 2, 1, 2],
        }
    )


@pytest.fixture
def correlated_df():
    """Return a dataframe with strong correlation."""
    x = list(range(1, 21))
    return pd.DataFrame({"price": x, "revenue": [v * 10 for v in x]})


@pytest.fixture
def anomaly_df():
    """Return a dataframe with an obvious outlier."""
    values = [10, 11, 12, 10, 11, 12, 10, 11, 12, 1000]
    return pd.DataFrame({"metric": values})


def test_descriptive_stats(trending_df):
    stats = StatisticalAnalyzer.descriptive_stats(trending_df)
    assert "revenue" in stats
    assert "mean" in stats["revenue"]
    assert stats["revenue"]["mean"] == pytest.approx(145.0)


def test_detect_trends(trending_df):
    trends = StatisticalAnalyzer.detect_trends(trending_df)
    assert len(trends) > 0
    revenue_trend = next((t for t in trends if t["column"] == "revenue"), None)
    assert revenue_trend is not None
    assert revenue_trend["direction"] == "increasing"


def test_no_trend_for_static_column(correlated_df):
    # quantity is evenly balanced; revenue trends strongly
    df = pd.DataFrame({"stable": [5, 5, 5, 5, 5, 5, 5, 5, 5, 5]})
    trends = StatisticalAnalyzer.detect_trends(df)
    assert len(trends) == 0


def test_correlations(correlated_df):
    corrs = StatisticalAnalyzer.correlations(correlated_df)
    assert len(corrs) > 0
    assert corrs[0]["strength"] == "strong"
    assert abs(corrs[0]["correlation"]) > 0.9


def test_no_correlation_below_threshold():
    df = pd.DataFrame({"a": [1, 2, 3, 4, 5], "b": [5, 1, 3, 2, 4]})
    corrs = StatisticalAnalyzer.correlations(df, threshold=0.9)
    assert len(corrs) == 0


def test_detect_anomalies(anomaly_df):
    anomalies = StatisticalAnalyzer.detect_anomalies(anomaly_df)
    assert "metric" in anomalies
    assert anomalies["metric"]["count"] >= 1


def test_no_anomalies_in_uniform_data():
    df = pd.DataFrame({"val": [10, 10, 10, 10, 10]})
    anomalies = StatisticalAnalyzer.detect_anomalies(df)
    assert len(anomalies) == 0


def test_segment_analysis():
    df = pd.DataFrame({"category": ["A", "B", "A", "C", "B", "A"]})
    segments = StatisticalAnalyzer.segment_analysis(df)
    assert "category" in segments
    assert segments["category"]["unique_values"] == 3


def test_full_analyze_pipeline(trending_df):
    results = StatisticalAnalyzer.analyze(trending_df)
    assert "trends" in results
    assert "correlations" in results
    assert "anomalies" in results
    assert "segments" in results
    assert "descriptive_stats" in results
