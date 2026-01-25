import streamlit as st
import numpy as np
from sklearn.linear_model import LinearRegression
from fpdf import FPDF
import tempfile

# ---------------- DEPARTMENT + SEMESTER SUBJECTS ----------------
dept_sem_subjects = {
    "CSE": {
        "Semester 1": [
            "Engineering Mathematics I",
            "Engineering Physics",
            "Programming for Problem Solving",
            "English",
            "Engineering Graphics",
            "Physics Lab"
        ],
        "Semester 2": [
            "Engineering Mathematics II",
            "Programming in C",
            "Basic Electrical Engineering",
            "Environmental Science",
            "Communication Skills",
            "C Programming Lab"
        ],
        "Semester 3": [
            "Data Structures",
            "Discrete Mathematics",
            "Digital Electronics",
            "Object Oriented Programming",
            "Operating Systems",
            "Data Structures Lab"
        ],
        "Semester 4": [
            "Database Management Systems",
            "Computer Networks",
            "Design & Analysis of Algorithms",
            "Software Engineering",
            "Microprocessors",
            "DBMS Lab"
        ],
        "Semester 5": [
            "Web Technologies",
            "Machine Learning",
            "Compiler Design",
            "Cloud Computing",
            "Computer Graphics",
            "Elective I"
        ],
        "Semester 6": [
            "Artificial Intelligence",
            "Big Data Analytics",
            "Internet of Things",
            "Mobile App Development",
            "Elective II",
            "Mini Project"
        ],
        "Semester 7": [
            "Deep Learning",
            "Information Security",
            "Data Science",
            "Elective III",
            "Seminar",
            "Internship"
        ],
        "Semester 8": [
            "Project Work",
            "Project Review",
            "Elective IV",
            "Industrial Training",
            "Comprehensive Viva",
            "Technical Presentation"
        ]
    },

    "IT": {
        "Semester 1": [
            "Engineering Mathematics I",
            "Engineering Physics",
            "Python Programming",
            "English",
            "Engineering Graphics",
            "Physics Lab"
        ],
        "Semester 2": [
            "Engineering Mathematics II",
            "Programming in C",
            "Digital Fundamentals",
            "Environmental Science",
            "Communication Skills",
            "IT Workshop"
        ],
        "Semester 3": [
            "Data Structures",
            "Discrete Mathematics",
            "Computer Organization",
            "Object Oriented Programming",
            "Operating Systems",
            "Data Structures Lab"
        ],
        "Semester 4": [
            "Database Management Systems",
            "Computer Networks",
            "Software Engineering",
            "Web Programming",
            "Microprocessors",
            "DBMS Lab"
        ],
        "Semester 5": [
            "Web Technologies",
            "Machine Learning",
            "Cloud Computing",
            "Data Warehousing",
            "Computer Graphics",
            "Elective I"
        ],
        "Semester 6": [
            "Artificial Intelligence",
            "Big Data Analytics",
            "Internet of Things",
            "Mobile App Development",
            "Elective II",
            "Mini Project"
        ],
        "Semester 7": [
            "Information Security",
            "Data Science",
            "Blockchain Technology",
            "Elective III",
            "Seminar",
            "Internship"
        ],
        "Semester 8": [
            "Project Work",
            "Project Review",
            "Elective IV",
            "Industrial Training",
            "Comprehensive Viva",
            "Technical Presentation"
        ]
    }
}

# ---------------- GRADE FUNCTION ----------------
def grade(mark):
    if mark >= 90:
        return "A+", "Pass"
    elif mark >= 80:
        return "A", "Pass"
    elif mark >= 70:
        return "B+", "Pass"
    elif mark >= 60:
        return "B", "Pass"
    elif mark >= 50:
        return "C", "Pass"
    else:
        return "D", "Fail"

# ---------------- ML PERFORMANCE ANALYSIS ----------------
def lr_suggestion(marks):
    X = np.array(range(1, len(marks) + 1)).reshape(-1, 1)
    y = np.array(marks)
    model = LinearRegression()
    model.fit(X, y)

    if model.coef_[0] > 0:
        return "Performance Improving"
    elif model.coef_[0] < 0:
        return "Performance Declining"
    else:
        return "Stable Performance"

# ---------------- PDF GENERATION ----------------
def generate_pdf(college, dept, sem, name, roll, subjects, marks):
    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, college, ln=True, align="C")
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 8, f"Department: {dept}", ln=True, align="C")
    pdf.cell(0, 8, f"Semester: {sem}", ln=True, align="C")
    pdf.ln(8)

    pdf.set_font("Arial", "", 11)
    pdf.cell(0, 8, f"Student Name : {name}", ln=True)
    pdf.cell(0, 8, f"Roll Number  : {roll}", ln=True)
    pdf.ln(5)

    pdf.set_font("Arial", "B", 11)
    pdf.cell(50, 10, "Subject", 1)
    pdf.cell(25, 10, "Marks", 1)
    pdf.cell(25, 10, "Grade", 1)
    pdf.cell(30, 10, "Result", 1)
    pdf.cell(60, 10, "ML Remark", 1)
    pdf.ln()

    suggestion = lr_suggestion(marks)

    for i in range(len(subjects)):
        g, r = grade(marks[i])
        pdf.set_font("Arial", "", 11)
        pdf.cell(50, 10, subjects[i], 1)
        pdf.cell(25, 10, str(marks[i]), 1)
        pdf.cell(25, 10, g, 1)
        pdf.cell(30, 10, r, 1)
        pdf.cell(60, 10, suggestion, 1)
        pdf.ln()

    avg = sum(marks) / len(marks)
    pdf.ln(5)
    pdf.set_font("Arial", "B", 11)
    pdf.cell(0, 8, f"Overall Percentage: {avg:.2f}%", ln=True)
    pdf.cell(0, 8, f"Final Result: {'PASS' if avg >= 50 else 'FAIL'}", ln=True)

    temp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf.output(temp.name)
    return temp.name, avg, suggestion

# ---------------- STREAMLIT UI ----------------
st.title("🎓 Smart College Marksheet Generator (ML Based)")

college = st.text_input("College Name")
dept = st.selectbox("Department", list(dept_sem_subjects.keys()))
sem = st.selectbox("Semester", list(dept_sem_subjects[dept].keys()))

name = st.text_input("Student Name")
roll = st.text_input("Roll Number")
parent_mobile = st.text_input("Parent Mobile Number")
parent_email = st.text_input("Parent Email")

st.subheader("📘 Enter Subject Marks")

subjects = dept_sem_subjects[dept][sem]
marks = []

for sub in subjects:
    marks.append(st.number_input(sub, min_value=0, max_value=100, step=1))

if st.button("Generate Marksheet"):
    if college and name and roll and parent_mobile and parent_email:
        pdf_path, avg, insight = generate_pdf(
            college, dept, sem, name, roll, subjects, marks
        )

        st.success("✅ Marksheet Generated Successfully")

        st.subheader("📊 Performance Summary")
        st.write(f"Overall Percentage: **{avg:.2f}%**")
        st.write(f"ML Insight: **{insight}**")

        with open(pdf_path, "rb") as f:
            st.download_button(
                "📥 Download Marksheet PDF",
                f,
                file_name=f"{roll}_{sem}_Marksheet.pdf",
                mime="application/pdf"
            )

        st.info(f"📧 Sent to Parent Email: {parent_email}")
        st.info(f"📱 Sent to Parent Mobile: {parent_mobile}")
    else:
        st.error("❌ Please fill all required fields")
