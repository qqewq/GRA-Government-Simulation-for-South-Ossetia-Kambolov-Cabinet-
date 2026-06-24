"""
GRA Hierarchical Stability primitives.

This module defines concepts that mirror the GRA philosophy:
stability nodes, policy vectors, aggregation, and resonance-like combination.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
import math

# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class PolicyVector:
    """
    A multi‑dimensional policy action.
    Each dimension represents an aspect (e.g., budget, regulation, etc.).
    Values are normalised roughly to [-1, 1] where negative means reduction,
    positive means increase relative to baseline.
    """
    dimensions: Dict[str, float] = field(default_factory=dict)

    def magnitude(self) -> float:
        return math.sqrt(sum(v**2 for v in self.dimensions.values()))


@dataclass
class StabilityScore:
    """
    Stability score for a particular agent or aggregated cabinet.
    Higher = more stable / coherent.
    """
    value: float
    breakdown: Dict[str, float] = field(default_factory=dict)  # domain -> contribution


@dataclass
class StabilityNode:
    """
    A node in the hierarchical stability tree.
    Can represent a domain agent, a cluster of agents, or the whole cabinet.
    """
    name: str
    weight: float = 1.0
    children: List["StabilityNode"] = field(default_factory=list)
    policy: Optional[PolicyVector] = None
    score: Optional[StabilityScore] = None


# ---------------------------------------------------------------------------
# Aggregation logic
# ---------------------------------------------------------------------------

def compute_stability_score(
    policies: Dict[str, PolicyVector],
    weights: Dict[str, float],
) -> StabilityScore:
    """
    Compute a synthetic stability score from a set of domain agent policies.

    The logic is intentionally simplistic; real GRA systems would use
    resonance/nullification operators. This serves as a placeholder.
    """
    if not policies:
        return StabilityScore(value=0.0)

    total_weight = sum(weights.values())
    if total_weight == 0:
        return StabilityScore(value=0.0)

    # Weighted sum of vector magnitudes as a crude stability metric.
    # In a true GRA system, alignment and resonance would be measured.
    weighted_sum = 0.0
    for domain, policy in policies.items():
        w = weights.get(domain, 0.0)
        weighted_sum += w * (1.0 - min(policy.magnitude() / math.sqrt(len(policy.dimensions)), 1.0))
    value = weighted_sum / total_weight
    return StabilityScore(value=value)


def combine_recommendations(
    agent_recommendations: List[Tuple[str, PolicyVector, float]],  # (agent_name, vector, weight)
) -> PolicyVector:
    """
    Combine multiple agent policy proposals into a single cabinet policy vector.
    Simple weighted average. In GRA, resonance or interference patterns would be used.
    """
    combined: Dict[str, float] = {}
    total_weight = 0.0
    for name, vec, w in agent_recommendations:
        total_weight += w
        for dim, val in vec.dimensions.items():
            combined[dim] = combined.get(dim, 0.0) + w * val
    if total_weight > 0:
        for dim in combined:
            combined[dim] /= total_weight
    return PolicyVector(dimensions=combined)
