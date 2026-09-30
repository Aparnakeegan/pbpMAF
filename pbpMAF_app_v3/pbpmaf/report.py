"""PDF report for a completed pbpMAF self-assessment (reportlab).

Uses the HSE palette. Helvetica is used as the PDF font: it is built into every
PDF reader and is metrically the same as Arial.
"""

from datetime import date
from io import BytesIO
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from .assessment import priority_areas, ratings_table, step_counts
from .charts import HSE_GREEN, HSE_NAVY, HSE_ORANGE, STEP_COLOURS
from .framework import CROSS_CUTTING_CONCEPTS, LOWER_MATURITY_STEPS, STEPS, THEMES

GREEN = colors.HexColor(HSE_GREEN)
NAVY = colors.HexColor(HSE_NAVY)
ORANGE = colors.HexColor(HSE_ORANGE)
GREEN_TINT = colors.HexColor("#E6EFEE")
ORANGE_TINT = colors.HexColor("#FDF2EA")
RULE = colors.HexColor("#B3D0CB")

PAGE_W, PAGE_H = A4
MARGIN = 15 * mm
CONTENT_W = PAGE_W - 2 * MARGIN

TITLE = "Population Based Planning Maturity Self-Assessment"
SUBTITLE = "Population Based Planning Maturity Assessment Framework (pbpMAF)"


def _styles() -> dict:
    base = ParagraphStyle("base", fontName="Helvetica", fontSize=9.5, leading=13, textColor=NAVY)
    return {
        "body": base,
        "small": ParagraphStyle("small", parent=base, fontSize=8, leading=10.5),
        "cell": ParagraphStyle("cell", parent=base, fontSize=8, leading=10),
        "cell_bold": ParagraphStyle("cell_bold", parent=base, fontSize=8, leading=10, fontName="Helvetica-Bold"),
        "h1": ParagraphStyle("h1", parent=base, fontName="Helvetica-Bold", fontSize=15, leading=19,
                             textColor=GREEN, spaceBefore=4, spaceAfter=6),
        "h2": ParagraphStyle("h2", parent=base, fontName="Helvetica-Bold", fontSize=11.5, leading=15,
                             textColor=GREEN, spaceBefore=8, spaceAfter=4),
        "label": ParagraphStyle("label", parent=base, fontName="Helvetica-Bold", fontSize=8.5, leading=11),
        "tile_n": ParagraphStyle("tile_n", parent=base, fontName="Helvetica-Bold", fontSize=16,
                                 leading=19, alignment=TA_CENTER),
        "tile_l": ParagraphStyle("tile_l", parent=base, fontSize=7.5, leading=9.5, alignment=TA_CENTER),
    }


def _on_page(canvas, doc):
    canvas.saveState()
    if doc.page == 1:
        band_h = 26 * mm
        canvas.setFillColor(GREEN)
        canvas.rect(0, PAGE_H - band_h, PAGE_W, band_h, stroke=0, fill=1)
        canvas.setFillColor(colors.white)
        canvas.setFont("Helvetica-Bold", 16)
        canvas.drawString(MARGIN, PAGE_H - 13 * mm, TITLE)
        canvas.setFont("Helvetica", 10)
        canvas.drawString(MARGIN, PAGE_H - 19.5 * mm, SUBTITLE + " - Self-assessment report")
    else:
        canvas.setStrokeColor(GREEN)
        canvas.setLineWidth(1.5)
        canvas.line(MARGIN, PAGE_H - 11 * mm, PAGE_W - MARGIN, PAGE_H - 11 * mm)
        canvas.setFillColor(GREEN)
        canvas.setFont("Helvetica-Bold", 8)
        canvas.drawString(MARGIN, PAGE_H - 9.5 * mm, TITLE)
    canvas.setFillColor(NAVY)
    canvas.setFont("Helvetica", 7.5)
    canvas.drawString(
        MARGIN, 9 * mm,
        "Self-assessment at a point in time. Not validated for comparing regions. "
        "No data is stored by the tool.",
    )
    canvas.drawRightString(PAGE_W - MARGIN, 9 * mm, f"Page {doc.page}")
    canvas.restoreState()


def _step_cell(step: str, s: dict):
    fill, ink = STEP_COLOURS[step]
    style = ParagraphStyle("step", parent=s["cell_bold"], textColor=colors.HexColor(ink))
    return Paragraph(escape(step), style), colors.HexColor(fill)


def _bullets(items, s) -> Paragraph:
    return Paragraph("<br/>".join(f"&bull;&nbsp;{escape(c)}" for c in items), s["cell"])


