"""
Sample analysis script demonstrating the complete agent workflow.
Run this to test the agent end-to-end.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.agent import BusinessDecisionAgent


def main():
    """Run complete agent analysis."""
    
    # Initialize agent
    agent = BusinessDecisionAgent()
    
    # Path to sample data
    data_file = "examples/sample_ecommerce_data.csv"
    
    # Run analysis
    results = agent.run(data_file)
    
    # Export results
    agent.export_json("output/analysis_results.json")
    
    # Print CEO summary
    print("\n" + "=" * 60)
    print(agent.get_ceo_summary())
    print("=" * 60)


if __name__ == "__main__":
    main()
