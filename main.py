
import json
import csv
import os

# -----------------------------------
# CONFIGURATION
# -----------------------------------

SUBJECTS = ["Python", "SQL", "Statistics"]

DATA_FILE = "students.json"


# -----------------------------------
# LOAD AND SAVE STUDENT DATA
# -----------------------------------

def load_students():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            return json.load(file)

    return {}


def save_students():
    with open(DATA_FILE, "w") as file:
        json.dump(students, file, indent=4)


students = load_students()


# -----------------------------------
# GRADE CALCULATION
# -----------------------------------

def calculate_grade(percentage):

    if percentage >= 90:
        return "A+", 10
    elif percentage >= 80:
        return "A", 9
    elif percentage >= 70:
        return "B", 8
    elif percentage >= 60:
        return "C", 7
    elif percentage >= 50:
        return "D", 6
    elif percentage >= 40:
        return "E", 5
    else:
        return "F", 0


def calculate_results(marks):

    total = sum(marks.values())
    maximum = len(SUBJECTS) * 100

    percentage = (total / maximum) * 100

    grade, gpa = calculate_grade(percentage)

    return total, percentage, grade, gpa


# -----------------------------------
# INPUT VALIDATION
# -----------------------------------

def get_marks(subject):

    while True:
        try:
            mark = float(input(f"Enter {subject} marks (0-100): "))

            if 0 <= mark <= 100:
                return mark

            print("Marks must be between 0 and 100.")

        except ValueError:
            print("Please enter a valid number.")


# -----------------------------------
# ADD STUDENT
# -----------------------------------

def add_student():

    student_id = input("Enter Student ID: ").strip()

    if not student_id:
        print("Student ID cannot be empty.")
        return

    if student_id in students:
        print("Student ID already exists.")
        return

    name = input("Enter Student Name: ").strip()

    if not name:
        print("Student name cannot be empty.")
        return

    marks = {}

    for subject in SUBJECTS:
        marks[subject] = get_marks(subject)

    students[student_id] = {
        "name": name,
        "marks": marks
    }

    save_students()

    print("Student added successfully!")


# -----------------------------------
# DISPLAY ALL STUDENTS
# -----------------------------------

def display_students():

    if not students:
        print("No student records found.")
        return

    print("\n========== STUDENT RECORDS ==========")

    for student_id, details in students.items():

        total, percentage, grade, gpa = calculate_results(
            details["marks"]
        )

        print("\nStudent ID:", student_id)
        print("Name:", details["name"])

        for subject, mark in details["marks"].items():
            print(subject + ":", mark)

        print("Total:", total)
        print("Percentage:", round(percentage, 2), "%")
        print("Grade:", grade)
        print("GPA:", gpa)
        print("------------------------------------")


# -----------------------------------
# UPDATE STUDENT
# -----------------------------------

def update_student():

    student_id = input("Enter Student ID to update: ").strip()

    if student_id not in students:
        print("Student not found.")
        return

    print("\n1. Update Name")
    print("2. Update Subject Marks")

    choice = input("Enter your choice: ")

    if choice == "1":

        new_name = input("Enter new name: ").strip()

        if not new_name:
            print("Name cannot be empty.")
            return

        students[student_id]["name"] = new_name

    elif choice == "2":

        print("\nAvailable Subjects:")

        for i, subject in enumerate(SUBJECTS, start=1):
            print(i, subject)

        try:
            subject_choice = int(input("Select subject number: "))

            if not 1 <= subject_choice <= len(SUBJECTS):
                print("Invalid subject selection.")
                return

            subject = SUBJECTS[subject_choice - 1]

            students[student_id]["marks"][subject] = get_marks(subject)

        except ValueError:
            print("Please enter a valid number.")
            return

    else:
        print("Invalid choice.")
        return

    save_students()

    print("Student record updated successfully!")


# -----------------------------------
# DELETE STUDENT
# -----------------------------------

def delete_student():

    student_id = input("Enter Student ID to delete: ").strip()

    if student_id not in students:
        print("Student not found.")
        return

    confirm = input("Are you sure? (yes/no): ").lower()

    if confirm == "yes":

        del students[student_id]

        save_students()

        print("Student deleted successfully!")

    else:
        print("Deletion cancelled.")


# -----------------------------------
# SEARCH STUDENT
# -----------------------------------

