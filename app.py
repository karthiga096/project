import streamlit as st
import numpy as np
from sklearn.linear_model import LinearRegression
from fpdf import FPDF
import tempfile
import matplotlib.pyplot as plt
import pandas as pd
import os

# ---------------- SUBJECT DATA ----------------
dept_sem_subjects = {
    "CSE": {
        "Semester 1": ["Maths I","Physics","C Programming","English","Graphics","Physics Lab"],
        "Semester 2": ["Maths II","Data Structures","Digital Logic","EVS","Communication","DS Lab"],
        "Semester 3": ["OOP","OS","DBMS","CN","Discrete Maths","OOP Lab"],
        "Semester 4": ["DAA","SE","Microprocessors","Web Tech","DBMS","DBMS Lab"],
        "Semester 5": ["ML","AI","Cloud Computing","Compiler Design","Elective I","ML Lab"],
        "Semester 6": ["Data Science","Big Data","IoT","Mobile Computing","Elective II","Mini Project"],
        "Semester 7": ["Deep Learning","Cyber Security","Elective III","Seminar","Internship","Research"],
        "Semester 8": ["Project Work","Project Review","Elective IV","Industrial Training","Viva","Presentation"]
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
    }
}

# ---------------- GRADE & CGPA ----------------
def grade(m):
    if m >= 90: return "A+",10,"Pass"
    elif m >= 80: return "A",9,"Pass"
    elif m >= 70: return "B+",8,"Pass"
    elif m >= 60: return "B",7,"Pass"
    elif m >= 50: return "C",6,"Pass"
    else: return "D",0,"Fail"

def calculate_cgpa(marks):
    return round(sum([grade(m)[1] for m in marks]) / len(marks), 2)

# ---------------- ML PERFORMANCE ----------------
def performance_trend(marks):
    X = np.arange(1,len(marks)+1).reshape(-1,1)
    y = np.array(marks)
    model = LinearRegression().fit(X,y)
    return "Improving 📈" if model.coef_[0] > 0 else "Needs Improvement 📉"

# ---------------- PDF GENERATOR ----------------
def generate_pdf(college, name, roll, dept, sem, subjects, marks, cgpa):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial","B",16)
    pdf.cell(0,10,college,ln=True,align="C")

    pdf.set_font("Arial","",12)
    pdf.cell(0,10,f"Student Name: {name}",ln=True)
    pdf.cell(0,10,f"Roll No: {roll}",ln=True)
    pdf.cell(0,10,f"Department: {dept}",ln=True)
    pdf.cell(0,10,f"Semester: {sem}",ln=True)
    pdf.ln(5)

    pdf.set_font("Arial","B",12)
    pdf.cell(80,8,"Subject",1)
    pdf.cell(30,8,"Marks",1)
    pdf.cell(30,8,"Grade",1)
    pdf.ln()

    pdf.set_font("Arial","",12)
    for s,m in zip(subjects,marks):
        pdf.cell(80,8,s,1)
        pdf.cell(30,8,str(m),1)
        pdf.cell(30,8,grade(m)[0],1)
        pdf.ln()

    pdf.ln(5)
    pdf.cell(0,10,f"CGPA: {cgpa}",ln=True)

    temp = tempfile.NamedTemporaryFile(delete=False,suffix=".pdf")
    pdf.output(temp.name)
    return temp.name

# ---------------- STREAMLIT UI ----------------
st.title("🎓 Smart College Marksheet Generator (Semester 1–8)")

college = st.text_input("College Name")
dept = st.selectbox("Department", dept_sem_subjects.keys())
sem = st.selectbox("Semester", dept_sem_subjects[dept].keys())
name = st.text_input("Student Name")
roll = st.text_input("Roll Number")

subjects = dept_sem_subjects[dept][sem]
marks = [st.number_input(sub, 0, 100) for sub in subjects]

if st.button("Generate Marksheet"):
    if college and name and roll:
        cgpa = calculate_cgpa(marks)
        trend = performance_trend(marks)

        st.subheader("📊 Marks Analysis")
        fig, ax = plt.subplots()
        ax.bar(subjects, marks)
        plt.xticks(rotation=45)
        st.pyplot(fig)

        st.success(f"CGPA: {cgpa} | Performance: {trend}")

        # -------- SAVE TO EXCEL --------
        data = {
            "College": college,
            "Name": name,
            "Roll": roll,
            "Department": dept,
            "Semester": sem,
            "CGPA": cgpa
        }
        for s,m in zip(subjects,marks):
            data[s] = m

        df = pd.DataFrame([data])
        excel_file = "student_records.xlsx"

        if os.path.exists(excel_file):
            old = pd.read_excel(excel_file)
            df = pd.concat([old,df],ignore_index=True)

        df.to_excel(excel_file,index=False)

        st.download_button(
            "📊 Download Excel Records",
            data=open(excel_file,"rb"),
            file_name="student_records.xlsx"
        )

        # -------- PDF DOWNLOAD --------
        pdf_path = generate_pdf(college,name,roll,dept,sem,subjects,marks,cgpa)
        st.download_button(
            "📄 Download Marksheet PDF",
            data=open(pdf_path,"rb"),
            file_name=f"{roll}_marksheet.pdf",
            mime="application/pdf"
        )
    else:
        st.error("Please fill all fields")
