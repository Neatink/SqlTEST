import sqlite3


conn = sqlite3.connect("testdb.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER,
    major TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS courses (
    course_id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_name TEXT NOT NULL,
    instructor TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS student_courses (
    student_id INTEGER,
    course_id INTEGER,
    FOREIGN KEY (student_id) REFERENCES students(id),
    FOREIGN KEY (course_id) REFERENCES courses(course_id),
    PRIMARY KEY (student_id, course_id)
)
""")

conn.commit()

def add_student(name, age, major):
    cursor.execute("INSERT INTO students (name, age, major) VALUES (?, ?, ?)", (name, age, major))
    conn.commit()
    print("Студент доданий успішно!")

def add_course(course_name, instructor):
    cursor.execute("INSERT INTO courses (course_name, instructor) VALUES (?, ?)", (course_name, instructor))
    conn.commit()
    print("Курс доданий успішно!")

def enroll_student(student_id, course_id):
    cursor.execute("INSERT INTO student_courses (student_id, course_id) VALUES (?, ?)", (student_id, course_id))
    conn.commit()
    print("Студент записаний на курс!")

def list_students():
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    for student in students:
        print(student)

def list_courses():
    cursor.execute("SELECT * FROM courses")
    courses = cursor.fetchall()
    for course in courses:
        print(course)

def list_students_in_course(course_id):
    cursor.execute("""
    SELECT students.id, students.name FROM students
    JOIN student_courses ON students.id = student_courses.student_id
    WHERE student_courses.course_id = ?
    """, (course_id,))
    students = cursor.fetchall()
    for student in students:
        print(student)

def main():
    while True:
        print("\nМеню:")
        print("1. Додати студента")
        print("2. Додати курс")
        print("3. Записати студента на курс")
        print("4. Показати всіх студентів")
        print("5. Показати всі курси")
        print("6. Показати студентів у курсі")
        print("7. Вийти")
        
        choice = input("Виберіть опцію: ")
        
        if choice == "1":
            name = input("Введіть ім'я студента: ")
            age = int(input("Введіть вік студента: "))
            major = input("Введіть спеціальність студента: ")
            add_student(name, age, major)
        elif choice == "2":
            course_name = input("Введіть назву курсу: ")
            instructor = input("Введіть ім'я викладача: ")
            add_course(course_name, instructor)
        elif choice == "3":
            student_id = int(input("Введіть ID студента: "))
            course_id = int(input("Введіть ID курсу: "))
            enroll_student(student_id, course_id)
        elif choice == "4":
            list_students()
        elif choice == "5":
            list_courses()
        elif choice == "6":
            course_id = int(input("Введіть ID курсу: "))
            list_students_in_course(course_id)
        elif choice == "7":
            break
        else:
            print("Невірний вибір. Спробуйте ще раз.")

    conn.close()

if __name__ == "__main__":
    main()
