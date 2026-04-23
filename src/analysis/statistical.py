"""
Statistical Analysis Module
Performs trend detection, correlation analysis, anomaly detection, and segmentation.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Tuple
from scipy import stats
import logging

logger = logging.getLogger(__name__)


class StatisticalAnalyzer:
    """Perform statistical analysis on data."""

    @staticmethod
    def analyze(df: pd.DataFrame) -> Dict[str, Any]:
        """
        Complete statistical analysis pipeline.

        Args:
            df: Input dataframe

        Returns:
            Dictionary with trends, correlations, anomalies, segments

        Example:
            >>> results = StatisticalAnalyzer.analyze(df)
            >>> print(f"Trends: {len(results['trends'])}")
            Trends: 3
        """
        analysis = {
            "descriptive_stats": StatisticalAnalyzer.descriptive_stats(df),
            "trends": StatisticalAnalyzer.detect_trends(df),
            "correlations": StatisticalAnalyzer.correlations(df),
            "anomalies": StatisticalAnalyzer.detect_anomalies(df),
            "segments": StatisticalAnalyzer.segment_analysis(df),
        }

        logger.info("✓ Analysis complete")
        return analysis

    @staticmethod
    def descriptive_stats(df: pd.DataFrame) -> Dict[str, Dict[str, float]]:
        """Calculate descriptive statistics for each numeric column."""
        stats_dict = {}

        for col in df.select_dtypes(include=[np.number]).columns:
            stats_dict[col] = {
                "mean": float(df[col].mean()),
                "median": float(df[col].median()),
                "std": float(df[col].std()),
                "min": float(df[col].min()),
                "max": float(df[col].max()),
                "q1": float(df[col].quantile(0.25)),
                "q3": float(df[col].quantile(0.75)),
            }

        return stats_dict

    @staticmethod
    def detect_trends(df: pd.DataFrame) -> List[Dict[str, Any]]:
        """
        Detect trends in numeric columns.

        Returns:
            List of trend dictionaries with column, direction, magnitude
        """
        trends = []

        numeric_cols = df.select_dtypes(include=[np.number]).columns

        for col in numeric_cols:
            if len(df[col]) < 2:
                continue

            # Simple trend: compare first half vs second half
            mid = len(df[col]) // 2
            first_half_mean = df[col].iloc[:mid].mean()
            second_half_mean = df[col].iloc[mid:].mean()

            if first_half_mean == 0:
                continue

            pct_change = ((second_half_mean - first_half_mean) / abs(first_half_mean)) * 100

            if abs(pct_change) > 5:  # Threshold for trend significance
                trends.append(
                    {
                        "column": col,
                        "direction": "increasing" if pct_change > 0 else "decreasing",
                        "magnitude": round(abs(pct_change), 2),
                        "confidence": min(100, abs(pct_change) * 2),
                    }
                )

        logger.info(f"  • Detected {len(trends)} trends")
        return trends

    @staticmethod
    def correlations(df: pd.DataFrame, threshold: float = 0.5) -> List[Dict[str, Any]]:
        """
        Find significant correlations between numeric columns.

        Args:
            df: Input dataframe
            threshold: Correlation threshold (default 0.5)

        Returns:
            List of correlation pairs
        """
        numeric_df = df.select_dtypes(include=[np.number])

        if len(numeric_df.columns) < 2:
            return []

        corr_matrix = numeric_df.corr()
        correlations = []

        for i in range(len(corr_matrix.columns)):
            for j in range(i + 1, len(corr_matrix.columns)):
                corr_value = corr_matrix.iloc[i, j]

                if abs(corr_value) > threshold:
                    correlations.append(
                        {
                            "column1": corr_matrix.columns[i],
                            "column2": corr_matrix.columns[j],
                            "correlation": round(float(corr_value), 3),
                            "strength": "strong" if abs(corr_value) > 0.7 else "moderate",
                        }
                    )

        logger.info(f"  • Found {len(correlations)} significant correlations")
        return correlations

    @staticmethod
    def detect_anomalies(df: pd.DataFrame) -> Dict[str, List[int]]:
        """
        Detect anomalies using Interquartile Range (IQR) method.

        Returns:
            Dictionary mapping column names to list of anomaly indices
        """
        anomalies = {}

        for col in df.select_dtypes(include=[np.number]).columns:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1

            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR

            anomaly_indices = df[(df[col] < lower_bound) | (df[col] > upper_bound)].index.tolist()

            if anomaly_indices:
                anomalies[col] = {
                    "count": len(anomaly_indices),
                    "indices": anomaly_indices[:10],  # Top 10
                    "lower_bound": round(lower_bound, 2),
                    "upper_bound": round(upper_bound, 2),
                }

        logger.info(f"  • Detected {sum(len(v.get('indices', [])) for v in anomalies.values())} anomalies")
        return anomalies

    @staticmethod
    def segment_analysis(df: pd.DataFrame) -> Dict[str, Dict[str, Any]]:
        """
        Analyze categorical segments.

        Returns:
            Dictionary with segment statistics
        """
        segments = {}

        for col in df.select_dtypes(include=["object"]).columns:
            segment_counts = df[col].value_counts()

            segments[col] = {
                "unique_values": len(segment_counts),
                "top_segments": segment_counts.head(5).to_dict(),
                "distribution": "balanced" if segment_counts.max() / segment_counts.min() < 3 else "skewed",
            }

        logger.info(f"  • Analyzed {len(segments)} categorical columns")
        return segments
