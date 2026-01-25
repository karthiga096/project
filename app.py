import streamlit as st
import numpy as np
from sklearn.linear_model import LinearRegression
from fpdf import FPDF
import tempfile

# ---------------- DEPARTMENT + SEMESTER SUBJECTS ----------------
dept_sem_subjects = {

    "CSE": {
        "Semester 1": ["Engineering Mathematics I","Engineering Physics","Programming for Problem Solving","English","Engineering Graphics","Physics Lab"],
        "Semester 2": ["Engineering Mathematics II","Programming in C","Basic Electrical Engineering","Environmental Science","Communication Skills","C Programming Lab"],
        "Semester 3": ["Data Structures","Discrete Mathematics","Digital Electronics","OOP","Operating Systems","DS Lab"],
        "Semester 4": ["DBMS","Computer Networks","DAA","Software Engineering","Microprocessors","DBMS Lab"],
        "Semester 5": ["Web Technologies","Machine Learning","Compiler Design","Cloud Computing","Computer Graphics","Elective I"],
        "Semester 6": ["Artificial Intelligence","Big Data Analytics","IoT","Mobile App Development","Elective II","Mini Project"],
        "Semester 7": ["Deep Learning","Information Security","Data Science","Elective III","Seminar","Internship"],
        "Semester 8": ["Project Work","Project Review","Elective IV","Industrial Training","Comprehensive Viva","Technical Presentation"]
    },

    "IT": {
        "Semester 1": ["Engineering Mathematics I","Engineering Physics","Python Programming","English","Engineering Graphics","Physics Lab"],
        "Semester 2": ["Engineering Mathematics II","Programming in C","Digital Fundamentals","Environmental Science","Communication Skills","IT Workshop"],
        "Semester 3": ["Data Structures","Discrete Mathematics","Computer Organization","OOP","Operating Systems","DS Lab"],
        "Semester 4": ["DBMS","Computer Networks","Software Engineering","Web Programming","Microprocessors","DBMS Lab"],
        "Semester 5": ["Web Technologies","Machine Learning","Cloud Computing","Data Warehousing","Computer Graphics","Elective I"],
        "Semester 6": ["Artificial Intelligence","Big Data Analytics","IoT","Mobile App Development","Elective II","Mini Project"],
        "Semester 7": ["Information Security","Data Science","Blockchain Technology","Elective III","Seminar","Internship"],
        "Semester 8": ["Project Work","Project Review","Elective IV","Industrial Training","Comprehensive Viva","Technical Presentation"]
    },

    "AIDS": {
        "Semester 1": ["Engineering Mathematics I","Engineering Physics","Python Programming","English","Engineering Graphics","Physics Lab"],
        "Semester 2": ["Engineering Mathematics II","Data Structures","Digital Logic","Environmental Science","Communication Skills","Python Lab"],
        "Semester 3": ["Discrete Mathematics","OOP","DBMS","Statistics for AI","Operating Systems","DBMS Lab"],
        "Semester 4": ["Machine Learning","DAA","Computer Networks","Artificial Intelligence","Probability","ML Lab"],
        "Semester 5": ["Deep Learning","NLP","Big Data Analytics","Cloud Computing","Data Visualization","Elective I"],
        "Semester 6": ["Computer Vision","Reinforcement Learning","IoT","MLOps","Elective II","Mini Project"],
        "Semester 7": ["Advanced AI","Data Ethics","Elective III","Seminar","Internship","Research Methodology"],
        "Semester 8": ["Project Work","Project Review","Elective IV","Industrial Training","Comprehensive Viva","Technical Presentation"]
    },

    "ECE": {
        "Semester 1": ["Engineering Mathematics I","Engineering Physics","Basic Electronics","English","Engineering Graphics","Physics Lab"],
        "Semester 2": ["Engineering Mathematics II","Circuit Theory","Electronic Devices","Environmental Science","Communication Skills","Electronics Lab"],
        "Semester 3": ["Signals and Systems","Analog Circuits","Digital Electronics","EM Theory","Data Structures","Analog Lab"],
        "Semester 4": ["Communication Systems","Control Systems","Microprocessors","Linear ICs","Probability","Comm Lab"],
        "Semester 5": ["DSP","VLSI Design","Embedded Systems","Wireless Communication","Elective I","DSP Lab"],
        "Semester 6": ["Microwave Engineering","Optical Communication","IoT","Antennas","Elective II","Mini Project"],
        "Semester 7": ["ML for ECE","Satellite Communication","Elective III","Seminar","Internship","Research Methodology"],
        "Semester 8": ["Project Work","Project Review","Elective IV","Industrial Training","Comprehensive Viva","Technical Presentation"]
    },

    "EEE": {
        "Semester 1": ["Engineering Mathematics I","Engineering Physics","Basic Electrical Engineering","English","Engineering Graphics","Physics Lab"],
        "Semester 2": ["Engineering Mathematics II","Circuit Theory","Electrical Machines I","Environmental Science","Communication Skills","Electrical Lab"],
        "Semester 3": ["Electrical Machines II","Power Systems I","Digital Electronics","Control Systems","Data Structures","Machines Lab"],
        "Semester 4": ["Power Systems II","Power Electronics","Measurements","Microprocessors","Probability","PE Lab"],
        "Semester 5": ["Renewable Energy","Smart Grid","Embedded Systems","Electrical Drives","Elective I","Drives Lab"],
        "Semester 6": ["High Voltage Engineering","Industrial Automation","IoT","Energy Management","Elective II","Mini Project"],
        "Semester 7": ["ML for EEE","FACTS","Elective III","Seminar","Internship","Research Methodology"],
        "Semester 8": ["Project Work","Project Review","Elective IV","Industrial Training","Comprehensive Viva","Technical Presentation"]
    },

    "Biotechnology": {
        "Semester 1": ["Engineering Mathematics I","Engineering Physics","Engineering Chemistry","English","Biology","Chemistry Lab"],
        "Semester 2": ["Engineering Mathematics II","Biochemistry","Cell Biology","Environmental Science","Communication Skills","Biology Lab"],
        "Semester 3": ["Microbiology","Genetics","Bioprocess Engineering","Organic Chemistry","Data Analysis","Micro Lab"],
        "Semester 4": ["Molecular Biology","Immunology","Biostatistics","Downstream Processing","Bioinformatics","MB Lab"],
        "Semester 5": ["Genetic Engineering","Enzyme Technology","Pharma Biotechnology","Computational Biology","Elective I","Biotech Lab"],
        "Semester 6": ["Industrial Biotechnology","Plant Biotechnology","Medical Biotechnology","Bioprocess Control","Elective II","Mini Project"],
        "Semester 7": ["Bioethics","Research Methodology","Elective III","Seminar","Internship","Case Studies"],
        "Semester 8": ["Project Work","Project Review","Elective IV","Industrial Training","Comprehensive Viva","Technical Presentation"]
    }
}

