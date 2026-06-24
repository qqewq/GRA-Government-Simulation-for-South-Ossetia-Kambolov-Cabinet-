"""
Simulation state model for South Ossetia.

All indicators are hypothetical and chosen for research purposes only.
"""

from dataclasses import dataclass, field


@dataclass
class EconomyState:
    gdp_index: float = 70.0          # composite index, 0–100
    unemployment: float = 12.0       # percentage
    budget_dependency: float = 0.75  # fraction of budget from external aid


@dataclass
class DemographyState:
    population: float = 53.0         # thousand people
    population_change: float = -0.3  # annual % change
    net_migration: float = -150.0    # persons/year
    dependency_ratio: float = 0.55   # dependents per working-age person


@dataclass
class InfrastructureState:
    energy_index: float = 55.0       # 0–100
    road_quality: float = 35.0       # 0–100
    housing_index: float = 45.0      # 0–100


@dataclass
class SocialState:
    protest_index: float = 60.0      # 0–100, higher = more unrest
    trust_index: float = 40.0        # 0–100, trust in institutions


@dataclass
class SecurityState:
    military_risk: float = 45.0      # 0–100, external threat level
    crime_rate: float = 35.0         # per 100k population


@dataclass
class MediaState:
    freedom_index: float = 50.0      # 0–100, press freedom
    disinformation_risk: float = 55.0 # 0–100


@dataclass
class SimulationState:
    """Top‑level state container."""
    economy: EconomyState = field(default_factory=EconomyState)
    demography: DemographyState = field(default_factory=DemographyState)
    infrastructure: InfrastructureState = field(default_factory=InfrastructureState)
    social: SocialState = field(default_factory=SocialState)
    security: SecurityState = field(default_factory=SecurityState)
    media: MediaState = field(default_factory=MediaState)

    @classmethod
    def default(cls) -> "SimulationState":
        return cls()
