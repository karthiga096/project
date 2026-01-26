import streamlit as st
import numpy as np
from sklearn.linear_model import LinearRegression
from fpdf import FPDF
import tempfile
import matplotlib.pyplot as plt

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
    "Mechatronics": {
        "Semester 1": ["Maths I","Physics","Basic Electrical","English","Graphics","Physics Lab"],
        "Semester 2": ["Maths II","Electronics","Mechanics","EVS","Communication","Electronics Lab"],
        "Semester 3": ["Sensors","Microcontrollers","Control Systems","Hydraulics","DS","Control Lab"],
        "Semester 4": ["Robotics","PLC","Embedded Systems","Probability","CAD","PLC Lab"],
        "Semester 5": ["Industrial Automation","Machine Vision","AI Basics","Elective I","Mechatronics","Automation Lab"],
        "Semester 6": ["IoT","Advanced Robotics","Smart Systems","Elective II","Mini Project","Case Study"],
        "Semester 7": ["Autonomous Systems","ML for Mechatronics","Elective III","Seminar","Internship","Research"],
        "Semester 8": ["Project Work","Review","Elective IV","Industrial Training","Viva","Presentation"]
    },
    "Biotechnology": {
        "Semester 1": ["Maths I","Physics","Chemistry","English","Biology","Chem Lab"],
        "Semester 2": ["Maths II","Biochemistry","Cell Biology","EVS","Communication","Bio Lab"],
        "Semester 3": ["Microbiology","Genetics","Bioprocess","Organic Chem","Statistics","Micro Lab"],
        "Semester 4": ["Molecular Biology","Immunology","Bioinformatics","DSP","Probability","MB Lab"],
        "Semester 5": ["Genetic Engg","Enzyme Tech","Pharma Biotech","Elective I","Comp Biology","Biotech Lab"],
        "Semester 6": ["Industrial Biotech","Plant Biotech","Medical Biotech","Elective II","Mini Project","Case Study"],
        "Semester 7": ["Bioethics","Research Methodology","Elective III","Seminar","Internship","Research"],
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
    else:
        st.error("Please fill all fields")
