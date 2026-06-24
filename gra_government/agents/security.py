"""Security domain agent."""

from gra_government.agents.base import BaseAgent, AgentReport
from gra_government.scenario.state_model import SimulationState
from gra_government.core.hierarchical_stability import PolicyVector
from typing import List

class SecurityAgent(BaseAgent):
    """Simulated advisor for internal and external security risks."""

    def __init__(self, llm_client=None):
        super().__init__("SecurityAgent", "security", llm_client)

    def evaluate_state(self, state: SimulationState) -> AgentReport:
        issues = []
        if state.security.military_risk > 50:
            issues.append("Elevated military threat")
        if state.security.crime_rate > 40:
            issues.append("High crime rate")
        summary = (
            f"Security: military risk {state.security.military_risk}, "
            f"crime {state.security.crime_rate}/100k. "
            + ("Threats: " + "; ".join(issues) if issues else "Stable.")
        )
        return AgentReport(agent_name=self.name, domain=self.domain, summary=summary, priority_weight=0.25)

    def propose_actions(self, state: SimulationState, report: AgentReport) -> List[PolicyVector]:
        actions = []
        if state.security.military_risk > 50:
            actions.append(PolicyVector(dimensions={"border_reinforcement": 0.4, "diplomatic_engagement": 0.6}))
        if state.security.crime_rate > 40:
            actions.append(PolicyVector(dimensions={"community_policing": 0.5, "youth_programs": 0.3}))
        return actions
