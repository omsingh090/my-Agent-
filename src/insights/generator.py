"""
Insight Generator Module
Generates LLM-powered contextual business insights from statistical analysis.
Falls back to rule-based insights when no LLM API key is configured.
"""

import logging
from typing import Dict, Any, List

from src.insights.prompts import InsightPrompts

logger = logging.getLogger(__name__)


class InsightGenerator:
    """Generate business insights from analysis results."""

    def __init__(self, api_key: str = "", model: str = "gpt-4"):
        """
        Initialize the insight generator.

        Args:
            api_key: OpenAI API key (optional; falls back to rule-based mode)
            model: LLM model name
        """
        self.api_key = api_key
        self.model = model
        self._llm_available = bool(api_key)

    def generate(
        self,
        analysis_results: Dict[str, Any],
        context: str = "",
    ) -> List[Dict[str, Any]]:
        """
        Generate insights from analysis results.

        Uses LLM when an API key is available, otherwise falls back to
        rule-based insight generation.

        Args:
            analysis_results: Output from StatisticalAnalyzer
            context: Optional business context string

        Returns:
            List of insight dictionaries with title, description, impact

        Example:
            >>> gen = InsightGenerator()
            >>> insights = gen.generate(analysis_results)
            >>> print(insights[0]['title'])
        """
        if self._llm_available:
            return self._generate_llm_insights(analysis_results, context)
        return self._generate_rule_based_insights(analysis_results)

    def _generate_llm_insights(
        self,
        analysis_results: Dict[str, Any],
        context: str,
    ) -> List[Dict[str, Any]]:
        """Generate insights using LLM API."""
        try:
            import openai

            openai.api_key = self.api_key
            prompt = InsightPrompts.build_analysis_prompt(analysis_results, context)

            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": InsightPrompts.SYSTEM_PROMPT},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.7,
                max_tokens=1500,
            )

            raw_text = response.choices[0].message.content
            logger.info("✓ LLM insights generated")
            return self._parse_llm_response(raw_text)

        except Exception as e:
            logger.warning(f"LLM insight generation failed: {e}. Falling back to rule-based.")
            return self._generate_rule_based_insights(analysis_results)

    def _generate_rule_based_insights(
        self, analysis_results: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Generate rule-based insights without LLM.

        Produces structured insights directly from statistical patterns.
        """
        insights = []

        # Trend insights
        for trend in analysis_results.get("trends", []):
            direction = trend["direction"]
            col = trend["column"]
            magnitude = trend["magnitude"]
            insights.append(
                {
                    "title": f"{col.replace('_', ' ').title()} is {direction}",
                    "description": (
                        f"{col} has {direction} by {magnitude:.1f}% over the analysis period. "
                        f"This pattern warrants immediate attention for strategic planning."
                    ),
                    "impact": "high" if magnitude > 15 else "medium",
                    "source": "trend_analysis",
                }
            )

        # Correlation insights
        for corr in analysis_results.get("correlations", []):
            col1 = corr["column1"].replace("_", " ")
            col2 = corr["column2"].replace("_", " ")
            strength = corr["strength"]
            coefficient = corr["correlation"]
            insights.append(
                {
                    "title": f"{col1.title()} and {col2.title()} are {strength}ly correlated",
                    "description": (
                        f"A {strength} correlation (r={coefficient}) between {col1} and {col2} "
                        f"suggests a leverage opportunity: improving one metric will drive the other."
                    ),
                    "impact": "high" if strength == "strong" else "medium",
                    "source": "correlation_analysis",
                }
            )

        # Anomaly insights
        for col, anom_data in analysis_results.get("anomalies", {}).items():
            count = anom_data["count"]
            insights.append(
                {
                    "title": f"Unusual activity detected in {col.replace('_', ' ')}",
                    "description": (
                        f"{count} anomalous data point(s) found in {col} "
                        f"(outside range [{anom_data['lower_bound']}, {anom_data['upper_bound']}]). "
                        f"These may indicate errors, fraud, or unique business opportunities."
                    ),
                    "impact": "medium",
                    "source": "anomaly_detection",
                }
            )

        logger.info(f"✓ Generated {len(insights)} rule-based insights")
        return insights

    @staticmethod
    def _parse_llm_response(raw_text: str) -> List[Dict[str, Any]]:
        """
        Parse LLM response text into structured insight dictionaries.

        Args:
            raw_text: Raw text from LLM response

        Returns:
            List of insight dictionaries
        """
        insights = []
        blocks = raw_text.strip().split("\n\n")

        for block in blocks:
            lines = [line.strip() for line in block.strip().splitlines() if line.strip()]
            if not lines:
                continue
            insights.append(
                {
                    "title": lines[0].lstrip("0123456789.-) "),
                    "description": " ".join(lines[1:]) if len(lines) > 1 else lines[0],
                    "impact": "medium",
                    "source": "llm",
                }
            )

        return insights
