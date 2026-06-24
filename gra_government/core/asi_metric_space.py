"""
ASI Metric Space concepts.

Defines a function to compute conceptual distance between two policy vectors
or scenario states. This is a placeholder for future GRA-ASI-Metric-Space
integration.
"""

from gra_government.core.hierarchical_stability import PolicyVector
import math
from typing import Dict


def asi_distance(a: PolicyVector, b: PolicyVector) -> float:
    """
    Compute a metric distance between two policy vectors.
    The metric space is constructed so that policies that are
    'resonant' (aligned) are closer, and divergent policies are farther.
    Currently Euclidean, but can be replaced by a GRA nullification metric.
    """
    all_dims = set(a.dimensions.keys()) | set(b.dimensions.keys())
    squared_sum = 0.0
    for dim in all_dims:
        va = a.dimensions.get(dim, 0.0)
        vb = b.dimensions.get(dim, 0.0)
        squared_sum += (va - vb) ** 2
    return math.sqrt(squared_sum)
