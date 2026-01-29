import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Student Performance EDA", layout="wide")

# ---------- Load Data ----------
conn = sqlite3.connect("student_performance.db")
df = pd.read_sql("SELECT * FROM students", conn)
conn.close()

st.title("📊 Student Performance Analysis Dashboard")

# ---------- MS vs GP ----------
st.header("1️⃣ Pass Rate: MS vs GP")

school_pass = pd.crosstab(df["school"], df["pass_fail"])
st.dataframe(school_pass)

fig, ax = plt.subplots()
school_pass.plot(kind="bar", ax=ax)
plt.ylabel("Number of Students")
st.pyplot(fig)

# ---------- Scholarship ----------
st.header("2️⃣ Scholarship Distribution")

scholarship_counts = df["scholarship"].value_counts()
st.write(scholarship_counts)

fig, ax = plt.subplots()
scholarship_counts.plot(kind="pie", autopct="%1.1f%%", ax=ax)
st.pyplot(fig)

# ---------- Pass % by Scholarship ----------
st.header("3️⃣ Pass Percentage: Scholarship vs No Scholarship")

scholarship_pass = pd.crosstab(df["scholarship"], df["pass_fail"], normalize="index") * 100
st.dataframe(scholarship_pass)

fig, ax = plt.subplots()
scholarship_pass.plot(kind="bar", ax=ax)
plt.ylabel("Percentage")
st.pyplot(fig)

# ---------- Travel Time Impact ----------
st.header("4️⃣ Does Travel Time Impact Results?")

fig, ax = plt.subplots()
sns.boxplot(data=df, x="pass_fail", y="traveltime", ax=ax)
st.pyplot(fig)

st.info("Longer travel times show a tendency toward lower performance.")

# ---------- Absenteeism Impact ----------
st.header("5️⃣ Does Absenteeism Impact Results?")

fig, ax = plt.subplots()
sns.boxplot(data=df, x="pass_fail", y="absences", ax=ax)
st.pyplot(fig)

st.info("Students with higher absences are more likely to fail.")

# ---------- Study Time Impact ----------
st.header("6️⃣ Does Study Time Impact Results?")

fig, ax = plt.subplots()
sns.boxplot(data=df, x="pass_fail", y="studytime", ax=ax)
st.pyplot(fig)

st.success("Higher study time strongly correlates with passing.")
