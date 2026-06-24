"""Economy domain agent for South Ossetia simulation."""

from gra_government.agents.base import BaseAgent, AgentReport
from gra_government.scenario.state_model import SimulationState
from gra_government.core.hierarchical_stability import PolicyVector
from typing import List

class EconomyAgent(BaseAgent):
    """Simulated advisor focusing on GDP, unemployment, budget dependency."""

    def __init__(self, llm_client=None):
        super().__init__(
            name="EconomyAgent",
            domain="economy",
            llm_client=llm_client,
        )

    def evaluate_state(self, state: SimulationState) -> AgentReport:
        """Analyse economic indicators."""
        # Hypothetical, rule‑based evaluation
        issues = []
        if state.economy.gdp_index < 70:
            issues.append("GDP index critically low")
        if state.economy.unemployment > 15:
            issues.append("Unemployment dangerously high")
        if state.economy.budget_dependency > 0.8:
            issues.append("Heavy reliance on external budget support")

        summary = (
            f"Economy analysis: GDP index {state.economy.gdp_index}, "
            f"unemployment {state.economy.unemployment}%, "
            f"budget dependency {state.economy.budget_dependency:.2f}. "
            + ("Critical: " + "; ".join(issues) if issues else "Stable.")
        )
        return AgentReport(
            agent_name=self.name,
            domain=self.domain,
            summary=summary,
            priority_weight=0.2,
        )

    def propose_actions(self, state: SimulationState, report: AgentReport) -> List[PolicyVector]:
        """Propose corrective economic policies."""
        # For simulation only, generate simplistic policy vectors
        actions = []
        if state.economy.gdp_index < 70:
            actions.append(PolicyVector(dimensions={
                "investment_incentives": 0.5,
                "tax_reduction": 0.3,
            }))
        if state.economy.unemployment > 15:
            actions.append(PolicyVector(dimensions={
                "public_works_program": 0.7,
                "vocational_training": 0.4,
            }))
        if state.economy.budget_dependency > 0.8:
            actions.append(PolicyVector(dimensions={
                "diversify_income": 0.6,
                "reduce_external_debt": 0.2,
            }))
        return actions
