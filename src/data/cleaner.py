"""
Data Cleaner Module
Handles data cleaning: missing values, duplicates, format standardization.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, Tuple
import logging

logger = logging.getLogger(__name__)


class DataCleaner:
    """Clean and standardize data."""

    @staticmethod
    def clean(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """
        Complete data cleaning pipeline.

        Args:
            df: Input dataframe

        Returns:
            Tuple of (cleaned_df, cleaning_report)

        Example:
            >>> df_clean, report = DataCleaner.clean(df)
            >>> print(report['duplicates_removed'])
            5
        """
        report = {"original_rows": len(df)}

        # Step 1: Remove duplicates
        df = DataCleaner.remove_duplicates(df)
        report["duplicates_removed"] = report["original_rows"] - len(df)

        # Step 2: Handle missing values
        df, missing_report = DataCleaner.handle_missing_values(df)
        report.update(missing_report)

        # Step 3: Standardize formats
        df = DataCleaner.standardize_formats(df)
        report["format_standardized"] = True

        # Step 4: Calculate quality score
        report["quality_score"] = DataCleaner.quality_score(df)
        report["final_rows"] = len(df)

        logger.info(f"✓ Cleaned: {report['original_rows']} → {report['final_rows']} rows")
        return df, report

    @staticmethod
    def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
        """Remove exact duplicate rows."""
        before = len(df)
        df = df.drop_duplicates()
        removed = before - len(df)
        if removed > 0:
            logger.info(f"  • Removed {removed} duplicates")
        return df

    @staticmethod
    def handle_missing_values(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """
        Handle missing values using imputation.

        Returns:
            Tuple of (cleaned_df, missing_value_report)
        """
        report = {"missing_values_handled": 0, "columns_with_missing": {}}

        for col in df.columns:
            missing_count = df[col].isna().sum()
            if missing_count == 0:
                continue

            missing_pct = (missing_count / len(df)) * 100
            report["columns_with_missing"][col] = {
                "count": missing_count,
                "percentage": round(missing_pct, 2),
            }

            # Impute based on data type
            if df[col].dtype in ["float64", "int64"]:
                # Use median for numeric
                df[col] = df[col].fillna(df[col].median())
            else:
                # Use mode for categorical
                mode_val = df[col].mode()
                if len(mode_val) > 0:
                    df[col] = df[col].fillna(mode_val[0])

            report["missing_values_handled"] += missing_count
            logger.info(f"  • Imputed {missing_count} missing values in {col}")

        return df, report

    @staticmethod
    def standardize_formats(df: pd.DataFrame) -> pd.DataFrame:
        """Standardize data formats (dates, strings, numbers)."""
        for col in df.columns:
            # Try to parse dates (only for object/string columns)
            if df[col].dtype.kind == "O":
                try:
                    df[col] = pd.to_datetime(df[col])
                    logger.info(f"  • Standardized {col} as datetime")
                except (ValueError, TypeError):
                    # Standardize as lowercase stripped string
                    df[col] = df[col].astype(str).str.lower().str.strip()

        return df

    @staticmethod
    def quality_score(df: pd.DataFrame) -> float:
        """
        Calculate data quality score (0-100).

        Factors:
        - No null values
        - No duplicates
        - Proper data types
        """
        score = 100.0

        # Penalty for null values
        null_pct = (df.isna().sum().sum() / (len(df) * len(df.columns))) * 100
        score -= null_pct * 0.5

        # Penalty for high cardinality in categorical
        for col in df.select_dtypes(include=["object"]).columns:
            unique_ratio = df[col].nunique() / len(df)
            if unique_ratio > 0.9:
                score -= 5

        return max(0, round(score, 1))
