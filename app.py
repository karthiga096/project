import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF
import tempfile

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Smart Marksheet Generator",
    page_icon="🎓",
    layout="centered"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
body {
    background: linear-gradient(to right, #4facfe, #00f2fe);
}
.main {
    background-color: white;
    padding: 25px;
    border-radius: 15px;
}
h1 {
    color: #2b2d42;
    text-align: center;
}
.result {
    font-size: 20px;
    font-weight: bold;
    padding: 12px;
    border-radius: 10px;
    text-align: center;
}
.pass {
    background-color: #d4edda;
    color: #155724;
}
.fail {
    background-color: #f8d7da;
    color: #721c24;
}
</style>
""", unsafe_allow_html=True)

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
    if m >= 90: return "O"
    elif m >= 80: return "A+"
    elif m >= 70: return "A"
    elif m >= 60: return "B+"
    elif m >= 50: return "B"
    else: return "F"

def grade_point(m):
    if m >= 90: return 10
    elif m >= 80: return 9
    elif m >= 70: return 8
    elif m >= 60: return 7
    elif m >= 50: return 6
    else: return 0

# ---------------- PDF ----------------
def generate_pdf(name, roll, dept, sem, df, percentage, cgpa, result):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "COLLEGE MARKSHEET", ln=True, align="C")

    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 8, f"Name: {name}", ln=True)
    pdf.cell(0, 8, f"Roll No: {roll}", ln=True)
    pdf.cell(0, 8, f"Department: {dept}", ln=True)
    pdf.cell(0, 8, f"Semester: {sem}", ln=True)
    pdf.ln(5)

    pdf.set_font("Arial", "B", 11)
    pdf.cell(70, 8, "Subject", 1)
    pdf.cell(30, 8, "Marks", 1)
    pdf.cell(30, 8, "Grade", 1)
    pdf.ln()

    pdf.set_font("Arial", "", 11)
    for _, row in df.iterrows():
        pdf.cell(70, 8, row["Subject"], 1)
        pdf.cell(30, 8, str(row["Marks"]), 1)
        pdf.cell(30, 8, row["Grade"], 1)
        pdf.ln()

    pdf.ln(5)
    pdf.cell(0, 8, f"Percentage: {percentage}%", ln=True)
    pdf.cell(0, 8, f"CGPA: {cgpa}", ln=True)
    pdf.cell(0, 8, f"Result: {result}", ln=True)

    temp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf.output(temp.name)
    return temp.name

# ---------------- UI ----------------
st.title("🎓 Smart College Marksheet Generator")

dept = st.selectbox("Department", dept_sem_subjects.keys())
sem = st.selectbox("Semester", dept_sem_subjects[dept].keys())

name = st.text_input("Student Name")
roll = st.text_input("Roll Number")

subjects = dept_sem_subjects[dept][sem]
marks = [st.number_input(sub, 0, 100, key=sub) for sub in subjects]

if st.button("📊 Generate Marksheet"):
    if name and roll:
        grades = [grade(m) for m in marks]
        cgpa = round(sum(grade_point(m) for m in marks) / len(marks), 2)
        percentage = round(sum(marks) / len(marks), 2)
        result = "PASS" if min(marks) >= 50 else "FAIL"

        df = pd.DataFrame({
            "Subject": subjects,
            "Marks": marks,
            "Grade": grades
        })

        fig, ax = plt.subplots()
        ax.bar(subjects, marks)
        plt.xticks(rotation=45)
        st.pyplot(fig)

        st.table(df)

        if result == "PASS":
            st.markdown(f"<div class='result pass'>🎉 RESULT: PASS<br>CGPA: {cgpa} | Percentage: {percentage}%</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='result fail'>❌ RESULT: FAIL<br>CGPA: {cgpa} | Percentage: {percentage}%</div>", unsafe_allow_html=True)

        pdf_path = generate_pdf(name, roll, dept, sem, df, percentage, cgpa, result)

        st.download_button(
            "📄 Download Marksheet PDF",
            data=open(pdf_path, "rb"),
            file_name=f"{roll}_marksheet.pdf"
        )
    else:
        st.error("Please enter Name and Roll Number")
