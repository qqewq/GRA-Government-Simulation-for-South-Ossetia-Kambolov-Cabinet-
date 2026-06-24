"""
Cabinet Orchestrator.

Coordinates domain agents, computes stability, resolves conflicts,
and produces a unified cabinet report.
"""

from typing import List, Dict, Optional
import logging

from gra_government.agents.base import BaseAgent, AgentReport
from gra_government.scenario.state_model import SimulationState
from gra_government.core.hierarchical_stability import (
    PolicyVector,
    StabilityScore,
    compute_stability_score,
    combine_recommendations,
)
from gra_government.core.asi_metric_space import asi_distance
from gra_government.core.subject_swap import swap_perspective

logger = logging.getLogger(__name__)

class CabinetOrchestrator:
    """
    Main orchestrator that mimics a government cabinet.
    It runs evaluation cycles, aggregates agent proposals,
    and computes a synthetic stability score.
    """

    def __init__(self, agents: List[BaseAgent], perspective: str = "government"):
        """
        Args:
            agents: list of instantiated domain agents.
            perspective: initial stakeholder perspective (see subject_swap).
        """
        self.agents = {a.domain: a for a in agents}
        self.perspective = perspective
        self.default_weights = self._default_domain_weights()

    def _default_domain_weights(self) -> Dict[str, float]:
        """Return domain weights from the current perspective (via subject_swap)."""
        # Hard‑coded base weights, then adjust with perspective
        base = {
            "economy": 0.2,
            "demography": 0.1,
            "infrastructure": 0.15,
            "social_stability": 0.25,
            "security": 0.25,
            "media": 0.05,
        }
        return swap_perspective(base, self.perspective, blend=1.0)

    def evaluate_all(self, state: SimulationState) -> Dict[str, AgentReport]:
        """Run evaluate_state for each agent and collect reports."""
        reports = {}
        for domain, agent in self.agents.items():
            try:
                report = agent.evaluate_state(state)
                reports[domain] = report
                logger.debug(f"Agent {domain} report: {report.summary[:100]}...")
            except Exception as e:
                logger.error(f"Error evaluating agent {domain}: {e}")
                reports[domain] = AgentReport(
                    agent_name=agent.name,
                    domain=domain,
                    summary=f"Evaluation failed: {e}",
                )
        return reports

    def collect_policy_proposals(
        self, state: SimulationState, reports: Dict[str, AgentReport]
    ) -> Dict[str, List[PolicyVector]]:
        """Ask each agent to propose actions based on its evaluation."""
        proposals = {}
        for domain, agent in self.agents.items():
            try:
                props = agent.propose_actions(state, reports[domain])
                proposals[domain] = props
            except Exception as e:
                logger.error(f"Error proposing actions for {domain}: {e}")
                proposals[domain] = []
        return proposals

    def aggregate_policy(
        self, proposals: Dict[str, List[PolicyVector]]
    ) -> PolicyVector:
        """Combine all proposed actions into a single cabinet policy vector."""
        weighted_proposals = []
        for domain, prop_list in proposals.items():
            weight = self.default_weights.get(domain, 0.0)
            # If multiple actions per domain, average them first (simple approach)
            if prop_list:
                avg_vec = PolicyVector(dimensions={})
                for p in prop_list:
                    for dim, val in p.dimensions.items():
                        avg_vec.dimensions[dim] = avg_vec.dimensions.get(dim, 0.0) + val
                n = len(prop_list)
                for dim in avg_vec.dimensions:
                    avg_vec.dimensions[dim] /= n
                weighted_proposals.append((domain, avg_vec, weight))
        return combine_recommendations(weighted_proposals)

    def run_cycle(self, state: SimulationState) -> Dict:
        """
        Run one complete advisory cycle:
        evaluate, propose, aggregate, compute stability.
        Returns a dictionary with all outputs.
        """
        reports = self.evaluate_all(state)
        proposals = self.collect_policy_proposals(state, reports)
        cabinet_policy = self.aggregate_policy(proposals)

        # Compute stability using agent policy proposals (domain-level summary)
        # For simplicity, pick the first proposal from each domain as representative
        domain_policies: Dict[str, PolicyVector] = {}
        for domain, prop_list in proposals.items():
            if prop_list:
                domain_policies[domain] = prop_list[0]  # pick first

        stability = compute_stability_score(domain_policies, self.default_weights)

        return {
            "reports": reports,
            "proposals": proposals,
            "cabinet_policy": cabinet_policy,
            "stability": stability,
        }
