"""
Simple simulation engine that updates the state based on applied policies.

This is a deterministic placeholder intended for research.
"""

from gra_government.scenario.state_model import SimulationState
from gra_government.core.hierarchical_stability import PolicyVector
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

def apply_policy_effects(state: SimulationState, policy: PolicyVector) -> SimulationState:
    """
    Naive update rules: each policy dimension tweaks relevant state fields
    by a small fraction. Used purely for demonstration.
    """
    # Deep copy would be better, but for simplicity we return a new object.
    new_state = SimulationState(
        economy=type(state.economy)(**state.economy.__dict__),
        demography=type(state.demography)(**state.demography.__dict__),
        infrastructure=type(state.infrastructure)(**state.infrastructure.__dict__),
        social=type(state.social)(**state.social.__dict__),
        security=type(state.security)(**state.security.__dict__),
        media=type(state.media)(**state.media.__dict__),
    )

    dims = policy.dimensions
    # Economy
    new_state.economy.gdp_index += dims.get("investment_incentives", 0) * 2.0
    new_state.economy.gdp_index += dims.get("tax_reduction", 0) * 1.5
    new_state.economy.unemployment -= dims.get("public_works_program", 0) * 1.0
    new_state.economy.unemployment -= dims.get("vocational_training", 0) * 0.5
    new_state.economy.budget_dependency -= dims.get("diversify_income", 0) * 0.05
    new_state.economy.budget_dependency -= dims.get("reduce_external_debt", 0) * 0.02

    # Demography
    new_state.demography.population_change += dims.get("child_support", 0) * 0.1
    new_state.demography.population_change += dims.get("maternity_capital", 0) * 0.1
    new_state.demography.net_migration += dims.get("return_programs", 0) * 10
    new_state.demography.net_migration += dims.get("diaspora_engagement", 0) * 5
    new_state.demography.dependency_ratio -= dims.get("pension_reform", 0) * 0.01
    new_state.demography.dependency_ratio -= dims.get("raise_retirement_age", 0) * 0.005

    # Infrastructure
    new_state.infrastructure.energy_index += dims.get("build_power_plants", 0) * 3
    new_state.infrastructure.energy_index += dims.get("renewable_investment", 0) * 1
    new_state.infrastructure.road_quality += dims.get("road_repair_program", 0) * 4
    new_state.infrastructure.housing_index += dims.get("social_housing", 0) * 2
    new_state.infrastructure.housing_index += dims.get("subsidised_mortgages", 0) * 1

    # Social
    new_state.social.protest_index -= dims.get("dialogue_platforms", 0) * 2
    new_state.social.protest_index -= dims.get("address_grievances", 0) * 3
    new_state.social.trust_index += dims.get("transparency_reforms", 0) * 2
    new_state.social.trust_index += dims.get("anti_corruption", 0) * 3

    # Security
    new_state.security.military_risk -= dims.get("diplomatic_engagement", 0) * 2
    new_state.security.military_risk -= dims.get("border_reinforcement", 0) * 1
    new_state.security.crime_rate -= dims.get("community_policing", 0) * 1.5
    new_state.security.crime_rate -= dims.get("youth_programs", 0) * 1

    # Media
    new_state.media.freedom_index += dims.get("media_law_reform", 0) * 3
    new_state.media.disinformation_risk -= dims.get("media_literacy_campaign", 0) * 2
    new_state.media.disinformation_risk -= dims.get("fact_checking_fund", 0) * 1

    # Clamp values to reasonable ranges (0–100 where applicable)
    for sector in ["economy", "demography", "infrastructure", "social", "security", "media"]:
        obj = getattr(new_state, sector)
        for field_name in obj.__dataclass_fields__:
            val = getattr(obj, field_name)
            # simplistic clamping for indices (assume 0-100)
            if field_name in ("population_change", "net_migration", "budget_dependency", "dependency_ratio", "crime_rate"):
                pass  # not clamped so simply
            else:
                if isinstance(val, (int, float)) and val != 0:
                    setattr(obj, field_name, max(0.0, min(100.0, val)))

    return new_state

def step(state: SimulationState, policy: PolicyVector) -> SimulationState:
    """Execute one simulation step by applying the policy."""
    return apply_policy_effects(state, policy)

def simulate(
    initial_state: SimulationState,
    policy_sequence: List[PolicyVector],
) -> SimulationState:
    """Run multiple steps in sequence."""
    state = initial_state
    for p in policy_sequence:
        state = step(state, p)
        logger.debug(f"Step completed: GDP index now {state.economy.gdp_index}")
    return state
