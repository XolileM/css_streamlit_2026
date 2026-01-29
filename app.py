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
        "Scholarship Analysis",
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
    This dashboard explores factors affecting student performance using
    cleaned and transformed school data.
    """)

    st.metric("Total Students", len(students))
    pass_rate = (
        students["pass_fail"].value_counts(normalize=True)["Pass"] * 100
    )
    st.metric("Overall Pass Rate", f"{pass_rate:.1f}%")

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
# SCHOLARSHIP ANALYSIS
# =========================
elif menu == "Scholarship Analysis":
    st.title("🎓 Scholarship Impact")

    scholarship_counts = (
        students
        .groupby(["scholarship", "pass_fail"])
        .size()
        .unstack(fill_value=0)
    )

    scholarship_pct = scholarship_counts.div(
        scholarship_counts.sum(axis=1), axis=0
    ) * 100

    st.dataframe(scholarship_pct.round(1))
    st.bar_chart(scholarship_pct)

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

