# GAIDS FlexiSAF Internship Tasks

Weekly tasks and final project completed during the **Generative AI & Data Science (GAIDS)** internship at [FlexiSAF](https://flexisaf.com/).

## Repo Structure

```
gaids_flexisaf_tasks/
├── 0-certificate/          # Program completion certificate
└── 1-beginner/              # Weekly beginner-track tasks
    ├── week-01/              # Rock, Paper, Scissors
    ├── week-02/              # Tic-Tac-Toe AI + sales data viz
    ├── week-03/              # Iris dataset analysis
    ├── week-04/              # Airline passenger data viz
    └── FIP/                  # Final Independent Project
```

## Weekly Tasks

| Week | Topic | Details |
|---|---|---|
| [Week 1](1-beginner/week-01) | Rock, Paper, Scissors | Terminal game with input validation and replayability |
| [Week 2](1-beginner/week-02) | Tic-Tac-Toe AI + Sales Data Viz | Minimax-based unbeatable AI; pandas/matplotlib sales analysis |
| [Week 3](1-beginner/week-03) | Iris Dataset Analysis | Descriptive stats and correlation analysis with pandas/numpy |
| [Week 4](1-beginner/week-04) | Airline Passenger Data Viz | pandas/matplotlib/seaborn visualizations ([demo video](https://www.loom.com/share/6a6f35cd5866466988236e7427a85455)) |

## Final Independent Project (FIP)

**[Student Performance & Attendance Analysis](1-beginner/FIP)**

An end-to-end data project built on a [Kaggle student performance dataset](https://www.kaggle.com/datasets/marvyaymanhalim/student-performance-and-attendance-dataset):

- Data cleaning across 5 raw CSVs (~12K students) — see the [cleaning brief](1-beginner/FIP/data/DATA_CLEANING_BRIEF.md)
- Documented Jupyter notebook (analysis, charts, findings)
- Interactive **Streamlit dashboard** for exploring the data
- Slide deck summarizing key findings (PDF + editable PPTX)

Quick start:
```bash
cd 1-beginner/FIP/dashboard_app
pip install -r requirements.txt
streamlit run app.py
```

## Certificate

Completion certificate for *Introduction to Generative AI & Data Science* is in [`0-certificate/`](0-certificate).

## Tech Stack

Python · pandas · numpy · matplotlib · seaborn · Plotly · Streamlit · Jupyter

## Author

Built by [@hxxisq](https://github.com/hxxisq) as part of the FlexiSAF GAIDS internship program.
