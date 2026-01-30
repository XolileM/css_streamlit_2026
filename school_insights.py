"""
@author: madun

1. Read and clean school data
2. Create insights out of the data
3. Load cleaned data & insights into SQLite
"""

import pandas as pd
import numpy as np
import sqlite3

print("********** Pipeline started ***********")

# =========================
# 1. EXTRACT
# =========================
school_data = pd.read_csv("student_perfomance_data.csv")

print("********** Extract done ***************")

# =========================
# 2. TRANSFORM (CLEAN DATA)
# =========================

school_perfom_data = school_data[
    [
        "school", "sex", "age", "address", "famsize",
        "Mjob", "Fjob", "guardian", "traveltime",
        "studytime", "failures", "activities",
        "schoolsup", "absences", "G1", "G2", "G3"
    ]
]

# Rename columns for business meaning
school_perfom_data = school_perfom_data.rename(
    columns={"schoolsup": "schoolsupport"}
)

# Standardize column names
school_perfom_data.columns = (
    school_perfom_data.columns
    .str.lower()
    .str.strip()
)


# Handle missing values
school_perfom_data["traveltime"].fillna(
    school_perfom_data["traveltime"].median(), inplace=True
)
school_perfom_data["studytime"].fillna(
    school_perfom_data["studytime"].median(), inplace=True
)
school_perfom_data["absences"].fillna(
    school_perfom_data["absences"].median(), inplace=True
)

# =========================
# 3. FEATURE ENGINEERING
# =========================

# Final grade average
school_perfom_data["final_grade"] = (
    school_perfom_data["g1"] +
    school_perfom_data["g2"] +
    school_perfom_data["g3"]
) / 3

# Pass / Fail logic
school_perfom_data["pass_fail"] = np.where(
    school_perfom_data["final_grade"] >= 10, "Pass", "Fail"
)

print("********** Transformation done ********")

# =========================
# 4. CREATE INSIGHTS
# =========================

# 1. Pass count by school (MS vs GP)
ins_school_pass = pd.crosstab(
    school_perfom_data["school"],
    school_perfom_data["pass_fail"]
)

# 2. Scholarship distribution
ins_schoolsup = school_perfom_data["schoolsupport"].value_counts()

# 3. Pass percentage with vs without scholarship
ins_schoolsup_pass_pct = (
    pd.crosstab(
        school_perfom_data["schoolsupport"],
        school_perfom_data["pass_fail"],
        normalize="index"
    ) * 100
)

# 4. Travel time impact
ins_traveltime = school_perfom_data.groupby(
    ["traveltime", "pass_fail"]
).size().reset_index(name="count")

# 5. Absenteeism impact
ins_absences = school_perfom_data.groupby(
    ["pass_fail"]
)["absences"].mean().reset_index()

# 6. Study time impact
ins_studytime = school_perfom_data.groupby(
    ["pass_fail"]
)["studytime"].mean().reset_index()

print("********** Insights created ***********")

# =========================
# 5. LOAD (SQLite)
# =========================

conn = sqlite3.connect("student_performance.db")

# Load cleaned data
school_perfom_data.to_sql(
    "students_clean",
    conn,
    if_exists="replace",
    index=False
)

# Load insights
ins_school_pass.to_sql(
    "ins_school_pass", 
    conn,
    if_exists="replace"
)

ins_schoolsup.to_frame("count").to_sql(
    "ins_schoolsup",
    conn,
    if_exists="replace"
)

ins_schoolsup_pass_pct.to_sql(
    "ins_schoolsup_pass_pct",
    conn,
    if_exists="replace"
)

ins_traveltime.to_sql(
    "ins_traveltime",
    conn,
    if_exists="replace",
    index=False
)

ins_absences.to_sql(
    "ins_absences",
    conn,
    if_exists="replace",
    index=False
)

ins_studytime.to_sql(
    "ins_studytime",
    conn,
    if_exists="replace",
    index=False
)

conn.close()

print("********** Load complete **************")
print("********** Pipeline finished **********")


        
    
    
    
