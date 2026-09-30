"""Charts for the pbpMAF results, using the HSE colour palette.

Each theme gets a dot chart showing where each subtheme sits on the Steps to
Maturity scale. No numbers are shown: the x axis is the step labels.
"""

import textwrap

import plotly.graph_objects as go

from .framework import LOWER_MATURITY_STEPS, STEPS

# HSE National Guideline: Visual Identity and Naming (primary + secondary palette).
HSE_GREEN = "#006152"
HSE_GREEN_30 = "#B3D0CB"
HSE_ORANGE = "#DF8234"
HSE_NAVY = "#0C2950"
HSE_GREY = "#9BAAB3"
FONT = "Arial, sans-serif"


def _wrap(text: str, width: int = 38) -> str:
    return "<br>".join(textwrap.wrap(text, width))


def theme_chart(theme_rows) -> go.Figure:
    """Dot chart for one theme. `theme_rows` is a slice of assessment.ratings_table()."""
    labels = [_wrap(s) for s in theme_rows["Subtheme"]]
    steps = list(theme_rows["Steps to Maturity"])

    fig = go.Figure()
    # Faint track across the whole scale so each dot is read against all five steps.
    for label in labels:
        fig.add_trace(
            go.Scatter(
                x=[STEPS[0], STEPS[-1]],
                y=[label, label],
                mode="lines",
                line=dict(color=HSE_GREEN_30, width=2),
                hoverinfo="skip",
                showlegend=False,
            )
        )

    groups = [
        ("Lower maturity (Not at all / To a Small Extent)", HSE_ORANGE, "diamond", True),
        ("Moderately or above", HSE_GREEN, "circle", False),
    ]
    for name, colour, symbol, is_lower in groups:
        xs, ys = [], []
        for label, step in zip(labels, steps):
            if (step in LOWER_MATURITY_STEPS) == is_lower:
                xs.append(step)
                ys.append(label)
        fig.add_trace(
            go.Scatter(
                x=xs,
                y=ys,
                mode="markers",
                name=name,
                marker=dict(
                    color=colour,
                    symbol=symbol,
                    size=16,
                    line=dict(color="#FFFFFF", width=2),
                ),
                hovertemplate="%{y}<br><b>%{x}</b><extra></extra>",
            )
        )

    fig.update_xaxes(
        type="category",
        categoryorder="array",
        categoryarray=STEPS,
        range=[-0.4, len(STEPS) - 0.6],
        showgrid=True,
        gridcolor="#E6EFEE",
        tickfont=dict(color=HSE_NAVY, size=13),
        fixedrange=True,
    )
    fig.update_yaxes(
        categoryorder="array",
        categoryarray=list(reversed(labels)),
        tickfont=dict(color=HSE_NAVY, size=13),
        showgrid=False,
        fixedrange=True,
    )
    fig.update_layout(
        height=100 + 58 * len(labels),
        margin=dict(l=10, r=20, t=10, b=10),
        font=dict(family=FONT, color=HSE_NAVY),
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FFFFFF",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0, font=dict(size=12)),
        hoverlabel=dict(font_family=FONT),
    )
    return fig


# Heat map colours for the Steps to Maturity: HSE orange (lower) through a neutral
# grey midpoint to HSE green (higher). Each cell also carries the step name, so the
# colour is never the only cue. (fill, text colour)
STEP_COLOURS = {
    "Not at all": ("#DF8234", HSE_NAVY),
    "To a Small Extent": ("#EFC09A", HSE_NAVY),
    "Moderately": ("#E1E6E9", HSE_NAVY),
    "To a Large Extent": ("#80B0A9", HSE_NAVY),
    "Full": (HSE_GREEN, "#FFFFFF"),
}


def heatmap_html(table) -> str:
    """Heat map of every subtheme, one row per theme, as an HTML table.

    `table` is assessment.ratings_table(). Cells show the subtheme and its step.
    """
    from html import escape

    max_subthemes = table.groupby("Theme", sort=False).size().max()
    rows = []
    for theme, group in table.groupby("Theme", sort=False):
        cells = [f'<th class="pbp-hm-theme">{escape(theme)}</th>']
        for _, row in group.iterrows():
            fill, ink = STEP_COLOURS[row["Steps to Maturity"]]
            cells.append(
                f'<td style="background:{fill};color:{ink}">'
                f'<div class="pbp-hm-sub">{escape(row["Subtheme"])}</div>'
                f'<div class="pbp-hm-step">{escape(row["Steps to Maturity"])}</div></td>'
            )
        cells.extend('<td class="pbp-hm-empty"></td>' for _ in range(max_subthemes - len(group)))
        rows.append(f"<tr>{''.join(cells)}</tr>")

    legend = "".join(
        f'<span class="pbp-hm-key" style="background:{fill};color:{ink}">{escape(step)}</span>'
        for step, (fill, ink) in STEP_COLOURS.items()
    )
    return (
        f'<div class="pbp-hm-legend"><b>Key:</b>{legend}</div>'
        f'<div class="pbp-hm-wrap"><table class="pbp-hm">{"".join(rows)}</table></div>'
    )