# ---------------- GRADE FUNCTION ----------------
def grade(mark):
    if mark >= 90: return "A+", "Pass"
    elif mark >= 80: return "A", "Pass"
    elif mark >= 70: return "B+", "Pass"
    elif mark >= 60: return "B", "Pass"
    elif mark >= 50: return "C", "Pass"
    else: return "D", "Fail"

# ---------------- ML PERFORMANCE ----------------
def lr_suggestion(marks):
    X = np.array(range(1, len(marks)+1)).reshape(-1,1)
    y = np.array(marks)
    model = LinearRegression().fit(X,y)
    return "Performance Improving" if model.coef_[0] > 0 else "Needs Improvement"

# ---------------- PDF GENERATION ----------------
def generate_pdf(college, dept, sem, name, roll, subjects, marks):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial","B",16)
    pdf.cell(0,10,college,ln=True,align="C")
    pdf.set_font("Arial","",12)
    pdf.cell(0,8,f"{dept} - {sem}",ln=True,align="C")
    pdf.ln(5)
    pdf.cell(0,8,f"Student Name: {name}",ln=True)
    pdf.cell(0,8,f"Roll Number: {roll}",ln=True)
    pdf.ln(5)

    pdf.set_font("Arial","B",11)
    pdf.cell(60,10,"Subject",1)
    pdf.cell(25,10,"Marks",1)
    pdf.cell(25,10,"Grade",1)
    pdf.cell(30,10,"Result",1)
    pdf.ln()

    for i in range(len(subjects)):
        g,r = grade(marks[i])
        pdf.set_font("Arial","",11)
        pdf.cell(60,10,subjects[i],1)
        pdf.cell(25,10,str(marks[i]),1)
        pdf.cell(25,10,g,1)
        pdf.cell(30,10,r,1)
        pdf.ln()

    temp = tempfile.NamedTemporaryFile(delete=False,suffix=".pdf")
    pdf.output(temp.name)
    return temp.name

# ---------------- STREAMLIT UI ----------------
st.title("🎓 Smart College Marksheet Generator (ML)")

college = st.text_input("College Name")
dept = st.selectbox("Department", dept_sem_subjects.keys())
sem = st.selectbox("Semester", dept_sem_subjects[dept].keys())
name = st.text_input("Student Name")
roll = st.text_input("Roll Number")

subjects = dept_sem_subjects[dept][sem]
marks = [st.number_input(sub,0,100) for sub in subjects]

if st.button("Generate Marksheet"):
    pdf = generate_pdf(college,dept,sem,name,roll,subjects,marks)
    st.success("Marksheet Generated")
    with open(pdf,"rb") as f:
        st.download_button("Download PDF",f,file_name=f"{roll}_{sem}.pdf")
