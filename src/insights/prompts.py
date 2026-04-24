"""
Prompt Templates Module
Defines structured prompts for LLM-powered insight generation.
"""

from typing import Dict, Any


class InsightPrompts:
    """Prompt templates for business insight generation."""

    SYSTEM_PROMPT = """You are an expert business analyst with deep expertise in 
data interpretation and strategic decision-making. Your role is to analyze 
business data and generate specific, actionable insights that drive revenue 
and efficiency."""

    @staticmethod
    def build_analysis_prompt(analysis_results: Dict[str, Any], context: str = "") -> str:
        """
        Build a structured prompt for insight generation.

        Args:
            analysis_results: Output from StatisticalAnalyzer
            context: Optional business context string

        Returns:
            Formatted prompt string
        """
        trends = analysis_results.get("trends", [])
        correlations = analysis_results.get("correlations", [])
        anomalies = analysis_results.get("anomalies", {})

        trend_lines = "\n".join(
            f"  - {t['column']}: {t['direction']} by {t['magnitude']}%"
            for t in trends
        ) or "  None detected"

        corr_lines = "\n".join(
            f"  - {c['column1']} ↔ {c['column2']}: {c['strength']} ({c['correlation']})"
            for c in correlations
        ) or "  None detected"

        anom_lines = "\n".join(
            f"  - {col}: {data['count']} anomalies"
            for col, data in anomalies.items()
        ) or "  None detected"

        context_section = f"\nBusiness Context:\n{context}\n" if context else ""

        return f"""Analyze the following business data patterns and generate 3-5 specific,
actionable insights with quantified impact estimates.{context_section}

DATA PATTERNS DETECTED:

Trends:
{trend_lines}

Correlations:
{corr_lines}

Anomalies:
{anom_lines}

For each insight provide:
1. A clear title (what is happening)
2. Root cause (why it is happening)
3. Business impact (revenue/cost/customer effect with numbers)
4. Recommended action (specific next step)
"""

    @staticmethod
    def build_decision_prompt(insights: list, top_n: int = 3) -> str:
        """
        Build a prompt to convert insights into ranked decisions.

        Args:
            insights: List of insight strings or dicts
            top_n: Number of top decisions to request

        Returns:
            Formatted prompt string
        """
        insight_text = "\n".join(
            f"  {i + 1}. {insight}" for i, insight in enumerate(insights)
        )

        return f"""Based on the following business insights, generate the top {top_n} 
prioritized decisions ranked by impact and ease of implementation.

INSIGHTS:
{insight_text}

For each decision provide:
- Title: Specific action to take
- Impact score (1-10): Revenue or cost impact
- Effort score (1-10): Implementation complexity
- Business value (1-10): Strategic alignment
- Timeline: Days to implement
- Expected outcome: Quantified result
"""
