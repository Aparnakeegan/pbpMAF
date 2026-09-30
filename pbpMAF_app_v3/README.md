# pbpMAF: Population Based Planning Maturity Self-Assessment

A Streamlit app for teams to self-assess population based planning (PBP) maturity
using the Population Based Planning Maturity Assessment Framework (pbpMAF).

- **8 themes, 27 subthemes**, each described by its characteristics of high maturity.
- Every subtheme is rated on the **Steps to Maturity** scale:
  Not at all, To a Small Extent, Moderately, To a Large Extent, Full.
- **No scoring, weighting or overall result.** The report identifies **priority areas for
  discussion**: subthemes rated Not at all, then those rated To a Small Extent, each group in
  framework order (not ranked), for regional discussion and action planning.
- The **Report** page shows a summary of how many subthemes sit at each step, a **heat map** of
  all 27 subthemes, the priority areas for discussion and a **detailed breakdown by theme**.
  The same report downloads as a **PDF**.
- A self-assessment **at a point in time**. It has not been built or validated for comparing
  regions, or for comparing over time unless the same people complete it each time.
- **No data is stored.** Answers exist only in the browser session. Users download the PDF
  report and can **Start over** at any time.
- Colours and font follow the HSE National Guideline: Visual Identity and Naming
  (HSE green `#006152`, secondary orange `#DF8234` and navy `#0C2950`, Arial; the PDF uses
  Helvetica, which is built into every PDF reader and matches Arial's proportions).

## Project layout

| Path | What it is |
|---|---|
| `app.py` | The Streamlit app (front page, assessment, report) |
| `pbpmaf/framework.py` | Framework wording: themes, subthemes, characteristics, Steps to Maturity, health regions. **Edit wording here.** |
| `pbpmaf/assessment.py` | Completion checks, priority areas for discussion, step counts |
| `pbpmaf/charts.py` | Heat map and per-theme charts, HSE colours for each step |
| `pbpmaf/report.py` | PDF report (reportlab) |
| `notebooks/pbpmaf_development.ipynb` | Jupyter notebook for developing and testing the logic and charts |
| `assets/figure3_interconnected_themes.webp` | Figure 3 infographic shown on the front page |
| `.streamlit/config.toml` | HSE colour theme |
| `requirements.txt` | Python packages needed by the app |

## Working in Jupyter

```bash
pip install -r requirements.txt jupyterlab
jupyter lab
```

Open `notebooks/pbpmaf_development.ipynb`. It imports the same code the app uses, so you can
change the framework, logic or charts, test them in the notebook, and the app picks up
the changes.

## Running the app on your computer

```bash
pip install -r requirements.txt
streamlit run app.py
```

The app opens in your browser at http://localhost:8501.

## Publishing for free on Streamlit Community Cloud

1. Make sure this code is pushed to GitHub, on the branch you want to publish (usually `main`).
2. Go to https://share.streamlit.io and sign in with your GitHub account.
3. Select **Create app**, then choose **Deploy a public app from GitHub**.
4. Fill in:
   - **Repository:** `Aparnakeegan/pbpMAF`
   - **Branch:** `main` (or the branch you want to publish)
   - **Main file path:** `app.py`
   - **App URL:** optionally choose a custom name, for example `pbpmaf`.
5. Select **Deploy**. The first build takes a few minutes.

Every time you push a change to that branch, the published app updates automatically.

Notes:

- Community Cloud can deploy from a private repository, and the app itself can be kept
  public or restricted to invited viewers in the app's **Share** settings.
- Apps on the free tier go to sleep after a period without visitors. The next visitor
  wakes it with one click.
- The app does not write any data to disk or to a database, so nothing entered by users
  is kept on Streamlit's servers after their session ends.
