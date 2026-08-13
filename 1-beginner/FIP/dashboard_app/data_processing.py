"""
Data loading, cleaning, and merging for the Student Performance Dashboard.
"""
import pandas as pd
import numpy as np
import re
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"


# ---------- helpers ----------

def _parse_date(series):
    """Parse dates that may come in mixed formats (YYYY-MM-DD or DD-MM-YYYY)."""
    return pd.to_datetime(series, errors="coerce", format="mixed", dayfirst=False)


def _clean_percent(series):
    """Turn '100%', '90', 90 into a clean float 0-100."""
    s = series.astype(str).str.strip().str.replace("%", "", regex=False)
    return pd.to_numeric(s, errors="coerce")


# ---------- loaders ----------

def load_students():
    df = pd.read_csv(DATA_DIR / "students.csv")
    df["Date_of_Birth"] = _parse_date(df["Date_of_Birth"])
    df["Grade_Level"] = df["Grade_Level"].astype(str).str.strip()
    return df


def load_attendance():
    df = pd.read_csv(DATA_DIR / "attendance.csv")
    df["Date"] = _parse_date(df["Date"])
    status = df["Attendance_Status"].astype(str).str.strip().str.lower()
    status_map = {
        "present": "Present",
        "absent": "Absent",
        "excused": "Excused",
        "late": "Late",
    }
    df["Attendance_Status"] = status.map(status_map).fillna(status.str.title())
    df["Subject"] = df["Subject"].astype(str).str.strip()
    return df


def load_homework():
    df = pd.read_csv(DATA_DIR / "homework.csv")
    df["Due_Date"] = _parse_date(df["Due_Date"])
    status = df["Status"].astype(str).str.strip()
    status_map = {
        "❌": "Not Done",
        "✅": "Done",
        "Done": "Done",
        "done": "Done",
    }
    df["Status"] = status.map(status_map).fillna(status)
    df["Guardian_Signature"] = (
        df["Guardian_Signature"].astype(str).str.strip().replace({"": "No", "nan": "No"})
    )
    df["Subject"] = df["Subject"].astype(str).str.strip()
    return df


def load_performance():
    df = pd.read_csv(DATA_DIR / "performance.csv")
    df["Exam_Score"] = pd.to_numeric(df["Exam_Score"], errors="coerce")
    df["Homework_Completion_%"] = _clean_percent(df["Homework_Completion_%"])
    df["Subject"] = df["Subject"].astype(str).str.strip()
    return df


def load_communication():
    df = pd.read_csv(DATA_DIR / "teacher_parent_communication.csv")
    df["Date"] = _parse_date(df["Date"])
    return df


# ---------- aggregation ----------

def attendance_rate_by_student(attendance_df):
    """% of 'Present' records per student (and per student+subject)."""
    att = attendance_df.copy()
    att["is_present"] = att["Attendance_Status"] == "Present"
    overall = (
        att.groupby("Student_ID")["is_present"].mean().mul(100).round(1)
        .rename("Attendance_Rate_%").reset_index()
    )
    by_subject = (
        att.groupby(["Student_ID", "Subject"])["is_present"].mean().mul(100).round(1)
        .rename("Attendance_Rate_%").reset_index()
    )
    return overall, by_subject


def homework_completion_by_student(homework_df):
    hw = homework_df.copy()
    hw["is_done"] = hw["Status"] == "Done"
    overall = (
        hw.groupby("Student_ID")["is_done"].mean().mul(100).round(1)
        .rename("Homework_Done_Rate_%").reset_index()
    )
    return overall


def build_master_table():
    """Merge everything into one row-per-(student, subject) analysis table."""
    students = load_students()
    attendance = load_attendance()
    homework = load_homework()
    performance = load_performance()

    att_overall, att_subject = attendance_rate_by_student(attendance)
    hw_overall = homework_completion_by_student(homework)

    # Average exam score per student+subject (some students may have multiple entries)
    perf_agg = (
        performance.groupby(["Student_ID", "Subject"])
        .agg(Exam_Score=("Exam_Score", "mean"),
             Homework_Completion_pct=("Homework_Completion_%", "mean"))
        .reset_index()
    )

    master = perf_agg.merge(students[["Student_ID", "Full_Name", "Grade_Level"]],
                             on="Student_ID", how="left")
    master = master.merge(att_subject, on=["Student_ID", "Subject"], how="left")
    master = master.merge(att_overall.rename(columns={"Attendance_Rate_%": "Overall_Attendance_Rate_%"}),
                           on="Student_ID", how="left")
    master = master.merge(hw_overall, on="Student_ID", how="left")

    return master, students, attendance, homework, performance


def compute_indicators(master_df):
    """Per-subject mean/variance of exam scores + correlations."""
    rows = []
    for subject, g in master_df.groupby("Subject"):
        mean_score = g["Exam_Score"].mean()
        var_score = g["Exam_Score"].var()
        corr_attendance = g["Attendance_Rate_%"].corr(g["Exam_Score"])
        corr_homework = g["Homework_Completion_pct"].corr(g["Exam_Score"])
        rows.append({
            "Subject": subject,
            "Mean_Score": round(mean_score, 2) if pd.notna(mean_score) else np.nan,
            "Variance": round(var_score, 2) if pd.notna(var_score) else np.nan,
            "Corr_Attendance_vs_Score": round(corr_attendance, 2) if pd.notna(corr_attendance) else np.nan,
            "Corr_Homework_vs_Score": round(corr_homework, 2) if pd.notna(corr_homework) else np.nan,
        })
    return pd.DataFrame(rows).sort_values("Subject").reset_index(drop=True)


def attendance_heatmap_data(attendance_df, students_df, date_range=None):
    """Pivot table: rows=Grade_Level, cols=Subject, values=avg attendance rate %."""
    att = attendance_df.merge(students_df[["Student_ID", "Grade_Level"]], on="Student_ID", how="left")
    if date_range:
        start, end = date_range
        att = att[(att["Date"] >= pd.Timestamp(start)) & (att["Date"] <= pd.Timestamp(end))]
    att["is_present"] = att["Attendance_Status"] == "Present"
    pivot = att.pivot_table(index="Grade_Level", columns="Subject", values="is_present", aggfunc="mean") * 100
    return pivot.round(1)


def monthly_attendance_trend(attendance_df):
    att = attendance_df.dropna(subset=["Date"]).copy()
    att["Month"] = att["Date"].dt.to_period("M").dt.to_timestamp()
    att["is_present"] = att["Attendance_Status"] == "Present"
    trend = att.groupby("Month")["is_present"].mean().mul(100).round(1)
    return trend


if __name__ == "__main__":
    # quick sanity check when run directly
    master, students, attendance, homework, performance = build_master_table()
    print("Master table shape:", master.shape)
    print(master.head())
    print("\nIndicators:")
    print(compute_indicators(master))
