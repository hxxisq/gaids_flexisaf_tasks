import io
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

import data_processing as dp

st.set_page_config(page_title="Student Performance Dashboard", layout="wide")


# ---------- cached data loading ----------

@st.cache_data
def get_data():
    master, students, attendance, homework, performance = dp.build_master_table()
    return master, students, attendance, homework, performance


master, students, attendance, homework, performance = get_data()

st.title("Student Performance Dashboard")
st.caption("Subject-wise performance, attendance, and homework analytics")


# ---------- sidebar filters ----------

st.sidebar.header("Filters")

grade_options = sorted(master["Grade_Level"].dropna().unique().tolist())
subject_options = sorted(master["Subject"].dropna().unique().tolist())

selected_grades = st.sidebar.multiselect("Grade / Class", grade_options, default=grade_options)
selected_subjects = st.sidebar.multiselect("Subject", subject_options, default=subject_options)

min_date = attendance["Date"].min()
max_date = attendance["Date"].max()
date_range = st.sidebar.date_input(
    "Attendance date range",
    value=(min_date.date(), max_date.date()),
    min_value=min_date.date(),
    max_value=max_date.date(),
)
if isinstance(date_range, tuple) and len(date_range) == 2:
    date_range = date_range
else:
    date_range = (min_date.date(), max_date.date())

filtered = master[
    master["Grade_Level"].isin(selected_grades) & master["Subject"].isin(selected_subjects)
]

if filtered.empty:
    st.warning("No data matches the selected filters.")
    st.stop()


# ---------- KPI row ----------

col1, col2, col3, col4 = st.columns(4)
col1.metric("Students (filtered)", f"{filtered['Student_ID'].nunique():,}")
col2.metric("Avg Exam Score", f"{filtered['Exam_Score'].mean():.1f}")
col3.metric("Avg Attendance", f"{filtered['Overall_Attendance_Rate_%'].mean():.1f}%")
col4.metric("Avg Homework Done", f"{filtered['Homework_Done_Rate_%'].mean():.1f}%")

st.divider()

tab1, tab2, tab3, tab4 = st.tabs(
    ["Subject Trends", "Attendance Heatmap", "Student Explorer", "Export"]
)


# ---------- Tab 1: Subject trends ----------

with tab1:
    indicators = dp.compute_indicators(filtered)

    c1, c2 = st.columns(2)

    with c1:
        st.subheader("Average Exam Score by Subject")
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.bar(indicators["Subject"], indicators["Mean_Score"], color="#4C72B0")
        ax.set_ylabel("Mean Exam Score")
        ax.set_ylim(0, 100)
        plt.xticks(rotation=30, ha="right")
        st.pyplot(fig)

    with c2:
        st.subheader("Exam Score Distribution")
        fig2, ax2 = plt.subplots(figsize=(6, 4))
        ax2.hist(filtered["Exam_Score"].dropna(), bins=20, color="#55A868", edgecolor="white")
        ax2.set_xlabel("Exam Score")
        ax2.set_ylabel("Count")
        st.pyplot(fig2)

    st.subheader("Indicators by Subject")
    st.dataframe(indicators, use_container_width=True)

    st.subheader("Attendance vs. Exam Score")
    fig3, ax3 = plt.subplots(figsize=(8, 4))
    ax3.scatter(filtered["Attendance_Rate_%"], filtered["Exam_Score"], alpha=0.2, s=10, color="#C44E52")
    ax3.set_xlabel("Attendance Rate (%)")
    ax3.set_ylabel("Exam Score")
    st.pyplot(fig3)


# ---------- Tab 2: Attendance heatmap ----------

with tab2:
    st.subheader("Attendance Rate: Grade vs. Subject")
    heatmap_data = dp.attendance_heatmap_data(attendance, students, date_range=date_range)
    heatmap_data = heatmap_data.loc[
        heatmap_data.index.intersection(selected_grades), heatmap_data.columns.intersection(selected_subjects)
    ]

    if heatmap_data.empty:
        st.info("No attendance data for the current filter selection.")
    else:
        fig4, ax4 = plt.subplots(figsize=(8, max(3, 0.5 * len(heatmap_data))))
        im = ax4.imshow(heatmap_data.values, cmap="RdYlGn", vmin=0, vmax=100, aspect="auto")
        ax4.set_xticks(range(len(heatmap_data.columns)))
        ax4.set_xticklabels(heatmap_data.columns, rotation=30, ha="right")
        ax4.set_yticks(range(len(heatmap_data.index)))
        ax4.set_yticklabels(heatmap_data.index)
        for i in range(heatmap_data.shape[0]):
            for j in range(heatmap_data.shape[1]):
                val = heatmap_data.values[i, j]
                if pd.notna(val):
                    ax4.text(j, i, f"{val:.0f}%", ha="center", va="center", fontsize=8)
        fig4.colorbar(im, ax=ax4, label="Attendance Rate (%)")
        st.pyplot(fig4)

    st.subheader("Monthly Attendance Trend")
    trend = dp.monthly_attendance_trend(attendance)
    fig5, ax5 = plt.subplots(figsize=(8, 3))
    ax5.plot(trend.index, trend.values, marker="o", color="#4C72B0")
    ax5.set_ylabel("Attendance Rate (%)")
    ax5.set_ylim(0, 100)
    st.pyplot(fig5)


# ---------- Tab 3: Student explorer ----------

with tab3:
    st.subheader("Per-student summary")
    student_summary = (
        filtered.groupby(["Student_ID", "Full_Name", "Grade_Level"])
        .agg(
            Avg_Exam_Score=("Exam_Score", "mean"),
            Avg_Attendance_Pct=("Overall_Attendance_Rate_%", "mean"),
            Avg_Homework_Done_Pct=("Homework_Done_Rate_%", "mean"),
        )
        .round(1)
        .reset_index()
        .sort_values("Avg_Exam_Score", ascending=False)
    )

    search = st.text_input("Search by student name or ID")
    if search:
        mask = (
            student_summary["Full_Name"].str.contains(search, case=False, na=False)
            | student_summary["Student_ID"].str.contains(search, case=False, na=False)
        )
        student_summary = student_summary[mask]

    st.dataframe(student_summary, use_container_width=True, height=500)


# ---------- Tab 4: Export ----------

with tab4:
    st.subheader("Export filtered data")

    csv_buffer = io.StringIO()
    filtered.to_csv(csv_buffer, index=False)
    st.download_button(
        "Download filtered data (CSV)",
        data=csv_buffer.getvalue(),
        file_name="filtered_student_performance.csv",
        mime="text/csv",
    )

    st.subheader("Export subject trend chart (PNG)")
    indicators = dp.compute_indicators(filtered)
    fig_export, ax_export = plt.subplots(figsize=(6, 4))
    ax_export.bar(indicators["Subject"], indicators["Mean_Score"], color="#4C72B0")
    ax_export.set_ylabel("Mean Exam Score")
    ax_export.set_ylim(0, 100)
    plt.xticks(rotation=30, ha="right")
    img_buffer = io.BytesIO()
    fig_export.savefig(img_buffer, format="png", bbox_inches="tight", dpi=150)
    st.download_button(
        "Download subject score chart (PNG)",
        data=img_buffer.getvalue(),
        file_name="subject_scores.png",
        mime="image/png",
    )
