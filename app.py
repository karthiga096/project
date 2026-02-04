import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF
import tempfile
import os

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Smart Marksheet Generator", page_icon="🎓")

# ---------------- SUBJECT DATA (UNCHANGED) ----------------
dept_sem_subjects = {
    "CSE": {
        "Semester 1": ["Maths I","Physics","C Programming","English","Graphics","Physics Lab"],
        "Semester 2": ["Maths II","Data Structures","Digital Logic","EVS","Communication","DS Lab"],
        "Semester 3": ["OOP","OS","DBMS","CN","Discrete Maths","OOP Lab"],
        "Semester 4": ["DAA","SE","Microprocessors","Web Tech","DBMS","DBMS Lab"],
        "Semester 5": ["ML","AI","Cloud Computing","Compiler Design","Elective I","ML Lab"],
        "Semester 6": ["Data Science","Big Data","IoT","Mobile Computing","Elective II","Mini Project"],
        "Semester 7": ["Deep Learning","Cyber Security","Elective III","Seminar","Internship","Research"],
        "Semester 8": ["Project Work","Review","Elective IV","Industrial Training","Viva","Presentation"]
    },
    "IT": {
        "Semester 1": ["Maths I","Physics","Python","English","Graphics","Physics Lab"],
        "Semester 2": ["Maths II","DS","Digital Fundamentals","EVS","Communication","Python Lab"],
        "Semester 3": ["OOP","OS","DBMS","CN","Discrete Maths","DBMS Lab"],
        "Semester 4": ["SE","Web Programming","Microprocessors","DAA","CN","Web Lab"],
        "Semester 5": ["ML","Cloud","Big Data","Data Mining","Elective I","ML Lab"],
        "Semester 6": ["AI","IoT","Mobile App Dev","Elective II","Mini Project","Case Study"],
        "Semester 7": ["Cyber Security","Blockchain","Elective III","Seminar","Internship","Research"],
        "Semester 8": ["Project Work","Review","Elective IV","Industrial Training","Viva","Presentation"]
    },
    "ECE": {
        "Semester 1": ["Maths I","Physics","Basic Electronics","English","Graphics","Physics Lab"],
        "Semester 2": ["Maths II","Circuit Theory","EDC","EVS","Communication","EDC Lab"],
        "Semester 3": ["Signals","Analog Circuits","Digital Electronics","EM Theory","DS","Analog Lab"],
        "Semester 4": ["Communication Systems","Control Systems","Microprocessors","LIC","Probability","Comm Lab"],
        "Semester 5": ["DSP","VLSI","Embedded Systems","Wireless Comm","Elective I","DSP Lab"],
        "Semester 6": ["Microwave","Optical Comm","IoT","Antennas","Elective II","Mini Project"],
        "Semester 7": ["ML for ECE","Satellite Comm","Elective III","Seminar","Internship","Research"],
        "Semester 8": ["Project Work","Review","Elective IV","Industrial Training","Viva","Presentation"]
    },
    "EEE": {
        "Semester 1": ["Maths I","Physics","Basic Electrical","English","Graphics","Physics Lab"],
        "Semester 2": ["Maths II","Circuit Theory","Machines I","EVS","Communication","Machines Lab"],
        "Semester 3": ["Machines II","Power Systems I","Control Systems","Digital Electronics","DS","Machines Lab"],
        "Semester 4": ["Power Systems II","Power Electronics","Measurements","Microprocessors","Probability","PE Lab"],
        "Semester 5": ["Renewable Energy","Smart Grid","Drives","Embedded","Elective I","Drives Lab"],
        "Semester 6": ["HV Engineering","Industrial Automation","IoT","Energy Mgmt","Elective II","Mini Project"],
        "Semester 7": ["ML for EEE","FACTS","Elective III","Seminar","Internship","Research"],
        "Semester 8": ["Project Work","Review","Elective IV","Industrial Training","Viva","Presentation"]
    }
}

# ---------------- GRADING ----------------
def grade(m):
    return "O" if m>=90 else "A+" if m>=80 else "A" if m>=70 else "B+" if m>=60 else "B" if m>=50 else "F"

def grade_point(m):
    return 10 if m>=90 else 9 if m>=80 else 8 if m>=70 else 7 if m>=60 else 6 if m>=50 else 0

# ---------------- SAVE TO DEPARTMENT EXCEL ----------------
def save_department_excel(dept, data):
    file_name = f"{dept}_records.xlsx"
    if os.path.exists(file_name):
        old = pd.read_excel(file_name)
        data = pd.concat([old, data], ignore_index=True)
    data.to_excel(file_name, index=False)
    return file_name

# ---------------- UI ----------------
st.title("🎓 Smart College Marksheet Generator")

dept = st.selectbox("Department", dept_sem_subjects.keys())
sem = st.selectbox("Semester", dept_sem_subjects[dept].keys())
name = st.text_input("Student Name")
roll = st.text_input("Roll Number")

subjects = dept_sem_subjects[dept][sem]
marks = [st.number_input(s,0,100,key=s) for s in subjects]

if st.button("📊 Generate Marksheet") and name and roll:
    grades = [grade(m) for m in marks]
    cgpa = round(sum(grade_point(m) for m in marks)/len(marks),2)
    percentage = round(sum(marks)/len(marks),2)
    result = "PASS" if min(marks)>=50 else "FAIL"

    df = pd.DataFrame({
        "Name": name,
        "Roll No": roll,
        "Department": dept,
        "Semester": sem,
        "Subject": subjects,
        "Marks": marks,
        "Grade": grades,
        "CGPA": cgpa,
        "Percentage": percentage,
        "Result": result
    })

    # -------- PERFORMANCE GRAPH --------
    st.subheader("📈 Performance Analysis")

    fig, ax = plt.subplots()
    ax.bar(subjects, marks)
    ax.axhline(50, linestyle="--")
    ax.set_ylabel("Marks")
    ax.set_title("Subject-wise Performance")
    plt.xticks(rotation=45)
    st.pyplot(fig)

    # -------- SAVE & DOWNLOAD --------
    dept_file = save_department_excel(dept, df)

    st.success(f"Data saved to {dept_file}")

    st.download_button(
        "📥 Download Department Excel",
        open(dept_file, "rb"),
        file_name=dept_file
    )
