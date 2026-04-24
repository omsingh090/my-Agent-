"""
Metrics Evaluator Module
Calculates 10,000-point performance score for agent output.
"""

from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


class MetricsEvaluator:
    """Evaluate agent performance on 10,000-point scale."""

    # Point allocations
    METRICS = {
        "data_quality": 1500,
        "insight_relevance": 2500,
        "decision_actionability": 2500,
        "priority_accuracy": 2000,
        "speed": 1000,
        "ceo_clarity": 500,
    }

    TOTAL_POINTS = 10000

    @staticmethod
    def evaluate(
        data_quality: float,
        insight_count: int,
        decision_count: int,
        avg_priority_score: float,
        processing_time: float,
    ) -> Dict[str, Any]:
        """
        Calculate comprehensive performance score.

        Args:
            data_quality: Data quality score (0-100)
            insight_count: Number of insights generated (0-10)
            decision_count: Number of decisions generated (0-10)
            avg_priority_score: Average priority score (0-10)
            processing_time: Processing time in seconds (0-600)

        Returns:
            Dictionary with detailed metrics breakdown
        """
        scores = {}

        # Data Quality (1,500 pts)
        # Score based on data quality percentage
        scores["data_quality"] = (data_quality / 100.0) * MetricsEvaluator.METRICS["data_quality"]

        # Insight Relevance (2,500 pts)
        # More insights = higher score, but capped at 10
        insight_score = min(insight_count / 10.0, 1.0)
        scores["insight_relevance"] = insight_score * MetricsEvaluator.METRICS["insight_relevance"]

        # Decision Actionability (2,500 pts)
        # Score based on number of decisions (higher = better)
        # But decisions must be specific and ranked
        decision_score = min(decision_count / 7.0, 1.0)  # Cap at 7 decisions
        scores["decision_actionability"] = decision_score * MetricsEvaluator.METRICS["decision_actionability"]

        # Priority Accuracy (2,000 pts)
        # Score based on average priority score (0-10)
        scores["priority_accuracy"] = (avg_priority_score / 10.0) * MetricsEvaluator.METRICS["priority_accuracy"]

        # Speed (1,000 pts)
        # Full points if < 5 minutes (300 seconds)
        # Deduct points for slower processing
        if processing_time <= 300:
            scores["speed"] = MetricsEvaluator.METRICS["speed"]
        else:
            # Linear deduction for slower processing
            deduction = min((processing_time - 300) / 600, 1.0)
            scores["speed"] = (1.0 - deduction) * MetricsEvaluator.METRICS["speed"]

        # CEO Clarity (500 pts)
        # Full points if at least 1 top decision identified
        scores["ceo_clarity"] = (min(decision_count, 1) / 1.0) * MetricsEvaluator.METRICS["ceo_clarity"]

        # Calculate totals
        total_score = sum(scores.values())
        total_score = min(total_score, MetricsEvaluator.TOTAL_POINTS)  # Cap at 10,000

        # Determine grade
        grade = MetricsEvaluator._get_grade(total_score)

        result = {
            "breakdown": scores,
            "total": round(total_score, 0),
            "max": MetricsEvaluator.TOTAL_POINTS,
            "percentage": round((total_score / MetricsEvaluator.TOTAL_POINTS) * 100, 1),
            "grade": grade,
            "details": {
                "data_quality_input": data_quality,
                "insights_count": insight_count,
                "decisions_count": decision_count,
                "avg_priority": avg_priority_score,
                "processing_time_seconds": processing_time,
            },
        }

        logger.info(f"✓ Evaluated performance: {total_score:.0f}/10,000 ({grade})")
        return result

    @staticmethod
    def _get_grade(score: float) -> str:
        """Convert score to letter grade."""
        if score >= 9000:
            return "A+ (Exceptional)"
        elif score >= 8000:
            return "A (Excellent)"
        elif score >= 7000:
            return "B (Good)"
        elif score >= 6000:
            return "C (Fair)"
        else:
            return "D (Needs Improvement)"

    @staticmethod
    def format_report(metrics: Dict[str, Any]) -> str:
        """
        Format metrics as readable report.

        Returns:
            Formatted string report
        """
        report = []
        report.append("\n📊 PERFORMANCE METRICS")
        report.append("═" * 50)

        breakdown = metrics["breakdown"]
        for metric_name, points in breakdown.items():
            max_points = MetricsEvaluator.METRICS.get(metric_name, 0)
            pct = (points / max_points * 100) if max_points > 0 else 0
            report.append(f"  {metric_name.replace('_', ' ').title()}")
            report.append(f"    {points:.0f} / {max_points} points ({pct:.0f}%)")

        report.append("─" * 50)
        report.append(f"Total Score: {metrics['total']:.0f} / {metrics['max']} ({metrics['percentage']:.1f}%)")
        report.append(f"Grade: {metrics['grade']}")
        report.append("═" * 50)

        return "\n".join(report)
