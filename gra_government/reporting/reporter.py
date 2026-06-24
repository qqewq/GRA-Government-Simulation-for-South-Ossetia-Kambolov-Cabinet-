"""
Report generator.

Produces summaries in Russian or English for a hypothetical leader.
"""

from typing import Dict, Any
from gra_government.scenario.state_model import SimulationState
from gra_government.core.hierarchical_stability import PolicyVector, StabilityScore

def generate_report(
    state: SimulationState,
    cabinet_policy: PolicyVector,
    stability: StabilityScore,
    language: str = "ru",
) -> str:
    """
    Generate a human-readable report for the hypothetical leader.
    language: 'ru' for Russian, 'en' for English.
    """
    if language == "ru":
        return _report_ru(state, cabinet_policy, stability)
    else:
        return _report_en(state, cabinet_policy, stability)

def _report_ru(state: SimulationState, policy: PolicyVector, stability: StabilityScore) -> str:
    lines = [
        "══════════════════════════════════════════",
        "  ИМИТАЦИОННЫЙ ОТЧЁТ КАБИНЕТА МИНИСТРОВ",
        "  Южная Осетия – система «Камболов»",
        "  (исключительно для исследовательских целей)",
        "══════════════════════════════════════════",
        "",
        "Состояние системы:",
        f"  ВВП индекс:           {state.economy.gdp_index:.1f}",
        f"  Безработица:          {state.economy.unemployment:.1f}%",
        f"  Зависимость бюджета:  {state.economy.budget_dependency:.2f}",
        f"  Население (тыс.):     {state.demography.population:.1f}",
        f"  Миграция:             {state.demography.net_migration:.0f} чел/год",
        f"  Энергетика:           {state.infrastructure.energy_index:.1f}",
        f"  Дороги:               {state.infrastructure.road_quality:.1f}",
        f"  Жильё:                {state.infrastructure.housing_index:.1f}",
        f"  Протестный индекс:    {state.social.protest_index:.1f}",
        f"  Доверие институтам:   {state.social.trust_index:.1f}",
        f"  Военная угроза:       {state.security.military_risk:.1f}",
        f"  Преступность:         {state.security.crime_rate:.1f}/100k",
        f"  Свобода СМИ:          {state.media.freedom_index:.1f}",
        f"  Риск дезинформации:   {state.media.disinformation_risk:.1f}",
        "",
        "Выработанная политика (вектор):",
    ]
    if policy.dimensions:
        for dim, val in policy.dimensions.items():
            lines.append(f"  • {dim}: {val:+.2f}")
    else:
        lines.append("  (нет предложений)")
    lines.extend([
        "",
        f"Интегральная оценка устойчивости: {stability.value:.3f}",
        "",
        "Рекомендация: продолжить мониторинг и корректировку.",
        "══════════════════════════════════════════",
    ])
    return "\n".join(lines)

def _report_en(state: SimulationState, policy: PolicyVector, stability: StabilityScore) -> str:
    lines = [
        "==========================================",
        "  SIMULATED CABINET REPORT",
        "  South Ossetia – Kambolov System",
        "  (for research purposes only)",
        "==========================================",
        "",
        "System state:",
        f"  GDP index:            {state.economy.gdp_index:.1f}",
        f"  Unemployment:         {state.economy.unemployment:.1f}%",
        f"  Budget dependency:    {state.economy.budget_dependency:.2f}",
        f"  Population (k):       {state.demography.population:.1f}",
        f"  Net migration:        {state.demography.net_migration:.0f}/year",
        f"  Energy:               {state.infrastructure.energy_index:.1f}",
        f"  Roads:                {state.infrastructure.road_quality:.1f}",
        f"  Housing:              {state.infrastructure.housing_index:.1f}",
        f"  Protest index:        {state.social.protest_index:.1f}",
        f"  Trust in institutions:{state.social.trust_index:.1f}",
        f"  Military risk:        {state.security.military_risk:.1f}",
        f"  Crime rate:           {state.security.crime_rate:.1f}/100k",
        f"  Press freedom:        {state.media.freedom_index:.1f}",
        f"  Disinformation risk:  {state.media.disinformation_risk:.1f}",
        "",
        "Proposed policy vector:",
    ]
    if policy.dimensions:
        for dim, val in policy.dimensions.items():
            lines.append(f"  • {dim}: {val:+.2f}")
    else:
        lines.append("  (no proposals)")
    lines.extend([
        "",
        f"Overall stability score: {stability.value:.3f}",
        "",
        "Recommendation: continue monitoring and adjustment.",
        "==========================================",
    ])
    return "\n".join(lines)
