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
.result {
    font-size: 20px;
    font-weight: bold;
    padding: 12px;
    border-radius: 10px;
    text-align: center;
}
.pass { background-color: #d4edda; color: #155724; }
.fail { background-color: #f8d7da; color: #721c24; }
</style>
""", unsafe_allow_html=True)

# ---------------- SUBJECT DATA (OLD + NEW) ----------------
dept_sem_subjects = {

    # ----- EXISTING (UNCHANGED) -----
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

    # ----- NEW DEPARTMENTS ADDED -----
    "MECH": {
        "Semester 1": ["Maths I","Physics","Engineering Mechanics","English","Graphics","Physics Lab"],
        "Semester 2": ["Maths II","Thermodynamics","Material Science","EVS","Communication","Workshop"],
        "Semester 3": ["Strength of Materials","Kinematics","Manufacturing","Fluid Mechanics","DS","Mech Lab"],
        "Semester 4": ["Dynamics","Thermal Engg","Machine Design","Metrology","Probability","CAD Lab"],
        "Semester 5": ["Heat Transfer","CNC","Mechatronics","Elective I","Automation","Lab"],
        "Semester 6": ["Robotics","IC Engines","Power Plant","Elective II","Mini Project","Seminar"],
        "Semester 7": ["Industrial Engg","AI for Mech","Elective III","Internship","Research","Seminar"],
        "Semester 8": ["Project Work","Review","Elective IV","Industrial Training","Viva","Presentation"]
    },

    "CIVIL": {
        "Semester 1": ["Maths I","Physics","Basic Civil","English","Graphics","Physics Lab"],
        "Semester 2": ["Maths II","Surveying","Construction","EVS","Communication","Survey Lab"],
        "Semester 3": ["Structural Analysis","Geotech","Hydrology","DS","Materials","Lab"],
        "Semester 4": ["RCC","Steel Structures","Transportation","Environmental","Probability","Lab"],
        "Semester 5": ["Foundation Engg","Irrigation","Elective I","GIS","Management","Lab"],
        "Semester 6": ["Earthquake Engg","Remote Sensing","Elective II","Mini Project","Seminar","Lab"],
        "Semester 7": ["Smart Cities","AI for Civil","Elective III","Internship","Research","Seminar"],
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
    return 10 if m>=90 else 9 if m>=80 else 8 if m>=70 else 7 if m>=60 else 6 if m>=50 else 0

# ---------------- PDF ----------------
def generate_pdf(name, roll, dept, sem, df, percentage, cgpa, result):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial","B",16)
    pdf.cell(0,10,"COLLEGE MARKSHEET",ln=True,align="C")

    pdf.set_font("Arial","",12)
    pdf.multi_cell(0,8,f"Name: {name}\nRoll No: {roll}\nDepartment: {dept}\nSemester: {sem}\n")
    pdf.ln(3)

    pdf.set_font("Arial","B",11)
    pdf.cell(70,8,"Subject",1)
    pdf.cell(30,8,"Marks",1)
    pdf.cell(30,8,"Grade",1)
    pdf.ln()

    pdf.set_font("Arial","",11)
    for _,r in df.iterrows():
        pdf.cell(70,8,r["Subject"],1)
        pdf.cell(30,8,str(r["Marks"]),1)
        pdf.cell(30,8,r["Grade"],1)
        pdf.ln()

    pdf.ln(5)
    pdf.cell(0,8,f"Percentage: {percentage}% | CGPA: {cgpa} | Result: {result}",ln=True)

    temp = tempfile.NamedTemporaryFile(delete=False,suffix=".pdf")
    pdf.output(temp.name)
    return temp.name

# ---------------- EXCEL ----------------
def generate_excel(name, roll, dept, sem, df, percentage, cgpa, result):
    ex = df.copy()
    ex["Name"] = name
    ex["Roll No"] = roll
    ex["Department"] = dept
    ex["Semester"] = sem
    ex["Percentage"] = percentage
    ex["CGPA"] = cgpa
    ex["Result"] = result

    temp = tempfile.NamedTemporaryFile(delete=False,suffix=".xlsx")
    ex.to_excel(temp.name,index=False)
    return temp.name

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

    df = pd.DataFrame({"Subject":subjects,"Marks":marks,"Grade":grades})

    pdf = generate_pdf(name,roll,dept,sem,df,percentage,cgpa,result)
    excel = generate_excel(name,roll,dept,sem,df,percentage,cgpa,result)

    st.download_button("📄 Download PDF",open(pdf,"rb"),f"{roll}_marksheet.pdf")
    st.download_button("📥 Download Excel",open(excel,"rb"),f"{roll}_marksheet.xlsx")
