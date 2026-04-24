#!/usr/bin/env python3
"""
AI Business Decision Analyst Agent — Entry Point

Usage:
    python main.py
    python main.py --data examples/sample_ecommerce_data.csv
    python main.py --data data/your_file.csv --output results/output.json

Runs the full pipeline:
    Load → Clean → Analyze → Insights → Decisions → Rank → Score → Export
"""

import argparse
import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env before anything else
load_dotenv()

from src.agent import BusinessDecisionAgent


def parse_args():
    parser = argparse.ArgumentParser(
        description="AI Business Decision Analyst Agent",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py
  python main.py --data examples/sample_ecommerce_data.csv
  python main.py --data data/sales.csv --output results/output.json
        """,
    )
    parser.add_argument(
        "--data",
        default="examples/sample_ecommerce_data.csv",
        help="Path to input CSV/JSON/Excel file (default: examples/sample_ecommerce_data.csv)",
    )
    parser.add_argument(
        "--output",
        default="output/analysis_results.json",
        help="Path for JSON output file (default: output/analysis_results.json)",
    )
    parser.add_argument(
        "--ceo",
        action="store_true",
        default=True,
        help="Print CEO executive summary (default: True)",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    # Validate input file
    if not os.path.exists(args.data):
        print(f"❌ Error: Data file not found: {args.data}")
        print("   Make sure you are running from the project root directory.")
        sys.exit(1)

    # Ensure output directory exists
    output_dir = os.path.dirname(args.output)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    # Run the agent
    agent = BusinessDecisionAgent()
    results = agent.run(args.data)

    # Export JSON results
    agent.export_json(args.output)

    # Print CEO summary
    if args.ceo:
        print("\n" + "=" * 60)
        print(agent.get_ceo_summary())
        print("=" * 60)

    return results


if __name__ == "__main__":
    main()
