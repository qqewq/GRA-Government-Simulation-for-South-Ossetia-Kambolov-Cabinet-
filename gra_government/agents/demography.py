"""Demography domain agent."""

from gra_government.agents.base import BaseAgent, AgentReport
from gra_government.scenario.state_model import SimulationState
from gra_government.core.hierarchical_stability import PolicyVector
from typing import List

class DemographyAgent(BaseAgent):
    """Simulated advisor focusing on population trends, migration, age structure."""

    def __init__(self, llm_client=None):
        super().__init__("DemographyAgent", "demography", llm_client)

    def evaluate_state(self, state: SimulationState) -> AgentReport:
        issues = []
        if state.demography.population_change < -0.5:
            issues.append("Population decline")
        if state.demography.net_migration < -100:
            issues.append("Significant emigration")
        if state.demography.dependency_ratio > 0.6:
            issues.append("High dependency ratio")
        summary = (
            f"Demography: pop {state.demography.population}k, "
            f"change {state.demography.population_change}%/year, "
            f"migration {state.demography.net_migration}/year, "
            f"dependency {state.demography.dependency_ratio:.2f}. "
            + ("Issues: " + "; ".join(issues) if issues else "Balanced.")
        )
        return AgentReport(agent_name=self.name, domain=self.domain, summary=summary, priority_weight=0.1)

    def propose_actions(self, state: SimulationState, report: AgentReport) -> List[PolicyVector]:
        actions = []
        if state.demography.population_change < -0.5:
            actions.append(PolicyVector(dimensions={"child_support": 0.5, "maternity_capital": 0.6}))
        if state.demography.net_migration < -100:
            actions.append(PolicyVector(dimensions={"return_programs": 0.4, "diaspora_engagement": 0.3}))
        if state.demography.dependency_ratio > 0.6:
            actions.append(PolicyVector(dimensions={"pension_reform": 0.2, "raise_retirement_age": 0.1}))
        return actions