def search_student():

    student_id = input("Enter Student ID: ").strip()

    if student_id not in students:
        print("Student not found.")
        return

    details = students[student_id]

    total, percentage, grade, gpa = calculate_results(
        details["marks"]
    )

    print("\nStudent Name:", details["name"])
    print("Student ID:", student_id)

    for subject, mark in details["marks"].items():
        print(subject + ":", mark)

    print("Total Marks:", total)
    print("Percentage:", round(percentage, 2), "%")
    print("Grade:", grade)
    print("GPA:", gpa)


# -----------------------------------
# CLASS STATISTICS
# -----------------------------------

def class_statistics():

    if not students:
        print("No records available.")
        return

    percentages = []

    for details in students.values():

        total, percentage, grade, gpa = calculate_results(
            details["marks"]
        )

        percentages.append(percentage)

    average = sum(percentages) / len(percentages)

    highest = max(percentages)
    lowest = min(percentages)

    passed = sum(1 for p in percentages if p >= 40)
    failed = len(percentages) - passed

    print("\n========== CLASS STATISTICS ==========")

    print("Total Students:", len(students))
    print("Class Average:", round(average, 2), "%")
    print("Highest Percentage:", round(highest, 2), "%")
    print("Lowest Percentage:", round(lowest, 2), "%")
    print("Students Passed:", passed)
    print("Students Failed:", failed)


# -----------------------------------
# GENERATE STUDENT REPORT CARD
# -----------------------------------

def generate_report_card():

    student_id = input("Enter Student ID: ").strip()

    if student_id not in students:
        print("Student not found.")
        return

    details = students[student_id]

    total, percentage, grade, gpa = calculate_results(
        details["marks"]
    )

    os.makedirs("report_cards", exist_ok=True)

    filename = f"report_cards/{student_id}_report.txt"

    with open(filename, "w") as file:

        file.write("STUDENT PERFORMANCE REPORT\n")
        file.write("===========================\n")

        file.write(f"Student ID: {student_id}\n")
        file.write(f"Student Name: {details['name']}\n\n")

        file.write("SUBJECT MARKS\n")

        for subject, mark in details["marks"].items():
            file.write(f"{subject}: {mark}\n")

        file.write("\nRESULT SUMMARY\n")

        file.write(f"Total Marks: {total}\n")
        file.write(f"Percentage: {percentage:.2f}%\n")
        file.write(f"Grade: {grade}\n")
        file.write(f"GPA: {gpa}\n")

    print("Report card generated:", filename)


# -----------------------------------
# EXPORT ALL STUDENTS TO CSV
# -----------------------------------

def export_csv():

    if not students:
        print("No student records to export.")
        return

    filename = "student_records.csv"

    with open(filename, "w", newline="") as file:

        writer = csv.writer(file)

        writer.writerow([
            "Student ID",
            "Name",
            "Python",
            "SQL",
            "Statistics",
            "Total",
            "Percentage",
            "Grade",
            "GPA"
        ])

        for student_id, details in students.items():

            total, percentage, grade, gpa = calculate_results(
                details["marks"]
            )

            writer.writerow([
                student_id,
                details["name"],
                details["marks"]["Python"],
                details["marks"]["SQL"],
                details["marks"]["Statistics"],
                total,
                round(percentage, 2),
                grade,
                gpa
            ])

    print("Student records exported to", filename)


# -----------------------------------
# MAIN MENU
# -----------------------------------

def main():

    while True:

        print("\n===================================")
        print("   STUDENT GRADE MANAGEMENT SYSTEM")
        print("===================================")

        print("1. Add Student")
        print("2. Display All Students")
        print("3. Update Student")
        print("4. Delete Student")
        print("5. Search Student")
        print("6. Class Statistics")
        print("7. Generate Report Card")
        print("8. Export Student Records to CSV")
        print("9. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            add_student()

        elif choice == "2":
            display_students()

        elif choice == "3":
            update_student()

        elif choice == "4":
            delete_student()

        elif choice == "5":
            search_student()

        elif choice == "6":
            class_statistics()

        elif choice == "7":
            generate_report_card()

        elif choice == "8":
            export_csv()

        elif choice == "9":
            print("Thank you for using Student Grade Management System!")
            break

        else:
            print("Invalid choice. Please try again.")


# -----------------------------------
# RUN APPLICATION
# -----------------------------------

if __name__ == "__main__":
    main()
