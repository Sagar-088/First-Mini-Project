import tkinter as tk
import mysql.connector
from tkinter import messagebox

import os
from dotenv import load_dotenv

load_dotenv()
 
host = os.getenv('HOST') # Change to your MySQL server IP if remote
user = os.getenv('USER') # Replace with your MySQL username
password = os.getenv('PASSWORD') # Replace with your MySQL password
database = os.getenv('DATABASE') # Replace with your database name


# Function to establish connection
def establish_connection():
    try:
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        return conn
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
        return None

# Function to show all records in a message box
def show_table():
    conn = establish_connection()
    if conn is None:
        return
    cur = conn.cursor()
    cur.execute("SELECT * FROM students")
    result = cur.fetchall()
    conn.close()

    if not result:
        messagebox.showinfo("Info", "No records found!")
        return

    data = "\n".join([f"ID: {rec[0]}, Name: {rec[1]}, Age: {rec[2]}, Course: {rec[3]}, Gender: {rec[4]}" for rec in result])
    messagebox.showinfo("Student Records", data)

# Function to delete a record by ID
def delete():
    id = entry_id.get()
    if not id.isdigit():
        messagebox.showerror("Error", "Invalid ID! Please enter a numeric ID.")
        return

    conn = establish_connection()
    if conn is None:
        return
    cursor = conn.cursor()
    
    delete_query = "DELETE FROM students WHERE id = %s"
    cursor.execute(delete_query, (id,))
    conn.commit()
    
    if cursor.rowcount == 0:
        messagebox.showinfo("Info", "No record found with the given ID.")
    else:
        messagebox.showinfo("Success", "Record deleted successfully!")

    cursor.close()
    conn.close()

# Function to save student details
def save():

    id = entry_id.get()
    name = entry_name.get()
    age = entry_age.get()
    course = entry_course.get()
    gender = entry_gender.get()

    if not (id and name and age and course and gender):
        messagebox.showwarning("Warning", "Please fill all fields")
        return

    if not id.isdigit() or not age.isdigit():
        messagebox.showerror("Error", "ID and Age must be numeric values.")
        return

    try:
        conn = establish_connection()
        if conn is None:
            return
        cursor = conn.cursor()

        insert_query = """
        INSERT INTO students (id, fullname, age, course, gender)
        VALUES (%s, %s, %s, %s, %s)
        """
        
        cursor.execute(insert_query, (id, name, age, course, gender))
        conn.commit()
        cursor.close()
        conn.close()

        messagebox.showinfo("Success", "Student details saved to database!")

        # Clear input fields
        entry_id.delete(0, tk.END)
        entry_name.delete(0, tk.END)
        entry_age.delete(0, tk.END)
        entry_course.delete(0, tk.END)
        entry_gender.delete(0, tk.END)

    except mysql.connector.IntegrityError:
        messagebox.showerror("Database Error", "ID already exists! Use a unique ID.")
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")

def update_table():
    id = entry_id.get()
    name = entry_name.get()
    age = entry_age.get()
    course = entry_course.get()
    gender = entry_gender.get()

    if not (id and name and age and course and gender):
        messagebox.showwarning("Warning", "Please fill all fields")
        return

    if not id.isdigit() or not age.isdigit():
        messagebox.showerror("Error", "ID and Age must be numeric values.")
        return

    try:
        conn = establish_connection()
        if conn is None:
            return
        cursor = conn.cursor()

        update_query = """
        UPDATE students 
        SET fullname = %s, age = %s, course = %s, gender = %s  
        WHERE id = %s
        """
        
        cursor.execute(update_query, (name, age, course, gender, id))  # Corrected order of parameters
        conn.commit()

        if cursor.rowcount == 0:
            messagebox.showinfo("Info", "No record found with the given ID.")
        else:
            messagebox.showinfo("Success", "Student details updated!")

        cursor.close()
        conn.close()

        # Clear input fields
        entry_id.delete(0, tk.END)
        entry_name.delete(0, tk.END)
        entry_age.delete(0, tk.END)
        entry_course.delete(0, tk.END)
        entry_gender.delete(0, tk.END)

    except mysql.connector.IntegrityError:
        messagebox.showerror("Database Error", "ID already exists! Use a unique ID.")
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")


# GUI Setup
root = tk.Tk()
root.title("Student Form")
root.geometry("400x500")

tk.Label(root, text="ID:").grid(row=0, column=0, padx=30, pady=15)
entry_id = tk.Entry(root)
entry_id.grid(row=0, column=1)

tk.Label(root, text="Name:").grid(row=1, column=0, padx=30, pady=15)
entry_name = tk.Entry(root)
entry_name.grid(row=1, column=1)

tk.Label(root, text="Age:").grid(row=2, column=0, padx=30, pady=15)
entry_age = tk.Entry(root)
entry_age.grid(row=2, column=1)

tk.Label(root, text="Course:").grid(row=3, column=0, padx=30, pady=15)
entry_course = tk.Entry(root)
entry_course.grid(row=3, column=1)

tk.Label(root, text="Gender:").grid(row=4, column=0, padx=30, pady=15)
entry_gender = tk.Entry(root)
entry_gender.grid(row=4, column=1)


tk.Button(root, text="Save", command=save).grid(row=5, column=1, pady=5)
tk.Button(root, text="Delete", command=delete).grid(row=6, column=1, pady=5)
tk.Button(root, text="Show", command=show_table).grid(row=7, column=1, pady=5)
tk.Button(root, text="Update", command=update_table).grid(row=8, column=1, pady=5)


root.mainloop()
