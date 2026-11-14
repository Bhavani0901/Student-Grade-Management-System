from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO
import streamlit as st
import json
import os
import csv

# Page configuration
st.set_page_config(
    page_title="Student Grade Management System",
    page_icon="🎓",
    layout="wide"
)

SUBJECTS = ["Python", "SQL", "Statistics"]

# Load student records
def load_students():

    if os.path.exists("students.json"):

        with open("students.json", "r") as file:
            return json.load(file)

    return {}


students = load_students()

# Calculate student results
def calculate_results(marks):

    total = sum(marks.values())
    percentage = (total / 300) * 100

    if percentage >= 90:
        grade, gpa = "A+", 10
    elif percentage >= 80:
        grade, gpa = "A", 9
    elif percentage >= 70:
        grade, gpa = "B", 8
    elif percentage >= 60:
        grade, gpa = "C", 7
    elif percentage >= 50:
        grade, gpa = "D", 6
    elif percentage >= 40:
        grade, gpa = "E", 5
    else:
        grade, gpa = "F", 0

    return total, percentage, grade, gpa


# Application title
st.title("🎓 Student Grade Management System")

st.write(
    "Manage student records, marks, grades and academic performance."
)

st.divider()

st.header("Welcome, Administrator!")

st.subheader("Dashboard Overview")

# Dashboard metrics
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Students", len(students))

with col2:
    st.metric("Total Subjects", len(SUBJECTS))

with col3:
    st.metric("System Status", "Active")

st.divider()

# Display student records
st.header("📋 Student Records")

if students:

    student_data = []

    for student_id, details in students.items():

        marks = details["marks"]

        total, percentage, grade, gpa = calculate_results(marks)

        student_data.append({
            "Student ID": student_id,
            "Name": details["name"],
            "Python": marks["Python"],
            "SQL": marks["SQL"],
            "Statistics": marks["Statistics"],
            "Total": total,
            "Percentage": round(percentage, 2),
            "Grade": grade,
            "GPA": gpa
        })

    st.dataframe(
        student_data,
        use_container_width=True
    )

else:
    st.info("No student records found. Add students using your Python program.")


# --------------------------------
# ADD NEW STUDENT
# --------------------------------

st.divider()

st.header("➕ Add New Student")

with st.form("add_student_form"):

    student_id = st.text_input("Student ID")

    name = st.text_input("Student Name")

    st.subheader("Enter Subject Marks")

    python_marks = st.number_input(
        "Python Marks",
        min_value=0,
        max_value=100,
        step=1
    )

    sql_marks = st.number_input(
        "SQL Marks",
        min_value=0,
        max_value=100,
        step=1
    )

    statistics_marks = st.number_input(
        "Statistics Marks",
        min_value=0,
        max_value=100,
        step=1
    )

    submit = st.form_submit_button("Add Student")

    if submit:

        if not student_id.strip() or not name.strip():
            st.error("Student ID and Name are required.")

        elif student_id in students:
            st.error("Student ID already exists.")

        else:

            students[student_id] = {
                "name": name,
                "marks": {
                    "Python": python_marks,
                    "SQL": sql_marks,
                    "Statistics": statistics_marks
                }
            }

            with open("students.json", "w") as file:
                json.dump(students, file, indent=4)

            st.success("Student added successfully!")

            st.rerun()

# --------------------------------
# UPDATE STUDENT
# --------------------------------

st.divider()

st.header("✏️ Update Student")

if students:

    with st.form("update_student_form"):

        selected_id = st.selectbox(
            "Select Student ID",
            list(students.keys())
        )

        current_student = students[selected_id]
        current_marks = current_student["marks"]

        new_name = st.text_input(
            "Student Name",
            value=current_student["name"]
        )

        st.subheader("Update Subject Marks")

        new_python = st.number_input(
            "Python Marks",
            min_value=0,
            max_value=100,
            value=int(current_marks["Python"]),
            step=1,
            key="update_python"
        )

        new_sql = st.number_input(
            "SQL Marks",
            min_value=0,
            max_value=100,
            value=int(current_marks["SQL"]),
            step=1,
            key="update_sql"
        )

        new_statistics = st.number_input(
            "Statistics Marks",
            min_value=0,
            max_value=100,
            value=int(current_marks["Statistics"]),
            step=1,
            key="update_statistics"
        )

        update_button = st.form_submit_button(
            "Update Student"
        )

        if update_button:

            if not new_name.strip():

                st.error("Student name cannot be empty.")

            else:

                students[selected_id]["name"] = new_name.strip()

                students[selected_id]["marks"] = {
                    "Python": new_python,
                    "SQL": new_sql,
                    "Statistics": new_statistics
                }

                with open("students.json", "w") as file:
                    json.dump(students, file, indent=4)

                st.success("Student updated successfully!")

                st.rerun()

