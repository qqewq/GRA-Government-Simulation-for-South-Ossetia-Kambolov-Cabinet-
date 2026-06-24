"""Media domain agent."""

from gra_government.agents.base import BaseAgent, AgentReport
from gra_government.scenario.state_model import SimulationState
from gra_government.core.hierarchical_stability import PolicyVector
from typing import List

class MediaAgent(BaseAgent):
    """Simulated advisor for media landscape and information resilience."""

    def __init__(self, llm_client=None):
        super().__init__("MediaAgent", "media", llm_client)

    def evaluate_state(self, state: SimulationState) -> AgentReport:
        issues = []
        if state.media.freedom_index < 40:
            issues.append("Press freedom restricted")
        if state.media.disinformation_risk > 60:
            issues.append("High disinformation risk")
        summary = (
            f"Media: freedom {state.media.freedom_index}, "
            f"disinfo risk {state.media.disinformation_risk}. "
            + ("Concerns: " + "; ".join(issues) if issues else "Functional.")
        )
        return AgentReport(agent_name=self.name, domain=self.domain, summary=summary, priority_weight=0.05)

    def propose_actions(self, state: SimulationState, report: AgentReport) -> List[PolicyVector]:
        actions = []
        if state.media.freedom_index < 40:
            actions.append(PolicyVector(dimensions={"media_law_reform": 0.4}))
        if state.media.disinformation_risk > 60:
            actions.append(PolicyVector(dimensions={"media_literacy_campaign": 0.5, "fact_checking_fund": 0.3}))
        return actions
