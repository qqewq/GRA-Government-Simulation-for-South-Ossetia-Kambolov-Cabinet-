"""Base class for all domain advisory agents."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Optional, Dict

from gra_government.scenario.state_model import SimulationState
from gra_government.core.hierarchical_stability import PolicyVector


@dataclass
class AgentReport:
    """
    Report produced by an agent after evaluating the current state.
    Contains a natural language summary and a proposed policy vector.
    """
    agent_name: str
    domain: str
    summary: str = ""
    policy_proposals: List[PolicyVector] = field(default_factory=list)
    priority_weight: float = 1.0  # importance in stability aggregation


class BaseAgent(ABC):
    """
    Abstract base agent. Every domain agent must implement
    evaluate_state() and propose_actions(). 

    WARNING: All reasoning is purely hypothetical; agents are
    research artefacts and must not be used for real governance.
    """

    def __init__(self, name: str, domain: str, llm_client=None):
        self.name = name
        self.domain = domain
        self.llm_client = llm_client  # optional LLMClient instance

    @abstractmethod
    def evaluate_state(self, state: SimulationState) -> AgentReport:
        """Assess the current state from the agent's domain perspective."""
        ...

    @abstractmethod
    def propose_actions(self, state: SimulationState, report: AgentReport) -> List[PolicyVector]:
        """Propose policy vectors to address issues found during evaluation."""
        ...

    def __repr__(self):
        return f"<{self.__class__.__name__}({self.name}, domain={self.domain})>"