else:

    st.info("No students available to update.")


# --------------------------------
# DELETE STUDENT
# --------------------------------

st.divider()

st.header("🗑️ Delete Student")

if students:

    with st.form("delete_student_form"):

        delete_id = st.selectbox(
            "Select Student to Delete",
            list(students.keys()),
            key="delete_student_id"
        )

        confirm_delete = st.checkbox(
            "I confirm that I want to delete this student."
        )

        delete_button = st.form_submit_button(
            "Delete Student"
        )

        if delete_button:

            if confirm_delete:

                del students[delete_id]

                with open("students.json", "w") as file:
                    json.dump(students, file, indent=4)

                st.success("Student deleted successfully!")

                st.rerun()

            else:

                st.warning("Please confirm before deleting.")

else:

    st.info("No students available to delete.")


# --------------------------------
# CLASS STATISTICS
# --------------------------------

st.divider()

st.header("📊 Class Performance Statistics")

if students:

    percentages = []

    for student_id, details in students.items():

        marks = details["marks"]

        total = sum(marks.values())

        percentage = (total / 300) * 100

        percentages.append(percentage)

    total_students = len(percentages)

    class_average = sum(percentages) / total_students

    highest_percentage = max(percentages)

    lowest_percentage = min(percentages)

    passed_students = sum(
        percentage >= 40 for percentage in percentages
    )

    failed_students = total_students - passed_students

    col1, col2, col3 = st.columns(3)

    col1.metric("Class Average", f"{class_average:.2f}%")

    col2.metric("Highest Percentage", f"{highest_percentage:.2f}%")

    col3.metric("Lowest Percentage", f"{lowest_percentage:.2f}%")

    col4, col5, col6 = st.columns(3)

    col4.metric("Total Students", total_students)

    col5.metric("Passed Students", passed_students)

    col6.metric("Failed Students", failed_students)

else:

    st.info("No student records available for statistics.")


# --------------------------------
# PDF REPORT CARD GENERATOR
# --------------------------------

st.divider()

st.header("📄 Generate Student Report Card")

if students:

    selected_id = st.selectbox(
        "Select Student",
        list(students.keys()),
        key="report_student"
    )

    if st.button("Generate PDF Report Card"):

        student = students[selected_id]
        marks = student["marks"]

        total, percentage, grade, gpa = calculate_results(marks)

        pdf_buffer = BytesIO()

        pdf = canvas.Canvas(pdf_buffer, pagesize=A4)

        # Report heading
        pdf.setFont("Helvetica-Bold", 20)
        pdf.drawCentredString(300, 800, "STUDENT REPORT CARD")

        # Student details
        pdf.setFont("Helvetica", 12)

        pdf.drawString(60, 750, f"Student ID: {selected_id}")
        pdf.drawString(60, 725, f"Student Name: {student['name']}")

        # Subject marks
        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(60, 680, "Subject-wise Marks")

        pdf.setFont("Helvetica", 12)

        y = 650

        for subject, mark in marks.items():

            pdf.drawString(
                60,
                y,
                f"{subject}: {mark}/100"
            )

            y -= 25

        # Final results
        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(60, 540, "Academic Performance")

        pdf.setFont("Helvetica", 12)

        pdf.drawString(60, 510, f"Total Marks: {total}/300")
        pdf.drawString(60, 485, f"Percentage: {percentage:.2f}%")
        pdf.drawString(60, 460, f"Grade: {grade}")
        pdf.drawString(60, 435, f"GPA: {gpa}/10")

        pdf.drawString(60, 380, "Generated by Student Grade Management System")

        pdf.save()

        pdf_buffer.seek(0)

        st.success("Report card generated successfully!")

        st.download_button(
            label="Download PDF Report Card",
            data=pdf_buffer,
            file_name=f"{selected_id}_report_card.pdf",
            mime="application/pdf"
        )

else:

    st.info("No students available to generate report cards.")

# --------------------------------
# EXPORT STUDENT RECORDS TO CSV
# --------------------------------

st.divider()

st.header("📊 Export Student Records")

if students:

    csv_data = []

    for student_id, details in students.items():

        marks = details["marks"]

        total, percentage, grade, gpa = calculate_results(marks)

        csv_data.append({
            "Student ID": student_id,
            "Name": details["name"],
            "Python": marks["Python"],
            "SQL": marks["SQL"],
            "Statistics": marks["Statistics"],
            "Total": total,
            "Percentage": round(percentage, 2),
            "Grade": grade,
            "GPA": gpa
        })

    import pandas as pd

    df = pd.DataFrame(csv_data)

    csv_file = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download Student Records (CSV)",
        data=csv_file,
        file_name="student_records.csv",
        mime="text/csv"
    )

else:

    st.info("No student records available to export.")
