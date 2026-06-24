"""Infrastructure domain agent."""

from gra_government.agents.base import BaseAgent, AgentReport
from gra_government.scenario.state_model import SimulationState
from gra_government.core.hierarchical_stability import PolicyVector
from typing import List

class InfrastructureAgent(BaseAgent):
    """Advisor for energy, roads, housing."""

    def __init__(self, llm_client=None):
        super().__init__("InfrastructureAgent", "infrastructure", llm_client)

    def evaluate_state(self, state: SimulationState) -> AgentReport:
        issues = []
        if state.infrastructure.energy_index < 50:
            issues.append("Energy capacity low")
        if state.infrastructure.road_quality < 40:
            issues.append("Road network poor")
        if state.infrastructure.housing_index < 50:
            issues.append("Housing shortage")
        summary = (
            f"Infrastructure: energy {state.infrastructure.energy_index}, "
            f"roads {state.infrastructure.road_quality}, "
            f"housing {state.infrastructure.housing_index}. "
            + ("Problems: " + "; ".join(issues) if issues else "Adequate.")
        )
        return AgentReport(agent_name=self.name, domain=self.domain, summary=summary, priority_weight=0.15)

    def propose_actions(self, state: SimulationState, report: AgentReport) -> List[PolicyVector]:
        actions = []
        if state.infrastructure.energy_index < 50:
            actions.append(PolicyVector(dimensions={"build_power_plants": 0.7, "renewable_investment": 0.3}))
        if state.infrastructure.road_quality < 40:
            actions.append(PolicyVector(dimensions={"road_repair_program": 0.6}))
        if state.infrastructure.housing_index < 50:
            actions.append(PolicyVector(dimensions={"social_housing": 0.5, "subsidised_mortgages": 0.3}))
        return actions
