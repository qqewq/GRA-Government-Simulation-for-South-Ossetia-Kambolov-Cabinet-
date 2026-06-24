"""Social stability agent."""

from gra_government.agents.base import BaseAgent, AgentReport
from gra_government.scenario.state_model import SimulationState
from gra_government.core.hierarchical_stability import PolicyVector
from typing import List

class SocialStabilityAgent(BaseAgent):
    """Simulated advisor tracking protest risk and public trust."""

    def __init__(self, llm_client=None):
        super().__init__("SocialStabilityAgent", "social_stability", llm_client)

    def evaluate_state(self, state: SimulationState) -> AgentReport:
        issues = []
        if state.social.protest_index > 70:
            issues.append("High protest risk")
        if state.social.trust_index < 30:
            issues.append("Critically low public trust")
        summary = (
            f"Social: protest index {state.social.protest_index}, "
            f"trust index {state.social.trust_index}. "
            + ("Alarming: " + "; ".join(issues) if issues else "Calm.")
        )
        return AgentReport(agent_name=self.name, domain=self.domain, summary=summary, priority_weight=0.25)

    def propose_actions(self, state: SimulationState, report: AgentReport) -> List[PolicyVector]:
        actions = []
        if state.social.protest_index > 70:
            actions.append(PolicyVector(dimensions={"dialogue_platforms": 0.5, "address_grievances": 0.6}))
        if state.social.trust_index < 30:
            actions.append(PolicyVector(dimensions={"transparency_reforms": 0.4, "anti_corruption": 0.5}))
        return actions
