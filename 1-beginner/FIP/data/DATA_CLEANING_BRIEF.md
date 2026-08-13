# Data Cleaning Brief

## Source

**Dataset:** [Student Performance and Attendance Dataset](https://www.kaggle.com/datasets/marvyaymanhalim/student-performance-and-attendance-dataset)
**Author:** Marvy Ayman Halim (Kaggle)

Five raw CSV files, ~12,157 students:
- `students.csv` — student roster (ID, name, grade level, date of birth)
- `attendance.csv` — ~365K daily attendance records by subject
- `homework.csv` — ~61K homework assignment records
- `performance.csv` — ~36K exam score / homework completion records
- `teacher_parent_communication.csv` — ~24K communication log entries

Raw files are included at `../dashboard_app/data/`. The cleaned, merged output of this
process is at `cleaned/student_performance_master_cleaned.csv`.

## Issues found and how they were resolved

| Issue | Fix |
|---|---|
| `Attendance_Status` mixed case and stray whitespace (`Present`, `PRESENT `, `excused`) | Stripped whitespace, lowercased, then mapped to a canonical set: `Present`, `Absent`, `Excused`, `Late` |
| `homework.Status` used emoji (`✅`/`❌`) instead of text | Mapped emoji/text variants to `Done` / `Not Done` |
| `Homework_Completion_%` mixed plain numbers and percent-signed strings (`90` vs `100%`) | Stripped `%` and cast to numeric |
| Dates in more than one format (`YYYY-MM-DD`, `DD-MM-YYYY`) | Parsed with pandas' mixed-format date inference, coercing unparseable values to `NaT` |
| `students.csv` has no gender column | Used `Grade_Level` as the class/grouping variable instead |
| Multiple performance records per student/subject | Aggregated with `mean()` when merging into the master table |

## Merge logic

1. Attendance rate per student (overall) and per student+subject, from `is_present` mean
2. Homework completion rate per student, from `is_done` mean
3. Performance records aggregated to one row per (student, subject)
4. All joined on `Student_ID` (and `Subject` where applicable) into one master table:
   one row per (student, subject) with exam score, attendance rate, and homework
   completion rate together

Full code is in `../notebook/student_performance_analysis.ipynb`, section 4.

## Known limitation

The dataset appears to be synthetically generated: attendance, homework completion, and
exam scores show essentially no correlation with each other (see notebook section 6),
which would be unusual in real classroom data. Treat any "insights" as illustrative of
the analysis method rather than real findings about student behavior.
