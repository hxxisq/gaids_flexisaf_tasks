# Student Performance Dashboard

An interactive Streamlit dashboard for analyzing student performance, attendance,
and homework completion from CSV data.

## Setup

```bash
pip install -r requirements.txt
```

## Run

```bash
streamlit run app.py
```

Then open the URL Streamlit prints (usually `http://localhost:8501`).

## Files

- `app.py` — the Streamlit dashboard (filters, charts, tables, export)
- `data_processing.py` — data cleaning, merging, and indicator calculations
- `data/` — the five source CSVs (students, attendance, homework, performance,
  teacher-parent communication)

## What it does

- Cleans inconsistent raw data (mixed-case attendance statuses, `%` signs on
  grades, emoji-based homework status, mixed date formats)
- Merges students + performance + attendance + homework into one analysis table
- Computes per-subject mean/variance of exam scores and correlations between
  exam scores vs. attendance rate and vs. homework completion
- **Subject Trends tab**: bar chart of average score by subject, score
  distribution histogram, attendance-vs-score scatter plot, indicator table
- **Attendance Heatmap tab**: grade-level × subject attendance heatmap, plus a
  monthly attendance trend line
- **Student Explorer tab**: searchable per-student summary table
- **Export tab**: download the filtered dataset as CSV, or the subject-score
  chart as PNG
- **Filters** (sidebar): Grade/Class, Subject, attendance date range

## Notes on the data

- The source `students.csv` has no gender column, so the "filter by
  gender/class" requirement from the original brief uses `Grade_Level`
  instead.
- The dataset appears to be synthetic — correlations between attendance/
  homework and exam scores come out near zero, which is expected for
  randomly generated data rather than a bug in the analysis.
