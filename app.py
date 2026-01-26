import streamlit as st
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from fpdf import FPDF
import tempfile


# ================= SUBJECT DATA =================
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
    "AIDS": {
        "Semester 1": ["Maths I","Physics","Python","English","Graphics","Physics Lab"],
        "Semester 2": ["Maths II","DS","Statistics","EVS","Communication","Python Lab"],
        "Semester 3": ["DBMS","OS","Probability","AI Basics","OOP","DBMS Lab"],
        "Semester 4": ["ML","DAA","CN","Deep Learning","Maths","ML Lab"],
        "Semester 5": ["NLP","Big Data","Cloud","Data Visualization","Elective I","DL Lab"],
        "Semester 6": ["Computer Vision","MLOps","IoT","Elective II","Mini Project","Case Study"],
        "Semester 7": ["Advanced AI","Data Ethics","Elective III","Seminar","Internship","Research"],
        "Semester 8": ["Project Work","Review","Elective IV","Industrial Training","Viva","Presentation"]
    },
    "Mechanical": {
        "Semester 1": ["Maths I","Physics","Engineering Mechanics","English","Graphics","Physics Lab"],
        "Semester 2": ["Maths II","Thermodynamics","Material Science","EVS","Communication","Workshop"],
        "Semester 3": ["SOM","Manufacturing","Fluid Mechanics","Thermal Engg","DS","FM Lab"],
        "Semester 4": ["Kinematics","Dynamics","Heat Transfer","Metrology","Probability","HT Lab"],
        "Semester 5": ["Machine Design","CAD/CAM","Mechatronics","Elective I","FEM","CAD Lab"],
        "Semester 6": ["IC Engines","Refrigeration","Industrial Engg","Elective II","Mini Project","Case Study"],
        "Semester 7": ["Robotics","Automation","Elective III","Seminar","Internship","Research"],
        "Semester 8": ["Project Work","Review","Elective IV","Industrial Training","Viva","Presentation"]
    },
    "Civil": {
        "Semester 1": ["Maths I","Physics","Engineering Mechanics","English","Graphics","Physics Lab"],
        "Semester 2": ["Maths II","Surveying","Material Science","EVS","Communication","Workshop"],
        "Semester 3": ["Structural Analysis","Fluid Mechanics","Concrete Tech","Geotech","DS","FM Lab"],
        "Semester 4": ["Hydraulics","Transportation Engg","Environmental Engg","Probability","CAD","Lab"],
        "Semester 5": ["Design of RC","Water Resources","Elective I","Elective II","FEM","CAD Lab"],
        "Semester 6": ["Construction Management","Bridge Engineering","Elective III","Elective IV","Mini Project","Case Study"],
        "Semester 7": ["Advanced Structures","Planning","Elective V","Seminar","Internship","Research"],
        "Semester 8": ["Project Work","Review","Elective VI","Industrial Training","Viva","Presentation"]
    }
}

# ================= CGPA CALCULATION =================
def grade_point(m):
    if m >= 90: return 10
    elif m >= 80: return 9
    elif m >= 70: return 8
    elif m >= 60: return 7
    elif m >= 50: return 6
    else: return 0

def calculate_cgpa(marks):
    return round(sum(grade_point(m) for m in marks)/len(marks),2)

# ================= PDF GENERATION =================
def generate_pdf(name, roll, dept, sem, subjects, marks, cgpa):
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
    pdf.cell(90, 8, "Subject", 1)
    pdf.cell(30, 8, "Marks", 1)
    pdf.ln()
    pdf.set_font("Arial", "", 11)
    for s, m in zip(subjects, marks):
        pdf.cell(90, 8, s, 1)
        pdf.cell(30, 8, str(m), 1)
        pdf.ln()
    pdf.ln(5)
    pdf.cell(0, 8, f"CGPA: {cgpa}", ln=True)
    temp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf.output(temp.name)
    return temp.name

# ================= MAIN APP =================
def main_app():
    st.title("🎓 Smart College Marksheet System")
    st.button("🚪 Logout", on_click=logout)
    
    dept = st.selectbox("Department", dept_sem_subjects.keys())
    sem = st.selectbox("Semester", dept_sem_subjects[dept].keys())
    name = st.text_input("Student Name")
    roll = st.text_input("Roll Number")
    
    subjects = dept_sem_subjects[dept][sem]
    marks = [st.number_input(sub, 0, 100, key=sub) for sub in subjects]
    
    if "generated" not in st.session_state:
        st.session_state.generated = False

    # ---------- GENERATE ----------
    if st.button("📊 Generate Marksheet"):
        if name and roll:
            st.session_state.cgpa = calculate_cgpa(marks)
            st.session_state.generated = True
            fig, ax = plt.subplots()
            ax.bar(subjects, marks)
            plt.xticks(rotation=45)
            st.pyplot(fig)
            st.success(f"CGPA: {st.session_state.cgpa}")
        else:
            st.error("Enter Name and Roll Number")

    # ---------- SAVE TO EXCEL ----------
    if st.session_state.generated and st.button("💾 Save to Excel"):
        excel_file = f"{dept}_records.xlsx"
        record = {"Name": name, "Roll No": roll}
        for s, m in zip(subjects, marks):
            record[s] = m
        record[f"{sem} CGPA"] = st.session_state.cgpa

        if os.path.exists(excel_file):
            df_old = pd.read_excel(excel_file)
            df_new = pd.DataFrame([record])
            df_final = pd.concat([df_old, df_new], ignore_index=True)
        else:
            df_final = pd.DataFrame([record])

        df_final.to_excel(excel_file, index=False)
        st.success(f"Saved to {excel_file} ✅")

    # ---------- DOWNLOAD EXCEL ----------
    excel_file = f"{dept}_records.xlsx"
    if os.path.exists(excel_file):
        st.download_button(
            "📥 Download Excel",
            data=open(excel_file,"rb"),
            file_name=excel_file
        )

    # ---------- DOWNLOAD PDF ----------
    if st.session_state.generated:
        pdf_path = generate_pdf(name, roll, dept, sem, subjects, marks, st.session_state.cgpa)
        st.download_button(
            "📄 Download Marksheet PDF",
            data=open(pdf_path,"rb"),
            file_name=f"{roll}_{sem}_marksheet.pdf"
        )

# ================= ROUTING =================
if st.session_state.logged_in:
    main_app()
else:
    login_page()
