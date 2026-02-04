import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF
import tempfile
import os

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Smart Marksheet Generator", page_icon="🎓")

# ---------------- SUBJECT DATA (UNCHANGED + ADDED) ----------------
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
    },
    "MECH": {
        "Semester 1": ["Maths I","Physics","Engineering Mechanics","English","Graphics","Physics Lab"],
        "Semester 2": ["Maths II","Thermodynamics","Material Science","EVS","Communication","Workshop"],
        "Semester 3": ["SOM","Kinematics","Manufacturing","Fluid Mechanics","DS","Mech Lab"],
        "Semester 4": ["Dynamics","Thermal Engg","Machine Design","Metrology","Probability","CAD Lab"],
        "Semester 5": ["Heat Transfer","CNC","Mechatronics","Elective I","Automation","Lab"],
        "Semester 6": ["Robotics","IC Engines","Power Plant","Elective II","Mini Project","Seminar"],
        "Semester 7": ["Industrial Engg","AI for Mech","Elective III","Internship","Research","Seminar"],
        "Semester 8": ["Project Work","Review","Elective IV","Industrial Training","Viva","Presentation"]
    }
}

# ---------------- GRADING ----------------
def grade(m):
    return "O" if m>=90 else "A+" if m>=80 else "A" if m>=70 else "B+" if m>=60 else "B" if m>=50 else "F"

def grade_point(m):
    return 10 if m>=90 else 9 if m>=80 else 8 if m>=70 else 7 if m>=60 else 6 if m>=50 else 0

# ---------------- PDF ----------------
def generate_pdf(name, roll, dept, sem, df, cgpa, percentage, result):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial","B",16)
    pdf.cell(0,10,"COLLEGE MARKSHEET",ln=True,align="C")

    pdf.set_font("Arial","",12)
    pdf.multi_cell(0,8,f"Name: {name}\nRoll No: {roll}\nDepartment: {dept}\nSemester: {sem}")
    pdf.ln(3)

    pdf.set_font("Arial","B",11)
    pdf.cell(80,8,"Subject",1)
    pdf.cell(30,8,"Marks",1)
    pdf.cell(30,8,"Grade",1)
    pdf.ln()

    pdf.set_font("Arial","",11)
    for _,r in df.iterrows():
        pdf.cell(80,8,r["Subject"],1)
        pdf.cell(30,8,str(r["Marks"]),1)
        pdf.cell(30,8,r["Grade"],1)
        pdf.ln()

    pdf.ln(4)
    pdf.cell(0,8,f"CGPA: {cgpa} | Percentage: {percentage}% | Result: {result}",ln=True)

    temp = tempfile.NamedTemporaryFile(delete=False,suffix=".pdf")
    pdf.output(temp.name)
    return temp.name

# ---------------- SAVE TO DEPARTMENT EXCEL ----------------
def save_dept_excel(dept, df):
    file = f"{dept}_records.xlsx"
    if os.path.exists(file):
        old = pd.read_excel(file)
        df = pd.concat([old, df], ignore_index=True)
    df.to_excel(file, index=False)
    return file

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
        "Subject": subjects,
        "Marks": marks,
        "Grade": grades
    })

    # -------- PERFORMANCE GRAPH --------
    st.subheader("📈 Performance Graph")
    fig, ax = plt.subplots()
    ax.bar(subjects, marks)
    ax.axhline(50, linestyle="--")
    ax.set_ylabel("Marks")
    plt.xticks(rotation=45)
    st.pyplot(fig)

    # -------- PDF --------
    pdf_path = generate_pdf(name, roll, dept, sem, df, cgpa, percentage, result)
    st.download_button("📄 Download Marksheet PDF", open(pdf_path,"rb"), f"{roll}_marksheet.pdf")

    # -------- DEPT EXCEL --------
    excel_df = df.copy()
    excel_df["Name"] = name
    excel_df["Roll No"] = roll
    excel_df["Department"] = dept
    excel_df["Semester"] = sem
    excel_df["CGPA"] = cgpa
    excel_df["Percentage"] = percentage
    excel_df["Result"] = result

    dept_file = save_dept_excel(dept, excel_df)
    st.download_button("📥 Download Department Excel", open(dept_file,"rb"), dept_file)
