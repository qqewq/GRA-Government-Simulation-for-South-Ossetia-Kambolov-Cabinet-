"""
CLI entry point for the GRA Government Simulation.

Usage: python -m gra_government.cli.main --config config.yaml
"""

import argparse
import sys
from pathlib import Path

from gra_government.config import AppConfig
from gra_government.logger import setup_logging
from gra_government.llm.interface import DummyLLMClient
from gra_government.agents.economy import EconomyAgent
from gra_government.agents.demography import DemographyAgent
from gra_government.agents.infrastructure import InfrastructureAgent
from gra_government.agents.social_stability import SocialStabilityAgent
from gra_government.agents.security import SecurityAgent
from gra_government.agents.media import MediaAgent
from gra_government.swarm.orchestrator import CabinetOrchestrator
from gra_government.scenario.state_model import SimulationState
from gra_government.reporting.reporter import generate_report

def main():
    parser = argparse.ArgumentParser(description="GRA Government Simulation CLI")
    parser.add_argument(
        "--config",
        type=str,
        default="config.example.yaml",
        help="Path to configuration YAML file",
    )
    parser.add_argument(
        "--language",
        type=str,
        default="ru",
        choices=["ru", "en"],
        help="Report language",
    )
    args = parser.parse_args()

    # Load configuration
    config_path = Path(args.config)
    if not config_path.exists():
        print(f"Config file {config_path} not found. Using default configuration.")
        config = AppConfig.default()
    else:
        try:
            config = AppConfig.from_yaml(config_path)
        except ImportError:
            print("PyYAML not installed. Using default configuration. Install with `pip install pyyaml`.")
            config = AppConfig.default()
        except Exception as e:
            print(f"Error loading config: {e}. Using defaults.")
            config = AppConfig.default()

    setup_logging(config.logging.level)

    # Create LLM client (dummy for now, real provider can be plugged later)
    llm_client = DummyLLMClient()

    # Instantiate domain agents
    agents = [
        EconomyAgent(llm_client=llm_client),
        DemographyAgent(llm_client=llm_client),
        InfrastructureAgent(llm_client=llm_client),
        SocialStabilityAgent(llm_client=llm_client),
        SecurityAgent(llm_client=llm_client),
        MediaAgent(llm_client=llm_client),
    ]

    # Orchestrator with government perspective (can be changed)
    orchestrator = CabinetOrchestrator(agents, perspective="government")

    # Initial simulation state
    state = SimulationState.default()

    # Run one advisory cycle
    cycle_result = orchestrator.run_cycle(state)

    # Generate report
    report = generate_report(
        state=state,
        cabinet_policy=cycle_result["cabinet_policy"],
        stability=cycle_result["stability"],
        language=args.language,
    )

    print(report)

def main_entry():
    """Entry point for console script."""
    main()

if __name__ == "__main__":
    main()
