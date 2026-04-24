"""
Main Agent Module
Orchestrates the complete data → decisions → metrics pipeline.
"""

import time
import logging
from typing import Dict, Any
import json

from src.config import config
from src.data.loader import DataLoader
from src.data.cleaner import DataCleaner
from src.analysis.statistical import StatisticalAnalyzer
from src.insights.generator import InsightGenerator
from src.decisions.priority import PriorityEngine
from src.metrics.evaluator import MetricsEvaluator

# Configure logging
logging.basicConfig(
    level=config.log_level,
    format='%(message)s'
)
logger = logging.getLogger(__name__)


class BusinessDecisionAgent:
    """
    AI-Powered Business Decision Analyst Agent.

    Transforms raw business data into:
    1. Cleaned datasets
    2. Meaningful analytical insights  ← now powered by InsightGenerator
    3. Actionable business decisions
    4. Prioritized recommendations

    Pipeline: Load → Clean → Analyze → Insights → Decide → Evaluate
    """

    def __init__(self):
        """Initialize the agent and insight generator."""
        self.results = {}
        self.start_time = None

        # Initialize InsightGenerator with API key from config (falls back
        # to rule-based mode automatically when no key is set)
        self.insight_generator = InsightGenerator(
            api_key=config.llm.api_key,
            model=config.llm.model,
        )

    def run(self, file_path: str) -> Dict[str, Any]:
        """
        Run complete analysis pipeline.

        Args:
            file_path: Path to data file (CSV, JSON, Excel)

        Returns:
            Dictionary with all analysis results

        Example:
            >>> agent = BusinessDecisionAgent()
            >>> results = agent.run("examples/sample_ecommerce_data.csv")
            >>> print(results['metrics'])
        """
        self.start_time = time.time()

        try:
            logger.info("🤖 AI BUSINESS DECISION ANALYST AGENT")
            logger.info("=" * 60)

            # Step 1: Load Data
            logger.info("\n📂 LOADING DATA")
            df, load_metadata = self._load_data(file_path)
            self.results["load_metadata"] = load_metadata

            # Step 2: Clean Data
            logger.info("\n🧹 CLEANING DATA")
            df, clean_report = self._clean_data(df)
            self.results["clean_report"] = clean_report

            # Step 3: Analyze Data
            logger.info("\n🔍 ANALYZING DATA")
            analysis = self._analyze_data(df)
            self.results["analysis"] = analysis

            # Step 4: Generate Insights  ← NEW — wired in here
            logger.info("\n💡 GENERATING INSIGHTS")
            insights = self._generate_insights(analysis)
            self.results["insights"] = insights

            # Step 5: Generate Decisions
            logger.info("\n🎯 GENERATING DECISIONS")
            decisions = self._generate_decisions(analysis)
            self.results["decisions"] = decisions

            # Step 6: Evaluate Performance
            logger.info("\n📊 EVALUATING PERFORMANCE")
            metrics = self._evaluate_performance(analysis, decisions, insights)
            self.results["metrics"] = metrics

            # Summary
            self._print_summary()

            return self.results

        except Exception as e:
            logger.error(f"❌ Error: {str(e)}")
            raise

    # ── Pipeline steps ────────────────────────────────────────────────────────

    def _load_data(self, file_path: str) -> tuple:
        """Load data from file."""
        df, metadata = DataLoader.load(file_path)
        logger.info(f"✓ Loaded {metadata['rows']} rows, {metadata['columns']} columns")
        return df, metadata

    def _clean_data(self, df):
        """Clean and validate data."""
        df, report = DataCleaner.clean(df)
        logger.info(f"✓ Data Quality Score: {report['quality_score']}/100")
        return df, report

    def _analyze_data(self, df):
        """Perform statistical analysis."""
        analysis = StatisticalAnalyzer.analyze(df)
        logger.info(f"✓ Trends identified: {len(analysis['trends'])}")
        logger.info(f"✓ Correlations found: {len(analysis['correlations'])}")
        logger.info(
            f"✓ Anomalies detected: "
            f"{sum(len(a.get('indices', [])) for a in analysis['anomalies'].values())}"
        )
        return analysis

    def _generate_insights(self, analysis: Dict[str, Any]) -> list:
        """
        Generate business insights from analysis results.

        Uses LLM when OPENAI_API_KEY is set in .env.
        Automatically falls back to rule-based insights otherwise.
        """
        insights = self.insight_generator.generate(analysis)
        mode = "LLM-powered" if config.llm.api_key else "rule-based"
        logger.info(f"✓ Generated {len(insights)} insights ({mode})")
        return insights

    def _generate_decisions(self, analysis: Dict[str, Any]) -> list:
        """Generate and rank decisions from analysis."""
        decisions = PriorityEngine.generate_decisions(analysis)
        ranked = PriorityEngine.rank_decisions(decisions)
        logger.info(f"✓ Generated {len(ranked)} decisions")
        return ranked

    def _evaluate_performance(
        self,
        analysis: Dict[str, Any],
        decisions: list,
        insights: list,
    ) -> Dict[str, Any]:
        """Evaluate agent performance."""
        processing_time = time.time() - self.start_time

        data_quality = self.results["clean_report"].get("quality_score", 80)

        # Count insights + analysis signals for insight_count
        insight_count = len(insights) + len(analysis.get("trends", [])) + len(
            analysis.get("correlations", [])
        )
        decision_count = len(decisions)
        avg_priority = sum(d.get("priority_score", 5) for d in decisions) / max(
            decision_count, 1
        )

        metrics = MetricsEvaluator.evaluate(
            data_quality=data_quality,
            insight_count=insight_count,
            decision_count=decision_count,
            avg_priority_score=avg_priority,
            processing_time=processing_time,
        )

        return metrics

    # ── Output helpers ────────────────────────────────────────────────────────

    def _print_summary(self):
        """Print executive summary to console."""
        logger.info("\n" + "=" * 60)
        logger.info("📊 TOP DECISIONS (Ranked by Priority)")
        logger.info("─" * 60)

        decisions = self.results.get("decisions", [])
        for i, decision in enumerate(decisions[:3], 1):
            logger.info(
                f"\n{i}️⃣  {decision['title']} (Priority: {decision['priority_score']}/10)"
            )
            logger.info(
                f"   📊 Impact: {decision['impact']}/10 | "
                f"⚙️  Effort: {decision['effort']}/10 | "
                f"💰 Value: {decision['business_value']}/10"
            )
            if decision["do_this_first"]:
                logger.info("   >>> DO THIS FIRST <<<")

        # Key insights summary
        insights = self.results.get("insights", [])
        if insights:
            logger.info("\n💡 KEY INSIGHTS")
            logger.info("─" * 60)
            for ins in insights[:3]:
                title = ins.get("title", "")
                impact = ins.get("impact", "")
                logger.info(f"  • [{impact.upper()}] {title}")

        metrics = self.results.get("metrics", {})
        logger.info(MetricsEvaluator.format_report(metrics))

        logger.info("\n👔 EXECUTIVE SUMMARY")
        logger.info("═" * 60)
        if decisions:
            top = decisions[0]
            logger.info(f"🎯 Top Priority: {top['title']}")
            logger.info(f"   Evidence: {top['evidence']}")
            logger.info(f"   Timeline: {top['implementation_days']} days")
            logger.info(f"   Performance Grade: {metrics['grade']}")
        logger.info("═" * 60 + "\n")

    def export_json(self, output_path: str = "output/analysis_results.json") -> str:
        """Export all results as a JSON file."""
        import os
        os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".", exist_ok=True)
        with open(output_path, "w") as f:
            json.dump(self.results, f, indent=2)
        logger.info(f"✓ Results exported to {output_path}")
        return output_path

    def get_ceo_summary(self) -> str:
        """
        Get a one-page executive summary.

        Returns:
            Formatted executive summary string
        """
        decisions = self.results.get("decisions", [])
        insights = self.results.get("insights", [])
        metrics = self.results.get("metrics", {})

        lines = []
        lines.append("AI BUSINESS DECISION ANALYST — EXECUTIVE SUMMARY")
        lines.append("=" * 50)

        # Top decisions
        lines.append("\nTOP 3 DECISIONS (Ranked by Priority)")
        lines.append("-" * 50)
        for i, d in enumerate(decisions[:3], 1):
            lines.append(f"\n{i}. {d['title']}")
            lines.append(f"   Priority Score: {d['priority_score']}/10")
            lines.append(f"   Evidence:       {d['evidence']}")
            lines.append(f"   Timeline:       {d['implementation_days']} days")
            if d["do_this_first"]:
                lines.append("   ★ DO THIS FIRST")

        # Key insights
        if insights:
            lines.append("\n\nKEY INSIGHTS")
            lines.append("-" * 50)
            for ins in insights[:3]:
                lines.append(f"  • [{ins.get('impact','').upper()}] {ins.get('title','')}")
                lines.append(f"    {ins.get('description','')[:120]}")

        # Performance score
        lines.append("\n\nPERFORMANCE GRADE")
        lines.append("-" * 50)
        lines.append(f"Overall Score: {metrics.get('total', 0):.0f}/{metrics.get('max', 10000)}")
        lines.append(f"Grade:         {metrics.get('grade', 'N/A')}")

        return "\n".join(lines)
