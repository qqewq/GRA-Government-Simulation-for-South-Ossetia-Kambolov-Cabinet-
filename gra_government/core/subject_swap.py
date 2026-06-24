"""
Subject swap tools.

Allows swapping perspectives between different stakeholders
(e.g., government, population, external actors) by remapping
weights and priorities.

This is a placeholder; in the full GRA ecosystem SubjectSwap
repos contain deeper mathematical constructs.
"""

from typing import Dict

# Predefined perspective profiles
PERSPECTIVES: Dict[str, Dict[str, float]] = {
    "government": {
        "economy": 0.2,
        "demography": 0.1,
        "infrastructure": 0.15,
        "social_stability": 0.25,
        "security": 0.25,
        "media": 0.05,
    },
    "population": {
        "economy": 0.3,
        "demography": 0.2,
        "infrastructure": 0.2,
        "social_stability": 0.15,
        "security": 0.05,
        "media": 0.1,
    },
    "external": {
        "economy": 0.1,
        "demography": 0.05,
        "infrastructure": 0.1,
        "social_stability": 0.15,
        "security": 0.5,
        "media": 0.1,
    },
}


def swap_perspective(
    current_weights: Dict[str, float],
    target_perspective: str,
    blend: float = 1.0,
) -> Dict[str, float]:
    """
    Blend current weights with a predefined perspective profile.
    blend=1.0 fully adopts the new perspective, blend=0.0 keeps the original.
    """
    profile = PERSPECTIVES.get(target_perspective, {})
    new_weights = {}
    all_domains = set(current_weights.keys()) | set(profile.keys())
    for domain in all_domains:
        orig = current_weights.get(domain, 0.0)
        target = profile.get(domain, 0.0)
        new_weights[domain] = orig * (1 - blend) + target * blend
    # Normalize
    total = sum(new_weights.values())
    if total > 0:
        for d in new_weights:
            new_weights[d] /= total
    return new_weights
