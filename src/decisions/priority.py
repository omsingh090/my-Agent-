"""
Priority Engine Module
Ranks decisions by Impact, Effort, and Business Value.
THIS IS THE CORE DIFFERENTIATOR OF THE AGENT.
"""

from dataclasses import dataclass
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)


@dataclass
class Decision:
    """Represents a business decision with priority scoring."""

    title: str
    description: str
    impact: int  # 1-10
    effort: int  # 1-10
    business_value: int  # 1-10
    evidence: str = ""
    confidence: float = 0.9
    implementation_days: int = 0

    def calculate_priority(self, impact_weight: float = 0.4, effort_weight: float = 0.3, value_weight: float = 0.3) -> float:
        """
        Calculate priority score.

        Formula:
        Priority = (Impact × 0.4) + (Effort_Inverted × 0.3) + (Value × 0.3)

        Why effort is inverted:
        - Lower effort = easier to implement = should be higher priority
        - Stratified thinking: high impact + low effort = immediate action

        Args:
            impact_weight: Weight for impact (default 0.4 = 40%)
            effort_weight: Weight for effort (default 0.3 = 30%)
            value_weight: Weight for business value (default 0.3 = 30%)

        Returns:
            Priority score 0-10
        """
        # Normalize scores to 0-1 range
        impact_norm = self.impact / 10.0
        effort_norm = 1.0 - (self.effort / 10.0)  # INVERT: lower effort = higher score
        value_norm = self.business_value / 10.0

        # Weighted sum
        priority = (impact_norm * impact_weight + 
                   effort_norm * effort_weight + 
                   value_norm * value_weight) * 10

        return round(priority, 1)

    def is_high_priority(self, threshold: float = 7.5) -> bool:
        """Check if decision is high priority (should be done first)."""
        return self.calculate_priority() >= threshold

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "title": self.title,
            "description": self.description,
            "impact": self.impact,
            "effort": self.effort,
            "business_value": self.business_value,
            "evidence": self.evidence,
            "confidence": self.confidence,
            "implementation_days": self.implementation_days,
            "priority_score": self.calculate_priority(),
            "do_this_first": self.is_high_priority(),
        }


class PriorityEngine:
    """Generate and rank business decisions."""

    @staticmethod
    def generate_decisions(analysis_results: Dict[str, Any]) -> List[Decision]:
        """
        Generate decisions from analysis results.

        Args:
            analysis_results: Output from StatisticalAnalyzer

        Returns:
            List of Decision objects
        """
        decisions = []

        # Decision 1: Address significant trends
        if analysis_results.get("trends"):
            for trend in analysis_results["trends"]:
                decision = Decision(
                    title=f"Address {trend['column']} {trend['direction']} trend",
                    description=f"The {trend['column']} is {trend['direction']} by {trend['magnitude']}%. This indicates significant business change.",
                    impact=8 if trend["magnitude"] > 10 else 6,
                    effort=4,
                    business_value=7,
                    evidence=f"Trend magnitude: {trend['magnitude']}%",
                    confidence=0.85,
                    implementation_days=7,
                )
                decisions.append(decision)

        # Decision 2: Leverage strong correlations
        if analysis_results.get("correlations"):
            for corr in analysis_results["correlations"]:
                decision = Decision(
                    title=f"Leverage {corr['column1']}-{corr['column2']} correlation",
                    description=f"Strong {corr['strength']} correlation ({corr['correlation']}) between {corr['column1']} and {corr['column2']} suggests optimization opportunity.",
                    impact=7,
                    effort=5,
                    business_value=7,
                    evidence=f"Correlation coefficient: {corr['correlation']}",
                    confidence=0.80,
                    implementation_days=10,
                )
                decisions.append(decision)

        # Decision 3: Investigate anomalies
        if analysis_results.get("anomalies"):
            for col, anom_data in analysis_results["anomalies"].items():
                decision = Decision(
                    title=f"Investigate {col} anomalies",
                    description=f"Detected {anom_data['count']} anomalies in {col}. These may indicate errors, fraud, or unique opportunities.",
                    impact=6,
                    effort=6,
                    business_value=8,
                    evidence=f"Anomaly count: {anom_data['count']}",
                    confidence=0.75,
                    implementation_days=5,
                )
                decisions.append(decision)

        # Decision 4: Optimize data pipeline
        if len(analysis_results) > 2:
            decision = Decision(
                title="Optimize data pipeline",
                description="Implement automated data quality checks and monitoring to prevent future data issues.",
                impact=6,
                effort=6,
                business_value=8,
                evidence="Data quality varies across pipeline",
                confidence=0.70,
                implementation_days=14,
            )
            decisions.append(decision)

        logger.info(f"✓ Generated {len(decisions)} decisions")
        return decisions

    @staticmethod
    def rank_decisions(decisions: List[Decision]) -> List[Dict[str, Any]]:
        """
        Rank decisions by priority score.

        Args:
            decisions: List of Decision objects

        Returns:
            List of ranked decision dictionaries
        """
        ranked = sorted(decisions, key=lambda d: d.calculate_priority(), reverse=True)

        logger.info(f"✓ Ranked {len(ranked)} decisions")
        logger.info(f"  • Top decision: {ranked[0].title} (Priority: {ranked[0].calculate_priority()}/10)")

        return [d.to_dict() for d in ranked]

    @staticmethod
    def get_top_decisions(decisions: List[Decision], count: int = 3) -> List[Dict[str, Any]]:
        """
        Get top N decisions (those that should be done first).

        Args:
            decisions: List of Decision objects
            count: Number of top decisions to return

        Returns:
            List of top decision dictionaries
        """
        ranked = PriorityEngine.rank_decisions(decisions)
        return ranked[:count]
