# -*- coding: utf-8 -*-
"""
Created on Thu Jan 29 21:41:42 2026

@author: madun
"""
import streamlit as st
import pandas as pd
import sqlite3

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Student Performance Explorer",
    layout="wide"
)

# =========================
# SIDEBAR NAVIGATION
# =========================
st.sidebar.title("Navigation")
menu = st.sidebar.radio(
    "Go to:",
    [
        "Project Overview",
        "School Insights",
        "School Support Analysis",
        "Performance Factors",
        "Contact"
    ]
)

# =========================
# LOAD DATA
# =========================
@st.cache_data
def load_data():
    conn = sqlite3.connect("student_performance.db")
    students = pd.read_sql("SELECT * FROM students_clean", conn)
    conn.close()
    return students

students = load_data()

# =========================
# PROJECT OVERVIEW
# =========================
if menu == "Project Overview":
    st.title("🎓 Student Performance Analysis")

    st.write("""
    This dashboard explores factors affecting student performance
    using cleaned and transformed school data.
    """)

    # Overall metrics
    st.metric("Total Students", len(students))

    overall_pass_rate = (
        students["pass_fail"]
        .value_counts(normalize=True)
        .get("Pass", 0) * 100
    )
    st.metric("Overall Pass Rate", f"{overall_pass_rate:.1f}%")

    st.divider()

    # =========================
    # SCHOOL-LEVEL SUMMARY
    # =========================
    st.subheader("School Overview (GP vs MS)")

    # Total learners per school
    total_per_school = (
        students
        .groupby("school")
        .size()
        .rename("Total Learners")
    )

    # Pass percentage per school
    pass_pct_per_school = (
        students[students["pass_fail"] == "Pass"]
        .groupby("school")
        .size()
        .div(total_per_school) * 100
    ).rename("Pass %")

    # School support percentage per school (FIXED COLUMN)
    schoolsupport_pct_per_school = (
        students[students["schoolsupport"] == "Yes"]
        .groupby("school")
        .size()
        .div(total_per_school) * 100
    ).rename("School Support %")

    # Combine summary
    overview_table = pd.concat(
        [
            total_per_school,
            pass_pct_per_school.round(1),
            schoolsupport_pct_per_school.round(1)
        ],
        axis=1
    ).fillna(0)

    st.dataframe(overview_table)

    st.subheader("Percentage Comparison by School")
    st.bar_chart(
        overview_table[["Pass %", "School Support %"]]
    )

# =========================
# SCHOOL INSIGHTS
# =========================
elif menu == "School Insights":
    st.title("🏫 School Performance (MS vs GP)")

    school_counts = (
        students
        .groupby(["school", "pass_fail"])
        .size()
        .unstack(fill_value=0)
    )

    st.dataframe(school_counts)
    st.bar_chart(school_counts)

# =========================
# SCHOOL SUPPORT ANALYSIS
# =========================
elif menu == "School Support Analysis":
    st.title("🎓 School Support Impact")

    schoolsupport_counts = (
        students
        .groupby(["schoolsupport", "pass_fail"])
        .size()
        .unstack(fill_value=0)
    )

    schoolsupport_pct = (
        schoolsupport_counts
        .div(schoolsupport_counts.sum(axis=1), axis=0) * 100
    )

    st.dataframe(schoolsupport_pct.round(1))
    st.bar_chart(schoolsupport_pct)

# =========================
# PERFORMANCE FACTORS
# =========================
elif menu == "Performance Factors":
    st.title("📈 Performance Factors")

    factor = st.sidebar.selectbox(
        "Select a factor:",
        ["Travel Time", "Absences", "Study Time"]
    )

    if factor == "Travel Time":
        st.write("Average travel time by outcome")
        st.bar_chart(
            students.groupby("pass_fail")["traveltime"].mean()
        )

    elif factor == "Absences":
        st.write("Average absences by outcome")
        st.bar_chart(
            students.groupby("pass_fail")["absences"].mean()
        )

    elif factor == "Study Time":
        st.write("Average study time by outcome")
        st.bar_chart(
            students.groupby("pass_fail")["studytime"].mean()
        )

# =========================
# CONTACT
# =========================
elif menu == "Contact":
    st.title("📬 Contact")

    st.write("""
    **Author:** Xolile Maduna  
    **Course:** CSS 2026 – Data Visualization  
    **Stack:** Python | Pandas | SQLite | Streamlit
    """)
