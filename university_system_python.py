import os 
import pwinput
import pandas as pd
import sys
import csv
import time

prof_list = []
student_list = []

def system_window():                                    #finished
    while True :
        print("1-Dean system:              1")
        print("2-Prof system:              2")
        print("3-Students system:          3")
        print("4-Exit                      4")
        try :
            system = int(input("Number of process:"))

        except ValueError :
            print("this is Not a choice, Try again")

        if system == 1:
            
            Dean = input("Enter name of Dean :")
            Dean_password = pwinput.pwinput("Enter your password: ", mask="*")
            dean(Dean_password , Dean)
            
            
        elif system == 2:
            
            prof()
            
        elif system == 3:
            
            student()
            
        elif system == 4:
            
            sys.exit()
            
def dean(Dean_password, Dean):                              #finished
    
    dean_file = os.path.join(dean_path, f"{Dean}.csv")

    if not os.path.exists(dean_file):
        with open(dean_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Dean Name", "Password"])  #header
            writer.writerow([Dean, Dean_password])      #rows
    
    
    
    tries = 3
    for _ in range(tries): 
        password = input("Enter the password of Dean system: ")
        if password == Dean_password:
            print(f"Nice to meet you, Dean {Dean}")

            while True:
                print("\nEnter the number of the process you need:")
                print("1 - Add new student")
                print("2 - Add new professor")
                print("3 - Show current students")
                print("4 - Show current professors")
                print("5 - Remove Student")
                print("6 - Remove Professor")
                print("7 - Exit to Main Menu") 
                try:
                    process = int(input("Number of process: "))
                except ValueError:
                    print("This is not a valid choice, try again.")
                    continue  

                if process == 1:
                    while True:
                        student_name = input("Student Name: ")
                        student_Age = input("Student Age: ")
                        student_phone_number = input("Student Phone Number: ")

                        add_students(student_name, student_Age, student_phone_number, Dean)

                        more = input("Add more students? (y/n): ").strip().lower()
                        if more == "n":
                            break

                elif process == 2:
                    while True:
                        prof_name = input("Professor Name: ")
                        prof_Age = input("Professor Age: ")
                        prof_phone_number = input("Professor Phone Number: ")
                        prof_department = input("Professor Department: ")

                        add_prof(prof_name, prof_Age, prof_phone_number, prof_department, Dean)

                        more = input("Add more professors? (y/n): ").strip().lower()
                        if more == "n":
                            break

                elif process == 3:
                    show_students()  

                elif process == 4:
                    show_profs()  

                elif process == 5:
                    prof_name = input("Enter professor name to remove: ")
                    remove_prof(prof_name, Dean)    
                    
                elif process == 6:
                    student_name = input("Enter student name to remove: ")
                    remove_student(student_name, Dean)       

                elif process == 7:
                    print("\nReturning to the main menu...")  
                    time.sleep(2)
                    system_window()
                    

                else:
                    print("Invalid choice. Please enter a number between 1 and 5.")

        else:
            print("Incorrect password. Try again.")

    print("Too many failed attempts. Returning to the main menu...")

def prof():                                                 #finished
    
    prof_name = input("Enter your name: ").strip()

   
    prof_folder_path = os.path.join(prof_path, prof_name)
    os.makedirs(prof_folder_path, exist_ok=True)

    while True:
        print("\n1 - Create Assignment")
        print("2 - Take Attendance")
        print("3 - Exit to Main Menu")

        try:
            choice = int(input("Choose an option: "))
        except ValueError:
            print("Invalid input. Try again.")
            continue

        if choice == 1:
            create_assignment(prof_name)
        elif choice == 2:
            take_attendance(prof_name)
        elif choice == 3:
            print("Returning to the main menu...")
            return
        else:
            print("Invalid choice. Try again.")
            
def create_assignment(prof_name):                                                  #finished
    assignment_title = input("Enter assignment title: ")
    assignment_description = input("Enter assignment description: ")
    due_date = input("Enter due date (YYYY-MM-DD): ")

    assignment = {
        "Title": assignment_title,
        "Description": assignment_description,
        "Due Date": due_date
    }

    file_path = os.path.join(prof_path, prof_name, "assignments.csv")
    file_exists = os.path.exists(file_path)

    with open(file_path, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["Title", "Description", "Due Date"])
        if not file_exists:
            writer.writeheader()
        writer.writerow(assignment)

    print(f"Assignment '{assignment_title}' created successfully!")


def take_attendance(prof_name):                                                      #finished
    class_date = input("Enter class date:")
    student_names = input("Enter student names (comma-separated): ").split(",")

    attendance_records = [{"Date": class_date, "Student Name": student.strip(), "Present": "Yes"} for student in student_names]

    file_path = os.path.join(prof_path, prof_name, "attendance.csv")
    file_exists = os.path.exists(file_path)

    with open(file_path, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["Date", "Student Name", "Present"])
        if not file_exists:
            writer.writeheader()
        writer.writerows(attendance_records)

    print(f"Attendance recorded for {class_date}!")


def student():                                                                        #finished
    student_name = input("Enter your name: ").strip()
    
    while True:
        print("\n1 - View Assignments")
        print("2 - Check Attendance")
        print("3 - Exit to Main Menu")

        try:
            choice = int(input("Choose an option: "))
        except ValueError:
            print("Invalid input. Try again.")
            continue

        if choice == 1:
            view_assignments()
        elif choice == 2:
            check_attendance(student_name)
        elif choice == 3:
            print("Returning to the main menu...")
            return
        else:
            print("Invalid choice. Try again.")

def view_assignments():                                                               #finished
    professor_folders = os.listdir(prof_path)
    
    if not professor_folders:
        print("No professors have posted assignments yet.")
        return

    print("\nAvailable Assignments:\n" + "-" * 30)

    for prof in professor_folders:
        assignment_file = os.path.join(prof_path, prof, "assignments.csv")
        
        if os.path.exists(assignment_file):
            df = pd.read_csv(assignment_file)
            print(f"\nProfessor {prof}'s Assignments:")
            print(df.to_string(index=False))  # Display as a table without index
        else:
            print(f"No assignments found for Professor {prof}.")

def check_attendance(student_name):                                                    #finished
    professor_folders = os.listdir(prof_path)
    attendance_records = []

    for prof in professor_folders:
        attendance_file = os.path.join(prof_path, prof, "attendance.csv")

        if os.path.exists(attendance_file):
            df = pd.read_csv(attendance_file)
            student_attendance = df[df["Student Name"] == student_name]

            if not student_attendance.empty:
                attendance_records.append((prof, student_attendance))

    if attendance_records:
        print("\nYour Attendance Records:\n" + "-" * 30)
        for prof, record in attendance_records:
            print(f"\nProfessor {prof}'s Class:")
            print(record.to_string(index=False))
    else:
        print("No attendance records found for you.")

def add_prof(prof_name, prof_Age, prof_phone_number, prof_department , Dean):            #finished
    
    professor = {
        "Professor Name": prof_name,
        "Professor Age": prof_Age,
        "Professor Phone Number": prof_phone_number,
        "Professor Department": prof_department
    }

    prof_list.append(professor)
    print(f"Professor {prof_name} added successfully!")
    save_profs_to_csv(Dean)
    
def add_students(student_name, student_Age, student_phone_number , Dean):                #finished
    
    student = {
        "Name": student_name,
        "Age": student_Age,
        "Phone Number": student_phone_number
    }
    
    
    student_list.append(student)
    print(f"Student {student_name} added successfully!")
    save_students_to_csv(Dean)
    
def save_students_to_csv(Dean):                                                   #finished
    dean_folder = os.path.join(student_path, Dean)
    os.makedirs(dean_folder, exist_ok=True)  

    file_path = os.path.join(dean_folder, "students.csv")
    fieldnames = ["Name", "Age", "Phone Number"]

    with open(file_path, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(student_list)

    print(f"Students saved successfully under {Dean}'s records!")

def save_profs_to_csv(Dean):                                                      #finished
    dean_folder = os.path.join(prof_path, Dean)
    os.makedirs(dean_folder, exist_ok=True)  

    file_path = os.path.join(dean_folder, "professors.csv")
    fieldnames = ["Professor Name", "Professor Age", "Professor Phone Number", "Professor Department"]

    with open(file_path, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(prof_list)

    print(f"Professors saved successfully under {Dean}'s records!")

def remove_student(student_name, Dean):                                           #finished
    file_path = os.path.join(student_path, Dean, "students.csv")

    if not os.path.exists(file_path):
        print("No students found under this Dean.")
        return

    df = pd.read_csv(file_path)

    if student_name not in df["Name"].values:
        print(f"Student '{student_name}' not found.")
        return

    df = df[df["Name"] != student_name]
    df.to_csv(file_path, index=False)

    print(f"Student '{student_name}' removed successfully.")

def remove_prof(prof_name, Dean):                                                 #finished
    file_path = os.path.join(prof_path, Dean, "professors.csv")

    if not os.path.exists(file_path):
        print("No professors found under this Dean.")
        return

    df = pd.read_csv(file_path)

    if prof_name not in df["Professor Name"].values:
        print(f"Professor '{prof_name}' not found.")
        return

    df = df[df["Professor Name"] != prof_name]
    df.to_csv(file_path, index=False)

    print(f"Professor '{prof_name}' removed successfully.")

def show_students():                                                              #finished
    if not student_list:
        print("No students found.")
        return
    
    All_students = pd.DataFrame(student_list)  
    print(All_students)
    time.sleep(3)
    return All_students 
    
def show_profs():                                                                 #finished
    if not prof_list:
        print("No students found.")
        return
    
        
    all_profs = pd.DataFrame(prof_list)  
    print(all_profs)
    time.sleep(3)
    return all_profs



home = os.path.expanduser("~")
desktop = os.path.join(home, "Desktop")
 
collage_folder = "collage"
collage_path = os.path.join(desktop, collage_folder)

dean_folder= "Dean folder"
dean_path = os.path.join(collage_path, dean_folder)

prof_folder = "professor folder"
prof_path = os.path.join(collage_path, prof_folder)

student_folder = "Student folder"
student_path = os.path.join(collage_path, student_folder)

os.makedirs(collage_path, exist_ok=True)
os.makedirs(dean_path, exist_ok=True)
os.makedirs(prof_path, exist_ok=True)
os.makedirs(student_path, exist_ok=True)




system_window()
