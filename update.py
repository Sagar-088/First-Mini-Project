import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import mysql.connector
import os

# ✅ Database Connection
def connect_db():
    return mysql.connector.connect(host="localhost", user="your user name", password="password", database="dbname")

def execute_query(query, params=()):
    con = connect_db()
    cursor = con.cursor()
    cursor.execute(query, params)
    con.commit()
    con.close()

# ✅ CRUD Operations
def insert_data():
    execute_query("INSERT INTO students (id, fullname, age, course, gender) VALUES (%s, %s, %s, %s, %s)", 
                  (id_var.get(), name_var.get(), age_var.get(), course_var.get(), gender_var.get()))
    refresh_data("Record inserted successfully!")

def update_data():
    execute_query("UPDATE students SET fullname=%s, age=%s, course=%s, gender=%s WHERE id=%s", 
                  (name_var.get(), age_var.get(), course_var.get(), gender_var.get(), id_var.get()))
    refresh_data("Record updated successfully!")

def delete_data():
    execute_query("DELETE FROM students WHERE id=%s", (id_var.get(),))
    refresh_data("Record deleted successfully!")

def fetch_data():
    con = connect_db()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()
    con.close()
    
    student_table.delete(*student_table.get_children())  
    for row in rows:
        student_table.insert("", tk.END, values=row)

def refresh_data(msg=""):
    fetch_data()
    clear_fields()
    if msg:
        messagebox.showinfo("Success", msg)

def get_selected(event):
    selected_item = student_table.focus()
    values = student_table.item(selected_item, 'values')
    if values:
        id_var.set(values[0])
        name_var.set(values[1])
        age_var.set(values[2])
        course_var.set(values[3])
        gender_var.set(values[4])

def clear_fields():
    id_var.set("")
    name_var.set("")
    age_var.set("")
    course_var.set("")
    gender_var.set("")

# ✅ GUI Setup
root = tk.Tk()
root.title("Student Management System")
root.geometry("800x600")  
root.state("zoomed")  

# ✅ Load Background Image
image_path = r"Image Path" #Change this


resize_id = None  # ✅ Used to cancel previous resize events

def resize_image(event):
    """ Resize background image dynamically but optimize performance """
    global bgv, resize_id
    
    if resize_id:
        root.after_cancel(resize_id)
    
    resize_id = root.after(100, lambda: do_resize(event.width, event.height))

def do_resize(new_width, new_height):
    """ Perform the actual image resize """
    global bgv
    image = Image.open(image_path)
    image = image.resize((new_width, new_height), Image.LANCZOS)
    bgv = ImageTk.PhotoImage(image)
    label1.config(image=bgv)

# ✅ Load Initial Image
if os.path.exists(image_path):
    try:
        image = Image.open(image_path)
        image = image.resize((root.winfo_screenwidth(), root.winfo_screenheight()), Image.LANCZOS)
        bgv = ImageTk.PhotoImage(image)
        label1 = tk.Label(root, image=bgv)
        label1.place(x=0, y=0, relwidth=1, relheight=1)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load image: {str(e)}")
else:
    messagebox.showerror("File Not Found", f"Image file not found: {image_path}")

# ✅ Bind Resize Event
root.bind("<Configure>", resize_image)

# ✅ Variables
id_var, name_var, age_var, course_var, gender_var = tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar()

# ✅ Form
frame = tk.Frame(root, bg="#7be1ff", padx=10, pady=10)
frame.pack(pady=10)

for i, (label, var) in enumerate([("ID", id_var), ("Name", name_var), ("Age", age_var), ("Course", course_var), ("Gender", gender_var)]):
    ttk.Label(frame, text=label).grid(row=i, column=0, padx=5, pady=5)
    ttk.Entry(frame, textvariable=var, width=30).grid(row=i, column=1, padx=5, pady=5)

# ✅ Buttons
button_frame = tk.Frame(root, bg="#7be1ff")
button_frame.pack(pady=10)
for i, (text, command) in enumerate([("Insert", insert_data), ("Update", update_data), 
                                     ("Delete", delete_data), ("Clear", clear_fields)]):
    ttk.Button(button_frame, text=text, command=command).grid(row=0, column=i, padx=10)

# ✅ Table
columns = ("id", "fullname", "age", "course", "gender")
student_table = ttk.Treeview(root, columns=columns, show="headings", height=10)
for col in columns:
    student_table.heading(col, text=col.capitalize())
    student_table.column(col, width=120, anchor="center")
student_table.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
student_table.bind("<ButtonRelease-1>", get_selected)

# ✅ Fetch Data Initially
fetch_data()

# ✅ Start GUI
root.mainloop()
