"""Population Based Planning Maturity Self-Assessment (pbpMAF) - Streamlit app.

Run locally with:  streamlit run app.py
No data is stored: everything lives in the browser session and is cleared on
"Start over" or when the page is closed.
"""

from datetime import date
from html import escape
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

from pbpmaf.assessment import (
    missing_details,
    missing_ratings,
    priority_areas,
    ratings_table,
    step_counts,
)
from pbpmaf.charts import STEP_COLOURS, heatmap_html, theme_chart
from pbpmaf.report import build_pdf
from pbpmaf.framework import (
    ASSESSMENT_LEVELS,
    CROSS_CUTTING_CONCEPTS,
    HEALTH_REGIONS,
    LOWER_MATURITY_STEPS,
    STEPS,
    THEMES,
    iter_subthemes,
)

FIGURE_3 = Path(__file__).parent / "assets" / "figure3_interconnected_themes.webp"
TOTAL_SUBTHEMES = sum(len(t["subthemes"]) for t in THEMES)

DETAIL_KEYS = {
    "organisation": "detail_organisation",
    "region": "detail_region",
    "team_function": "detail_team_function",
    "date": "detail_date",
    "assessor": "detail_assessor",
}

st.set_page_config(
    page_title="pbpMAF Self-Assessment",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
    /* Arial for text only. Icons (e.g. expander arrows) use Streamlit's icon font,
       so it must not be overridden or the icon names show as text. */
    html, body, .stApp, p, li, label, td, th, input, textarea, select,
    button p, [data-baseweb="select"] div, [data-testid="stExpander"] summary p {
        font-family: Arial, sans-serif !important;
    }
    h1, h2, h3, h4 { color: #006152 !important; font-family: Arial, sans-serif !important; }
    .pbp-banner {
        background: #006152; color: #FFFFFF; padding: 1.25rem 1.5rem;
        border-radius: 6px; margin-bottom: 1rem;
    }
    .pbp-banner h1 { color: #FFFFFF !important; margin: 0; padding: 0; font-size: 1.9rem; }
    .pbp-banner p { color: #FFFFFF; margin: 0.35rem 0 0 0; font-size: 1.05rem; }
    .pbp-steps { display: flex; flex-wrap: wrap; gap: 0.4rem; align-items: center; margin: 0.5rem 0 1rem 0; }
    .pbp-step {
        border: 2px solid #006152; color: #0C2950; background: #FFFFFF;
        border-radius: 4px; padding: 0.35rem 0.75rem; font-weight: bold;
    }
    .pbp-arrow { color: #006152; font-weight: bold; }
    .pbp-callout {
        border-left: 6px solid #006152; background: #E6EFEE; padding: 0.9rem 1.1rem;
        border-radius: 4px; margin: 0.5rem 0 1rem 0; color: #0C2950;
    }
    .pbp-tiles { display: grid; grid-template-columns: repeat(5, 1fr); gap: 4px; margin: 0.5rem 0 1rem 0; }
    .pbp-tile { border-radius: 4px; padding: 0.6rem 0.4rem; text-align: center; }
    .pbp-tile-n { font-size: 1.8rem; font-weight: bold; line-height: 1.1; }
    .pbp-tile-l { font-size: 0.85rem; }
    .pbp-hm-legend { display: flex; flex-wrap: wrap; gap: 4px; align-items: center; margin-bottom: 8px; font-size: 0.85rem; }
    .pbp-hm-key { font-weight: bold; padding: 0.2rem 0.6rem; border-radius: 3px; }
    .pbp-hm-wrap { overflow-x: auto; margin-bottom: 1rem; }
    table.pbp-hm { border-collapse: separate; border-spacing: 4px; width: 100%; min-width: 720px; table-layout: fixed; }
    table.pbp-hm th, table.pbp-hm td { border: none; border-radius: 3px; padding: 0.55rem 0.6rem; vertical-align: middle; }
    th.pbp-hm-theme { background: #006152; color: #FFFFFF; text-align: left; width: 19%; font-size: 0.95rem; }
    td.pbp-hm-empty { background: transparent; }
    .pbp-hm-sub { font-size: 0.85rem; line-height: 1.25; }
    .pbp-hm-step { font-weight: bold; font-size: 0.85rem; margin-top: 0.2rem; }
    table.pbp-bd { border-collapse: collapse; width: 100%; min-width: 640px; font-size: 0.92rem; }
    table.pbp-bd th { background: #006152; color: #FFFFFF; text-align: left; padding: 0.45rem 0.6rem; border: none; }
    table.pbp-bd td { border: none; border-bottom: 1px solid #B3D0CB; padding: 0.45rem 0.6rem; vertical-align: top; color: #0C2950; }
    table.pbp-bd td.pbp-bd-step { font-weight: bold; white-space: nowrap; }
    table.pbp-bd ul { margin: 0; padding-left: 1.1rem; }
    table.pbp-bd li { margin: 0; }
    .pbp-concept {
        display: inline-block; border: 1px solid #006152; background: #E6EFEE; color: #0C2950;
        border-radius: 4px; padding: 0.25rem 0.6rem; margin: 0.15rem 0.2rem 0.15rem 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def steps_scale_html() -> str:
    parts = []
    for i, step in enumerate(STEPS):
        if i:
            parts.append('<span class="pbp-arrow">&rarr;</span>')
        parts.append(f'<span class="pbp-step">{escape(step)}</span>')
    return f'<div class="pbp-steps">{"".join(parts)}</div>'


# Widget keys carry a version number so "Start over" can give every input a
# fresh, empty widget (deleting the old keys alone does not reset the browser).
st.session_state.setdefault("form_version", 0)


def wkey(name: str) -> str:
    return f"{name}_v{st.session_state['form_version']}"


def current_details() -> dict:
    return {field: st.session_state.get(wkey(key)) for field, key in DETAIL_KEYS.items()}


def current_ratings() -> dict:
    return {key: st.session_state.get(wkey(f"rating_{key}")) for key, *_ in iter_subthemes()}


@st.dialog("Start over")
def confirm_start_over():
    st.write(
        "This clears the organisation details and every rating in this session. "
        "Nothing is stored by the app, so cleared answers cannot be recovered. "
        "Download your results first if you need to keep them."
    )
    left, right = st.columns(2)
    if left.button("Yes, clear everything", type="primary", width="stretch"):
        next_version = st.session_state["form_version"] + 1
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.session_state["form_version"] = next_version
        st.rerun()
    if right.button("Cancel", width="stretch"):
        st.rerun()


def start_over_button(location: str):
    if st.button("Start over", key=wkey(f"start_over_{location}")):
        confirm_start_over()


# --------------------------------------------------------------------------- #
# Header
# --------------------------------------------------------------------------- #
st.markdown(
    """
    <div class="pbp-banner">
      <h1>Population Based Planning Maturity Self-Assessment</h1>
      <p>Population Based Planning Maturity Assessment Framework (pbpMAF)</p>
    </div>
    """,
    unsafe_allow_html=True,
)

TAB_LABELS = ["1. About this tool", "2. Complete the assessment", "3. Report"]


def go_to_tab(label: str):
    st.session_state["nav_tab"] = label
    st.session_state["scroll_to_top"] = True


def next_page_button(label: str, text: str):
    st.divider()
    st.button(text, type="primary", on_click=go_to_tab, args=(label,), key=wkey(f"next_{label}"))


tab_intro, tab_assess, tab_results = st.tabs(TAB_LABELS, key="nav_tab", on_change="rerun")

if st.session_state.pop("scroll_to_top", False):
    # After a "Next" button, bring the new tab into view from the top of the page.
    components.html(
        "<script>const main = window.parent.document.querySelector('[data-testid=\"stMain\"]');"
        "if (main) { main.scrollTo({top: 0}); } window.parent.scrollTo({top: 0});</script>",
        height=0,
    )

# --------------------------------------------------------------------------- #
# Front page
# --------------------------------------------------------------------------- #
with tab_intro:
    st.header("About this tool")
    st.write(
        "This is a self-assessment tool for teams involved in population based planning (PBP). "
        "It supports a team to reflect on its current level of maturity across eight themes of "
        "organisational capability, and to identify areas of lower maturity for regional "
        "discussion and action planning."
    )

    col_for, col_not = st.columns(2)
    with col_for:
        st.subheader("What this tool is for")
        st.markdown(
            "- A **self-assessment**, completed by the team itself.\n"
            "- A snapshot of maturity **at a point in time**.\n"
            "- Structured reflection and discussion within the team.\n"
            "- Identifying **areas of lower maturity** to inform regional discussion and "
            "action planning."
        )
    with col_not:
        st.subheader("What this tool is not for")
        st.markdown(
            "- It has **not been built or validated for comparing regions** against each other.\n"
            "- It is not suitable for comparing results **over time**, unless the **same people** "
            "complete the assessment each time.\n"
            "- It does not produce an overall score, ranking, weighting or prioritisation. "
            "There is no composite result.\n"
            "- It is not an external audit or a performance measure."
        )

    st.subheader("Who can use it")
    st.write(
        "The tool is flexible on the level at which it is applied. It can be completed at "
        + ", ".join(f"**{level}**" for level in ASSESSMENT_LEVELS[:-1])
        + f" or **{ASSESSMENT_LEVELS[-1]}** level. Record which team or level completed the "
        "assessment in the *Team / Function* field."
    )

    st.subheader("How to use the tool")
    st.markdown(
        "1. Read this page so everyone taking part understands what the tool is and is not for.\n"
        "2. Go to **2. Complete the assessment** and fill in the organisation details. "
        "Fields marked * are required.\n"
        f"3. For each of the {TOTAL_SUBTHEMES} subthemes, read the **characteristics of high "
        "maturity** and agree the step on the **Steps to Maturity** scale that best reflects "
        "where your team is now. All subthemes must be rated.\n"
        "4. Go to **3. Report** to see the report: a summary, a heat map, the priority areas for "
        "discussion and a detailed breakdown by theme.\n"
        "5. **Download the report (PDF)** before you close the page. The app does not store any data.\n"
        "6. Use **Start over** to clear all answers and begin a new assessment."
    )

    st.subheader("The framework")
    st.write(
        f"The framework is organised into **{len(THEMES)} themes** and **{TOTAL_SUBTHEMES} "
        "subthemes**. Each subtheme is described by its **characteristics of high maturity**, "
        "which describe what high maturity looks like in practice."
    )
    for theme in THEMES:
        with st.expander(theme["theme"]):
            for si, sub in enumerate(theme["subthemes"], start=1):
                st.markdown(f"**{si}. {sub['subtheme']}**")
                st.markdown("\n".join(f"- {c}" for c in sub["characteristics"]))

    st.subheader("Steps to Maturity")
    st.write(
        "Each subtheme is rated on the Steps to Maturity scale. The step names are intended "
        "to be used as they are, alongside the characteristics of high maturity for each subtheme."
    )
    st.markdown(steps_scale_html(), unsafe_allow_html=True)
    st.write(
        f"Subthemes rated **{LOWER_MATURITY_STEPS[0]}** or **{LOWER_MATURITY_STEPS[1]}** are "
        "identified as areas of lower maturity in the results."
    )

    st.subheader(
        "Interdependence of Themes and Cross-Cutting Concepts - Support for Co-ordinated Development"
    )
    text_col, fig_col = st.columns([1, 1.25])
    with text_col:
        st.markdown(
            "- The themes and subthemes are **highly interconnected** rather than independent "
            "areas of organisational capability. Development in one area frequently reinforces "
            "or enables maturity in others.\n"
            "- **Leadership and governance** functions as a **foundational capability** that "
            "supports development in all other areas.\n"
            "- There is a strong interrelationship between **infrastructure and information "
            "systems, resources, workforce capability, programme delivery, and monitoring and "
            "improving**. Mature information systems depend on data and digital infrastructure "
            "as well as analytical capability in the workforce, which relies on resources and "
            "workforce development. Access to data and high-quality analysis in turn underpins "
            "resource planning, evidence-informed decision making, and monitoring and improving.\n"
            "- Organisational maturity therefore develops through **co-ordinated development "
            "across multiple themes**."
        )
        st.markdown("**Cross-cutting concepts**")
        st.markdown(
            "".join(f'<span class="pbp-concept">{escape(c)}</span>' for c in CROSS_CUTTING_CONCEPTS),
            unsafe_allow_html=True,
        )
        st.write(
            "These concepts appear across multiple themes and subthemes. They are not assessed "
            "as standalone themes; instead they are embedded throughout the framework."
        )
    with fig_col:
        if FIGURE_3.exists():
            st.image(
                str(FIGURE_3),
                caption="Figure 3: Interconnected themes of organisational maturity",
                width="stretch",
            )

    st.subheader("Your data")
    st.markdown(
        '<div class="pbp-callout">No data is stored by this app. Your answers exist only in '
        "this browser session and are lost when you close or refresh the page, or select "
        "<b>Start over</b>. Download the report from the Report tab to keep a copy.</div>",
        unsafe_allow_html=True,
    )
    next_page_button(TAB_LABELS[1], "Next: Complete the assessment")

# --------------------------------------------------------------------------- #
# Assessment
# --------------------------------------------------------------------------- #
with tab_assess:
    st.header("Complete the assessment")

    with st.expander("Organisation details", expanded=True):
        c1, c2, c3 = st.columns(3)
        c1.text_input(
            "Organisation / Team name *",
            key=wkey(DETAIL_KEYS["organisation"]),
            placeholder="e.g. HSE Community Healthcare West",
        )
        c2.selectbox(
            "Health region *",
            HEALTH_REGIONS,
            index=None,
            key=wkey(DETAIL_KEYS["region"]),
            placeholder="Choose an option",
        )
        c3.text_input(
            "Team / Function *",
            key=wkey(DETAIL_KEYS["team_function"]),
            placeholder="e.g. Population Health and Wellbeing",
            help="Record which team or level completed the assessment, for example CHA, "
            "care group, network of care or PBP steering group.",
        )
        c4, c5 = st.columns(2)
        c4.date_input("Assessment date", value=date.today(), key=wkey(DETAIL_KEYS["date"]))
        c5.text_input("Assessor (name or role)", key=wkey(DETAIL_KEYS["assessor"]))

    st.write(
        "For each subtheme, read the characteristics of high maturity and select the step on "
        "the Steps to Maturity scale that best reflects where your team is now. "
        "All subthemes must be rated."
    )
    st.markdown(steps_scale_html(), unsafe_allow_html=True)

    progress_slot = st.empty()

    for ti, theme in enumerate(THEMES, start=1):
        with st.container(border=True):
            st.subheader(f"Theme {ti}: {theme['theme']}")
            for si, sub in enumerate(theme["subthemes"], start=1):
                st.markdown(f"#### {ti}.{si} {sub['subtheme']}")
                st.markdown("*Characteristics of high maturity*")
                st.markdown("\n".join(f"- {c}" for c in sub["characteristics"]))
                st.radio(
                    "Steps to Maturity",
                    STEPS,
                    index=None,
                    horizontal=True,
                    key=wkey(f"rating_t{ti}s{si}"),
                )
                if si < len(theme["subthemes"]):
                    st.divider()

    rated = TOTAL_SUBTHEMES - len(missing_ratings(current_ratings()))
    progress_slot.progress(
        rated / TOTAL_SUBTHEMES, text=f"{rated} of {TOTAL_SUBTHEMES} subthemes rated"
    )
    st.write(
        f"{rated} of {TOTAL_SUBTHEMES} subthemes rated. When all subthemes are rated and the "
        "required organisation details are complete, select **Next: View the report**."
    )
    next_page_button(TAB_LABELS[2], "Next: View the report")
    start_over_button("assessment")

# --------------------------------------------------------------------------- #
# Report
# --------------------------------------------------------------------------- #
def breakdown_html(rows, include_theme: bool) -> str:
    head = (["Theme"] if include_theme else []) + [
        "Subtheme", "Steps to Maturity", "Characteristics of high maturity"]
    body = []
    for _, row in rows.iterrows():
        fill, ink = STEP_COLOURS[row["Steps to Maturity"]]
        bullets = "".join(f"<li>{escape(c)}</li>" for c in row["Characteristics of high maturity"])
        cells = ([f"<td>{escape(row['Theme'])}</td>"] if include_theme else []) + [
            f"<td><b>{escape(row['Subtheme'])}</b></td>",
            f'<td class="pbp-bd-step" style="background:{fill};color:{ink}">'
            f"{escape(row['Steps to Maturity'])}</td>",
            f"<td><ul>{bullets}</ul></td>",
        ]
        body.append(f"<tr>{''.join(cells)}</tr>")
    header = "".join(f"<th>{h}</th>" for h in head)
    return (
        f'<div class="pbp-hm-wrap"><table class="pbp-bd"><thead><tr>{header}</tr></thead>'
        f"<tbody>{''.join(body)}</tbody></table></div>"
    )


def download_buttons(details: dict, ratings: dict, location: str):
    safe_name = "".join(
        ch if ch.isalnum() else "_" for ch in details["organisation"].strip()
    ).strip("_") or "report"
    stem = f"pbpMAF_self_assessment_{safe_name}_{details['date'] or date.today()}"
    left, _ = st.columns([1, 3])
    left.download_button(
        "Download report (PDF)",
        data=build_pdf(details, ratings),
        file_name=f"{stem}.pdf",
        mime="application/pdf",
        type="primary",
        width="stretch",
        key=wkey(f"pdf_{location}"),
    )


with tab_results:
    st.header("Self-assessment report")
    details = current_details()
    ratings = current_ratings()
    gaps_details = missing_details(details)
    gaps_ratings = missing_ratings(ratings)

    if gaps_details or gaps_ratings:
        st.warning(
            "The report is available once all required organisation details are complete and "
            "every subtheme has been rated. The following still need to be completed in "
            "**2. Complete the assessment**:"
        )
        if gaps_details:
            st.markdown("**Organisation details**")
            st.markdown("\n".join(f"- {label}" for label in gaps_details))
        if gaps_ratings:
            st.markdown(f"**Subthemes not yet rated ({len(gaps_ratings)})**")
            st.markdown("\n".join(f"- {theme}: {sub}" for theme, sub in gaps_ratings))
    else:
        table = ratings_table(ratings)
        groups = priority_areas(ratings)
        lower_total = sum(len(g) for _, g in groups)

        with st.container(border=True):
            d1, d2, d3 = st.columns(3)
            d1.markdown(f"**Organisation / Team name**  \n{escape(details['organisation'])}")
            d2.markdown(f"**Health region**  \n{escape(details['region'])}")
            d3.markdown(f"**Team / Function**  \n{escape(details['team_function'])}")
            d4, d5, _ = st.columns(3)
            d4.markdown(
                f"**Assessment date**  \n{details['date'].strftime('%d/%m/%Y') if details['date'] else 'Not recorded'}"
            )
            d5.markdown(f"**Assessor (name or role)**  \n{escape(details['assessor'] or 'Not recorded')}")
        download_buttons(details, ratings, "top")

        st.markdown(
            '<div class="pbp-callout"><b>Reading this report.</b> This is a self-assessment '
            "completed by the team at a point in time. It is not a score: there is no overall "
            "result, weighting or ranking. It has not been built or validated for comparing "
            "regions, or for comparing results over time unless the same people complete the "
            "assessment each time. The themes are interconnected, so areas of lower maturity are "
            "best considered together.</div>",
            unsafe_allow_html=True,
        )

        st.subheader("Summary")
        st.write(
            f"Number of the {TOTAL_SUBTHEMES} subthemes at each step on the Steps to Maturity "
            f"scale. {lower_total} rated {LOWER_MATURITY_STEPS[0]} or {LOWER_MATURITY_STEPS[1]} "
            "are identified as priority areas for discussion."
        )
        counts = step_counts(ratings)
        st.markdown(
            '<div class="pbp-tiles">'
            + "".join(
                f'<div class="pbp-tile" style="background:{STEP_COLOURS[step][0]};'
                f'color:{STEP_COLOURS[step][1]}"><div class="pbp-tile-n">{counts[step]}</div>'
                f'<div class="pbp-tile-l">{escape(step)}</div></div>'
                for step in STEPS
            )
            + "</div>",
            unsafe_allow_html=True,
        )

        st.subheader("Heat map")
        st.write("Every subtheme, by theme, coloured by its step on the Steps to Maturity scale.")
        st.markdown(heatmap_html(table), unsafe_allow_html=True)

        st.subheader("Priority areas for discussion")
        st.write(
            f"Subthemes rated **{LOWER_MATURITY_STEPS[0]}** are shown first, followed by those "
            f"rated **{LOWER_MATURITY_STEPS[1]}**. Within each group subthemes are listed in "
            "framework order; they are not weighted or ranked. Use these areas to inform regional "
            "discussion and action planning."
        )
        if not groups:
            st.info(
                f"No subthemes were rated {LOWER_MATURITY_STEPS[0]} or {LOWER_MATURITY_STEPS[1]}. "
                "Consider discussing subthemes rated Moderately as a next step."
            )
        for step, group in groups:
            st.markdown(f"#### Rated {step} ({len(group)})")
            st.markdown(breakdown_html(group, include_theme=True), unsafe_allow_html=True)

        st.subheader("Detailed breakdown by theme")
        for ti, theme in enumerate(THEMES, start=1):
            rows = table[table["Theme"] == theme["theme"]]
            theme_counts = rows["Steps to Maturity"].value_counts()
            with st.container(border=True):
                st.markdown(f"#### Theme {ti}: {theme['theme']}")
                st.caption(
                    "Subthemes at each step - "
                    + "; ".join(f"{s}: {theme_counts[s]}" for s in STEPS if s in theme_counts)
                )
                st.plotly_chart(
                    theme_chart(rows), width="stretch", config={"displayModeBar": False}
                )
                st.markdown(breakdown_html(rows, include_theme=False), unsafe_allow_html=True)

        st.subheader("Keep a copy")
        st.write(
            "The app does not store any data. Download the report now if you need to keep it."
        )
        download_buttons(details, ratings, "bottom")

    st.divider()
    start_over_button("results")
