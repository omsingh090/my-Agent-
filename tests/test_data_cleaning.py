"""
Tests for the data cleaning module.
"""

import pytest
import pandas as pd
import numpy as np

from src.data.cleaner import DataCleaner


@pytest.fixture
def sample_df():
    """Return a simple sample dataframe for testing."""
    return pd.DataFrame(
        {
            "revenue": [100.0, 200.0, None, 400.0, 200.0],
            "quantity": [1, 2, 3, 4, 2],
            "category": ["A", "B", None, "A", "B"],
        }
    )


@pytest.fixture
def df_with_duplicates():
    """Return a dataframe with duplicate rows."""
    return pd.DataFrame(
        {
            "revenue": [100.0, 200.0, 100.0],
            "category": ["A", "B", "A"],
        }
    )


def test_remove_duplicates(df_with_duplicates):
    cleaned = DataCleaner.remove_duplicates(df_with_duplicates)
    assert len(cleaned) == 2


def test_handle_missing_numeric(sample_df):
    df, report = DataCleaner.handle_missing_values(sample_df)
    assert df["revenue"].isna().sum() == 0
    assert report["missing_values_handled"] > 0


def test_handle_missing_categorical(sample_df):
    df, report = DataCleaner.handle_missing_values(sample_df)
    assert df["category"].isna().sum() == 0


def test_quality_score_perfect():
    df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    score = DataCleaner.quality_score(df)
    assert score == 100.0


def test_quality_score_with_nulls():
    df = pd.DataFrame({"a": [1, None, 3], "b": [4, 5, None]})
    score = DataCleaner.quality_score(df)
    assert score < 100.0


def test_clean_pipeline(sample_df):
    df_clean, report = DataCleaner.clean(sample_df)
    assert report["final_rows"] <= report["original_rows"]
    assert "quality_score" in report
    assert df_clean.isna().sum().sum() == 0


def test_standardize_formats():
    df = pd.DataFrame({"name": ["Alice ", " BOB", "Charlie"]})
    result = DataCleaner.standardize_formats(df)
    assert result["name"].tolist() == ["alice", "bob", "charlie"]