def _details_table(details: dict, s: dict) -> Table:
    assessed = details.get("date")
    rows = [
        ("Organisation / Team name", details.get("organisation") or ""),
        ("Health region", details.get("region") or ""),
        ("Team / Function", details.get("team_function") or ""),
        ("Assessment date", assessed.strftime("%d/%m/%Y") if assessed else "Not recorded"),
        ("Assessor (name or role)", details.get("assessor") or "Not recorded"),
        ("Report generated", date.today().strftime("%d/%m/%Y")),
    ]
    data = [[Paragraph(escape(k), s["label"]), Paragraph(escape(str(v)), s["body"])] for k, v in rows]
    t = Table(data, colWidths=[48 * mm, CONTENT_W - 48 * mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), GREEN_TINT),
        ("LINEBELOW", (0, 0), (-1, -1), 0.5, RULE),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    return t


def _callout(text: str, s: dict, fill=GREEN_TINT, bar=GREEN) -> Table:
    t = Table([[Paragraph(text, s["body"])]], colWidths=[CONTENT_W])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), fill),
        ("LINEBEFORE", (0, 0), (0, -1), 4, bar),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    return t


def _summary_tiles(ratings: dict, s: dict) -> Table:
    counts = step_counts(ratings)
    cells, styles = [], []
    for i, step in enumerate(STEPS):
        fill, ink = STEP_COLOURS[step]
        ink_c = colors.HexColor(ink)
        cells.append([
            Paragraph(str(counts[step]), ParagraphStyle("n", parent=s["tile_n"], textColor=ink_c)),
            Paragraph(escape(step), ParagraphStyle("l", parent=s["tile_l"], textColor=ink_c)),
        ])
        styles.append(("BACKGROUND", (i, 0), (i, 0), colors.HexColor(fill)))
    t = Table([cells], colWidths=[CONTENT_W / len(STEPS)] * len(STEPS))
    t.setStyle(TableStyle(styles + [
        ("LINEAFTER", (0, 0), (-2, -1), 2, colors.white),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    return t


def _heatmap(table, s: dict) -> Table:
    max_subs = max(len(t["subthemes"]) for t in THEMES)
    theme_w = 34 * mm
    sub_w = (CONTENT_W - theme_w) / max_subs
    theme_style = ParagraphStyle("hm_theme", parent=s["cell_bold"], textColor=colors.white)
    data, style = [], [
        ("GRID", (0, 0), (-1, -1), 1.5, colors.white),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("BACKGROUND", (0, 0), (0, -1), GREEN),
    ]
    for r, (theme, group) in enumerate(table.groupby("Theme", sort=False)):
        row = [Paragraph(escape(theme), theme_style)]
        for c, (_, item) in enumerate(group.iterrows(), start=1):
            fill, ink = STEP_COLOURS[item["Steps to Maturity"]]
            cell_style = ParagraphStyle("hm", parent=s["cell"], fontSize=7.5, leading=9.5,
                                        textColor=colors.HexColor(ink))
            row.append(Paragraph(
                f"{escape(item['Subtheme'])}<br/><b>{escape(item['Steps to Maturity'])}</b>", cell_style
            ))
            style.append(("BACKGROUND", (c, r), (c, r), colors.HexColor(fill)))
        row.extend([""] * (max_subs + 1 - len(row)))
        data.append(row)
    t = Table(data, colWidths=[theme_w] + [sub_w] * max_subs)
    t.setStyle(TableStyle(style))
    return t


def _legend(s: dict) -> Table:
    """Compact colour key, deliberately not aligned with the heat map columns."""
    cells = [Paragraph("<b>Key:</b>", s["small"])]
    style = [
        ("LINEAFTER", (1, 0), (-2, -1), 2, colors.white),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]
    for i, step in enumerate(STEPS, start=1):
        fill, ink = STEP_COLOURS[step]
        cells.append(Paragraph(escape(step), ParagraphStyle(
            "lg", parent=s["tile_l"], fontName="Helvetica-Bold", textColor=colors.HexColor(ink))))
        style.append(("BACKGROUND", (i, 0), (i, 0), colors.HexColor(fill)))
    t = Table([cells], colWidths=[11 * mm] + [26 * mm] * len(STEPS), hAlign="LEFT")
    t.setStyle(TableStyle(style))
    return t


def _subtheme_table(rows, s: dict, include_theme: bool) -> Table:
    widths = [34 * mm, 42 * mm, 26 * mm] if include_theme else [52 * mm, 28 * mm]
    widths.append(CONTENT_W - sum(widths))
    header = (["Theme"] if include_theme else []) + [
        "Subtheme", "Steps to Maturity", "Characteristics of high maturity"]
    head_style = ParagraphStyle("th", parent=s["cell_bold"], textColor=colors.white)
    data = [[Paragraph(h, head_style) for h in header]]
    style = [
        ("BACKGROUND", (0, 0), (-1, 0), GREEN),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LINEBELOW", (0, 1), (-1, -1), 0.5, RULE),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]
    step_col = 2 if include_theme else 1
    for r, (_, row) in enumerate(rows.iterrows(), start=1):
        step_para, fill = _step_cell(row["Steps to Maturity"], s)
        cells = ([Paragraph(escape(row["Theme"]), s["cell"])] if include_theme else []) + [
            Paragraph(f"<b>{escape(row['Subtheme'])}</b>", s["cell"]),
            step_para,
            _bullets(row["Characteristics of high maturity"], s),
        ]
        data.append(cells)
        style.append(("BACKGROUND", (step_col, r), (step_col, r), fill))
    t = Table(data, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle(style))
    return t


def build_pdf(details: dict, ratings: dict) -> bytes:
    """Build the PDF report for a completed assessment and return its bytes."""
    s = _styles()
    table = ratings_table(ratings)
    groups = priority_areas(ratings)
    lower_total = sum(len(g) for _, g in groups)

    story = [
        Spacer(1, 16 * mm),
        Paragraph("Assessment details", s["h1"]),
        _details_table(details, s),
        Spacer(1, 5 * mm),
        _callout(
            "<b>Reading this report.</b> This is a self-assessment completed by the team at a point "
            "in time. It is not a score: there is no overall result, weighting or ranking. It has "
            "not been built or validated for comparing regions, or for comparing results over time "
            "unless the same people complete the assessment each time. The themes are "
            "interconnected, so areas of lower maturity are best considered together.",
            s,
        ),
        Spacer(1, 3 * mm),
        Paragraph("Summary", s["h2"]),
        Paragraph(
            f"Number of the {len(table)} subthemes at each step on the Steps to Maturity scale. "
            f"{lower_total} subtheme{'s' if lower_total != 1 else ''} rated "
            f"{LOWER_MATURITY_STEPS[0]} or {LOWER_MATURITY_STEPS[1]} "
            f"{'are' if lower_total != 1 else 'is'} identified as priority areas for discussion.",
            s["body"],
        ),
        Spacer(1, 3 * mm),
        _summary_tiles(ratings, s),
        Spacer(1, 5 * mm),
        _callout(
            "<b>Co-ordinated development.</b> The themes and subthemes are interconnected. "
            "Leadership and governance functions as a foundational capability that enables "
            "development in all other themes. Infrastructure and information systems, resources, "
            "workforce capability, programme delivery, and monitoring and improving are strongly "
            "interdependent. The cross-cutting concepts of "
            + ", ".join(c.lower() for c in CROSS_CUTTING_CONCEPTS[:-1])
            + f" and {CROSS_CUTTING_CONCEPTS[-1].lower()} are embedded throughout the framework.",
            s,
        ),
        Spacer(1, 3 * mm),
        Paragraph("Contents", s["h2"]),
        Paragraph(
            "1. Assessment details and summary<br/>"
            "2. Heat map of all subthemes<br/>"
            "3. Priority areas for discussion<br/>"
            "4. Detailed breakdown by theme",
            s["body"],
        ),
        PageBreak(),
        KeepTogether([
            Paragraph("Heat map", s["h1"]),
            Paragraph("Every subtheme, by theme, coloured by its step on the Steps to Maturity scale.",
                      s["body"]),
            Spacer(1, 2 * mm),
            _legend(s),
            Spacer(1, 2 * mm),
            _heatmap(table, s),
        ]),
        PageBreak(),
        Paragraph("Priority areas for discussion", s["h1"]),
        Paragraph(
            f"Subthemes rated {LOWER_MATURITY_STEPS[0]} are shown first, followed by those rated "
            f"{LOWER_MATURITY_STEPS[1]}. Within each group subthemes are listed in framework order; "
            "they are not weighted or ranked. Use these areas to inform regional discussion and "
            "action planning.",
            s["body"],
        ),
        Spacer(1, 3 * mm),
    ]
    if groups:
        for step, group in groups:
            story.append(Paragraph(f"Rated {escape(step)} ({len(group)})", s["h2"]))
            story.append(_subtheme_table(group, s, include_theme=True))
            story.append(Spacer(1, 3 * mm))
    else:
        story.append(_callout(
            f"No subthemes were rated {LOWER_MATURITY_STEPS[0]} or {LOWER_MATURITY_STEPS[1]}. "
            "Consider discussing subthemes rated Moderately as a next step.",
            s, fill=ORANGE_TINT, bar=ORANGE,
        ))


    story.append(PageBreak())
    story.append(Paragraph("Detailed breakdown by theme", s["h1"]))
    for ti, theme in enumerate(THEMES, start=1):
        rows = table[table["Theme"] == theme["theme"]]
        counts = rows["Steps to Maturity"].value_counts()
        at_steps = "; ".join(f"{step}: {counts[step]}" for step in STEPS if step in counts)
        story.append(KeepTogether([
            Paragraph(f"Theme {ti}: {escape(theme['theme'])}", s["h2"]),
            Paragraph(f"Subthemes at each step - {escape(at_steps)}", s["small"]),
            Spacer(1, 2 * mm),
            _subtheme_table(rows, s, include_theme=False),
        ]))
        story.append(Spacer(1, 3 * mm))

    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=A4, leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=16 * mm, bottomMargin=16 * mm,
        title=TITLE, subject="Self-assessment report", author=details.get("organisation") or "",
    )
    doc.build(story, onFirstPage=_on_page, onLaterPages=_on_page)
    return buffer.getvalue()
