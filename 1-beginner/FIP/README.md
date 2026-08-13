# Student Performance & Attendance Analysis

**Dataset:** [Student Performance and Attendance Dataset](https://www.kaggle.com/datasets/marvyaymanhalim/student-performance-and-attendance-dataset) — Marvy Ayman Halim (Kaggle)

## Deliverables

| Item | Location |
|---|---|
| Jupyter notebook (clean, documented) | [`notebook/student_performance_analysis.ipynb`](notebook/student_performance_analysis.ipynb) |
| Notebook — HTML export | [`notebook/student_performance_analysis.html`](notebook/student_performance_analysis.html) |
| Notebook — PDF export | [`notebook/student_performance_analysis.pdf`](notebook/student_performance_analysis.pdf) |
| Code (interactive dashboard) | [`dashboard_app/`](dashboard_app/) — `app.py`, `data_processing.py` |
| Raw data | [`dashboard_app/data/`](dashboard_app/data/) (also the dataset source, credited above) |
| Cleaned dataset | [`data/cleaned/student_performance_master_cleaned.csv`](data/cleaned/student_performance_master_cleaned.csv) |
| Data cleaning brief + source credit | [`data/DATA_CLEANING_BRIEF.md`](data/DATA_CLEANING_BRIEF.md) |
| Charts & insights | Notebook sections 6–8 (matplotlib + Plotly); also live in the dashboard app |
| Slide deck (PDF) | [`slides/student_performance_slides.pdf`](slides/student_performance_slides.pdf) |
| Slide deck (editable PPTX) | [`slides/student_performance_slides.pptx`](slides/student_performance_slides.pptx) |

> Model training/evaluation was confirmed optional for this submission and is not included.
> The slide deck substitutes "key findings" for "model results" accordingly.

## Quick start

**Notebook:**
```bash
pip install -r dashboard_app/requirements.txt jupyter nbformat plotly kaleido
jupyter notebook notebook/student_performance_analysis.ipynb
```

**Interactive dashboard:**
```bash
cd dashboard_app
pip install -r requirements.txt
streamlit run app.py
```

## Summary

- **Problem:** attendance, homework, and exam data live in separate files, making it hard
  to see how they relate.
- **Approach:** clean each source file (inconsistent status text, mixed date formats,
  percent-sign grades), merge into one row-per-student-per-subject table, then compute
  per-subject indicators (mean, variance, correlation with attendance/homework) and
  visualize the results.
- **Finding:** scores are consistent across subjects (~75 average); attendance and
  homework completion show essentially no correlation with exam score. This is consistent
  with the dataset being synthetically generated rather than real classroom outcomes —
  see `data/DATA_CLEANING_BRIEF.md` for details.
- **No gender field exists** in the source data — grade level is used as the class/grouping
  variable throughout instead.
