import sqlite3
import tkinter as tk
from tkinter import messagebox
import csv

#Database detup
conn = sqlite3.connect('student.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY,
    name TEXT,
    branch TEXT,
    marks INTEGER
)''')
conn.commit()

def add_student():
    try:
      id = int(entry_id.get())
      name = entry_name.get()
      branch = entry_branch.get()
      marks = int(entry_marks.get())
  
      c.execute("INSERT INTO students VALUES (?, ?, ?, ?)", (id, name, branch, marks))
      conn.commit()
      messagebox.showinfo("Success", "Student added successfully!")
    except Exception as e:
      messagebox.showerror("Error", str(e))

def view_students():
    c.execute("SELECT * FROM students")
    records = c.fetchall()
    output_text.delete(1.0, tk.END)
    for row in records:
        output_text.insert(tk.END, f"{row}\n")

def search_student():
  id_input = entry_id.get().strip()
  name_input = entry_name.get().strip()

  output_text.delete('1.0', tk.END)

  if id_input:
    try:
      id_val = int(id_input)
      c.execute("SELECT * FROM students WHERE id=?", (int(id_val),))
      row = c.fetchone()
    except ValueError:
      output_text.insert(tk.END, "Invalid ID format!\n")
      return

  elif name_input:
    c.execute("SELECT * FROM students WHERE name=?", (name_input,))
    row = c.fetchone()
  else:
    output_text.insert(tk.END, "Please enter either ID or Name to search!\n")
    return

  if row:
    output_text.insert(tk.END, f"Student Found: {row}\n")
  else:
    output_text.insert(tk.END, "Student not found!\n")

def delete_student():
  try:
    id = int(entry_id.get())
    c.execute("DELETE FROM students WHERE id=?", (id,))
    conn.commit()
    messagebox.showinfo("Deleted", "Student deleted successfully!")
  except ValueError:
    messagebox.showerror("Error", "Invalid ID")

def export_to_csv():
  c.execute("SELECT * FROM students")
  rows = c.fetchall()
  if not rows:
    messagebox.showinfo("No Data", "No data to export.")
    return
  with open('students_export.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['ID', 'Name', 'Branch', 'Marks'])
    writer.writerows(rows)
  messagebox.showinfo("Success", "Data exported to students_export.csv successfully!")

# GUI setup
root = tk.Tk()
root.title("Student Profile Manager")
root.geometry("500x500")

#Entry fields
tk.Label(root, text="ID").pack()
entry_id = tk.Entry(root)
entry_id.pack()

tk.Label(root, text="Name").pack()
entry_name = tk.Entry(root)
entry_name.pack()

tk.Label(root, text="Branch").pack()
entry_branch = tk.Entry(root)
entry_branch.pack()

tk.Label(root, text="Marks").pack()
entry_marks = tk.Entry(root)
entry_marks.pack()

#Buttons
tk.Button(root, text="Add Student", command=add_student).pack(pady=5)
tk.Button(root, text="View Students", command=view_students).pack(pady=5)
tk.Button(root, text="Search Student", command=search_student).pack(pady=5)
tk.Button(root, text="Delete Student", command=delete_student).pack(pady=5)
tk.Button(root, text="Export to CSV", command=export_to_csv).pack(pady=5)

#Output text
output_text = tk.Text(root, height=10, width=50)
output_text.pack(pady=10)

root.mainloop()
conn.close()