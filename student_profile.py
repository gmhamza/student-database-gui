import sqlite3
import csv

conn = sqlite3.connect('student.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY,
    name TEXT,
    branch TEXT,
    marks INTEGER
)''')

def add_student():
  id = int(input("Enter ID: "))
  name = input("Enter Name: ")
  branch = input("Enter Branch: ")
  marks = int(input("Enter Marks: "))
  c.execute("INSERT INTO students VALUES (?, ?, ?, ?)", (id, name, branch, marks))
  conn.commit()
  print("Student added successfully!")

def view_students():
  c.execute("SELECT * FROM students")
  rows = c.fetchall()
  for row in rows:
    print(row)
  print("Student data viewed successfully!")

def search_student():
  name = input("Enter Name: ")
  c.execute("SELECT * FROM students WHERE name=?", (name,))
  row = c.fetchone()
  if row:
    print(row)
  else:
    print("Student not found!\n")

def delete_student():
  id = int(input("Enter ID: "))
  c.execute("DELETE FROM students WHERE id=?", (id,))
  conn.commit()
  print("Student deleted successfully!")

def export_to_csv():
  c.execute("SELECT * FROM students")
  rows = c.fetchall()

  if not rows:
    print("No data to export.\n")
    return

  with open('students_export.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['ID', 'Name', 'Branch', 'Marks'])
    writer.writerows(rows)

  print("Data exported to students_export.csv successfully!")
  

while True:
  print("\n1. Add Student")
  print("2. View Students")
  print("3. Search Student")
  print("4. Delete Student")
  print("5. Export to CSV")
  print("6. Exit")

  try:
    choice = int(input("Enter your choice: "))
  except ValueError:
    print("Please enter a valid number.")
    continue

  if choice == 1:
    add_student()
  elif choice == 2:
    view_students()
  elif choice == 3:
    search_student()
  elif choice == 4:
    delete_student()
  elif choice == 5:
    export_to_csv()
  elif choice == 6:
    break
  else:
    print("Invalid choice\n")

conn.close()