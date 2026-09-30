"""Logic for completing and summarising a pbpMAF self-assessment.

There is deliberately no scoring, weighting, prioritisation or composite
result. Ratings are kept as Steps to Maturity labels; the output identifies
subthemes at lower maturity for regional discussion and action planning.
"""

import pandas as pd

from .framework import LOWER_MATURITY_STEPS, STEPS, iter_subthemes

REQUIRED_DETAILS = {
    "organisation": "Organisation / Team name",
    "region": "Health region",
    "team_function": "Team / Function",
}


def missing_details(details: dict) -> list[str]:
    """Labels of required organisation details that have not been filled in."""
    return [
        label
        for field, label in REQUIRED_DETAILS.items()
        if not str(details.get(field) or "").strip()
    ]


def missing_ratings(ratings: dict) -> list[tuple[str, str]]:
    """(theme, subtheme) pairs that have not been given a Steps to Maturity rating."""
    return [
        (theme, subtheme)
        for key, _, theme, _, subtheme, _ in iter_subthemes()
        if ratings.get(key) not in STEPS
    ]


def ratings_table(ratings: dict) -> pd.DataFrame:
    """One row per subtheme, in framework order, with its rating."""
    rows = []
    for key, tn, theme, sn, subtheme, characteristics in iter_subthemes():
        step = ratings.get(key)
        rows.append(
            {
                "Theme": theme,
                "Subtheme": f"{tn}.{sn} {subtheme}",
                "Steps to Maturity": step,
                "Lower maturity": step in LOWER_MATURITY_STEPS,
                "Characteristics of high maturity": characteristics,
            }
        )
    return pd.DataFrame(rows)


def lower_maturity_areas(ratings: dict) -> pd.DataFrame:
    """Subthemes rated at a lower-maturity step, kept in framework order (not ranked)."""
    table = ratings_table(ratings)
    return table[table["Lower maturity"]].reset_index(drop=True)


def step_counts(ratings: dict) -> dict:
    """Number of subthemes at each step, in scale order (a count, not a score)."""
    values = list(ratings.values())
    return {step: values.count(step) for step in STEPS}


def priority_areas(ratings: dict) -> list[tuple[str, pd.DataFrame]]:
    """Priority areas for discussion, grouped by step: Not at all, then To a Small Extent.

    Within each group subthemes stay in framework order. Nothing is weighted or
    ranked; groups with no subthemes are left out.
    """
    table = ratings_table(ratings)
    groups = []
    for step in LOWER_MATURITY_STEPS:
        group = table[table["Steps to Maturity"] == step].reset_index(drop=True)
        if not group.empty:
            groups.append((step, group))
    return groups
