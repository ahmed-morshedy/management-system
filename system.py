import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

db = sqlite3.connect("app.db")
cr = db.cursor()


def show_data_window():
    show_window = tk.Toplevel()
    show_window.title("Show Student Data")
    show_window.geometry("300x320")

    def show_data():
        user_id = int(entry_id.get())
        data_text.delete(1.0, tk.END)  # Clear previous data
        try:
            cr.execute(f"SELECT * FROM student WHERE id={user_id}")
            main_data = cr.fetchone()

            if main_data:
                data_text.insert(
                    tk.END,
                    f"Name : {main_data[1]}\nId : {main_data[0]}\n",
                )
                cr.execute(f"SELECT * FROM courses WHERE student_id={user_id}")
                result = cr.fetchall()
                data_text.insert(tk.END, f"The student has {len(result)} courses\n")
                for idx, row in enumerate(result, start=1):
                    data_text.insert(
                        tk.END, f"Course {idx}: {row[0]}, Grade: {row[1]}%\n"
                    )
            else:
                data_text.insert(tk.END, "No data found for this ID")

        except sqlite3.Error as e:
            data_text.insert(tk.END, f"Error: {str(e)}")

    label_id = ttk.Label(show_window, text="Enter Student Id:")
    label_id.pack(pady=10)

    entry_id = ttk.Entry(show_window)
    entry_id.pack()

    show_button = ttk.Button(show_window, text="Show Data", command=show_data)
    show_button.pack(pady=10, ipadx=5, ipady=3)

    data_text = tk.Text(show_window, height=10, width=40, font=" arial 10 bold")
    data_text.pack()

    # close window
    def close():
        show_window.destroy()

    close_button = ttk.Button(show_window, text="Close Window", command=close)
    close_button.pack(pady=10, ipadx=5, ipady=2)


def add_data_window():
    add_window = tk.Toplevel()
    add_window.title("Add Student Data")
    add_window.geometry("250x240")

    # new student
    def add_new_student(user_id):
        sub_window = tk.Toplevel()
        sub_window.title("Add New Student")
        sub_window.geometry("200x270")

        label_name = ttk.Label(sub_window, text="Enter Student Name:")
        label_name.pack(pady=10)
        entry_name = ttk.Entry(sub_window)
        entry_name.pack()

        label_course = ttk.Label(sub_window, text="Choose Course:")
        label_course.pack(pady=10)
        courses = ttk.Combobox(sub_window, values=["Is", "Math", "Al Ahly"])
        courses.pack(pady=5)

        label_grade = ttk.Label(sub_window, text="Enter Grade:")
        label_grade.pack(pady=10)
        entry_grade = ttk.Entry(sub_window)
        entry_grade.pack()

        # save add
        def save_add():
            try:
                user_name = entry_name.get().capitalize()
                course = courses.get()
                grade = entry_grade.get()
                cr.execute(
                    "INSERT INTO student(id, name) VALUES (?, ?)", (user_id, user_name)
                )
                cr.execute(
                    "INSERT INTO courses(courses_name, grade, student_id) VALUES (?, ?, ?)",
                    (course, grade, user_id),
                )
                db.commit()
                message = messagebox.showinfo("status", "data saves successfully")
                if message:
                    sub_window.destroy()
            except sqlite3.Error as e:
                messagebox.showerror("Error", f"{str(e)}")

        save_button = ttk.Button(sub_window, text="Save", command=save_add)
        save_button.pack(pady=10, ipadx=10, ipady=3)

        # add new course

    def add_new_course(user_id):
        sub_window = tk.Toplevel()
        sub_window.title("Add Course")
        sub_window.geometry("250x220")

        def save_add():
            course = courses.get().capitalize()
            grade = entry_grade.get().strip()
            if grade == "" or course == "":
                messagebox.showerror("Empty", "You should fill labels")
            else:
                cr.execute(
                    "SELECT courses_name FROM courses WHERE student_id=?", (user_id,)
                )
                existing_course = cr.fetchall()
                if tuple([course]) in existing_course:
                    messagebox.showerror("existing course", "This course already exist")
                else:
                    cr.execute(
                        f"insert into courses(courses_name,grade,student_id) values('{course}','{grade}','{user_id}')"
                    )
                    db.commit()
                    message = messagebox.showinfo("saved", "Data added successfully")

        label_course = ttk.Label(sub_window, text="Choose Course:")
        label_course.pack(pady=10)
        courses = ttk.Combobox(sub_window, values=["Is", "Math", "Al Ahly"])
        courses.pack(pady=5)

        label_grade = ttk.Label(sub_window, text="Enter Grade:")
        label_grade.pack(pady=10)
        entry_grade = ttk.Entry(sub_window)
        entry_grade.pack()

        save_button = ttk.Button(sub_window, text="Save", command=save_add)
        save_button.pack(pady=10, ipadx=10, ipady=3)

        def close():
            sub_window.destroy()

        close_window = ttk.Button(sub_window, text="close window", command=close)
        close_window.pack(ipadx=10, ipady=3)

    # check id
    def check():
        user_id = int(entry_id.get())
        stat = status.get().lower()
        if stat == "course":
            add_window.destroy()
            add_new_course(user_id)
        else:
            cr.execute("SELECT id FROM student WHERE id=?", (user_id,))
            existing_id = cr.fetchone()

            if existing_id:
                messagebox.showerror("exists", "ID already exists")
            else:
                add_window.destroy()
                add_new_student(user_id)

    label_id = ttk.Label(add_window, text="Enter User Id:")
    label_id.pack(pady=10)
    entry_id = ttk.Entry(add_window)
    entry_id.pack()
    label_course = ttk.Label(add_window, text="Chose :")
    label_course.pack(pady=10)
    status = ttk.Combobox(add_window, values=["course", "Student"])
    status.pack(pady=5)

    add_button = ttk.Button(add_window, text="Continue", command=check)
    add_button.pack(pady=10, ipadx=10, ipady=3)

    # close window
    def close():
        add_window.destroy()

    close_window = ttk.Button(add_window, text="Close Window", command=close)
    close_window.pack(ipadx=10, ipady=3)


def delete_data_window():
    delete_window = tk.Toplevel()
    delete_window.title("Delete Student Data")
    delete_window.geometry("190x180")

    def delete_student():
        try:
            user_id = int(entry_id.get())
            cr.execute(f"DELETE FROM student WHERE id=?", (user_id,))
            cr.execute(f"DELETE FROM courses WHERE student_id=?", (user_id,))
            db.commit()
            messagebox.showinfo("success", "Student data deleted successfully")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"{str(e)}")

    label_id = ttk.Label(delete_window, text="Enter User Id:")
    label_id.pack(pady=10, ipadx=10)

    entry_id = ttk.Entry(delete_window)
    entry_id.pack()

    delete_button = ttk.Button(
        delete_window, text="Delete Student Data", command=delete_student
    )
    delete_button.pack(pady=10, ipadx=10, ipady=3)

    # close window
    def close():
        delete_window.destroy()

    close_button = ttk.Button(delete_window, text="Close Window", command=close)
    close_button.pack(ipadx=10, ipady=3)


def update_data_window():
    update_window = tk.Toplevel()
    update_window.title("Update Student Data")
    update_window.geometry("200x230")

    def update_student_name(user_id):
        sub_window = tk.Toplevel()
        sub_window.title("Change Name")
        sub_window.geometry("200x150")

        name_label = tk.Label(sub_window, text="New Name :")
        name_label.pack(pady=10)

        entry_name = tk.Entry(sub_window)
        entry_name.pack()

        def change():
            try:
                new_name = entry_name.get().capitalize()
                cr.execute(f"UPDATE student SET name=? WHERE id=?", (new_name, user_id))
                db.commit()
                messagebox.showinfo("success", "Student name Updated successfully")
                sub_window.destroy()
            except sqlite3.Error as e:
                messagebox.showerror("Error", f"{str(e)}")

        change_button = ttk.Button(sub_window, text="Change", command=change)
        change_button.pack(pady=10, ipadx=10, ipady=3)

        def close():
            sub_window.destroy()

        change_button = ttk.Button(sub_window, text="Close Window", command=close)
        change_button.pack(ipadx=10, ipady=3)

    def update_course(user_id):
        sub_window = tk.Toplevel()
        sub_window.title("Update Course")
        sub_window.geometry("250x230")

        course_label = tk.Label(sub_window, text="Chose Course :")
        course_label.pack(pady=10)

        chose_course = ttk.Combobox(sub_window, values=["Is", "Math", "Al Ahly"])
        chose_course.pack()

        grade_label = tk.Label(sub_window, text="New Grade :")
        grade_label.pack(pady=10)

        get_grade = tk.Entry(sub_window)
        get_grade.pack()

        def save():
            new_grade = int(get_grade.get())
            get_course = chose_course.get().capitalize()
            cr.execute(
                "SELECT courses_name FROM courses WHERE student_id=?", (user_id,)
            )
            existing_course = cr.fetchall()
            if tuple([get_course]) not in existing_course:
                messagebox.showerror("Not Existing ", "This course Not Exist")
            else:
                cr.execute(
                    f"UPDATE courses SET grade=? WHERE student_id=? and courses_name=?",
                    (new_grade, user_id, get_course),
                )
                db.commit()
                messagebox.showinfo("Update", "Grade Updated successfully")

        save_button = ttk.Button(sub_window, text="Update", command=save)
        save_button.pack(ipadx=10, ipady=3, pady=10)

        def close():
            sub_window.destroy()

        change_button = ttk.Button(sub_window, text="Close Window", command=close)
        change_button.pack(ipadx=10, ipady=3)

    def state():
        user_id = entry_id.get()
        get_state = status.get().lower()
        if get_state == "" or user_id == "":
            messagebox.showerror("Empty", "You should fill labels")
        else:
            cr.execute("SELECT id FROM student WHERE id=?", (user_id,))
            existing_id = cr.fetchone()
            if existing_id:
                if get_state == "course":
                    update_window.destroy()
                    update_course(user_id)
                else:
                    update_window.destroy()
                    update_student_name(user_id)
            else:
                messagebox.showerror(" Not Exists", "ID Not Exists")

    label_id = ttk.Label(update_window, text="Enter User Id:")
    label_id.pack(pady=10)

    entry_id = ttk.Entry(update_window)
    entry_id.pack()

    label_status = ttk.Label(update_window, text="chose:")
    label_status.pack(pady=10)

    status = ttk.Combobox(update_window, values=["course", "Student Name"])
    status.pack(pady=5)

    update_button = ttk.Button(update_window, text="Contiune", command=state)
    update_button.pack(pady=10, ipadx=10, ipady=3)

    def close():
        update_window.destroy()

    change_button = ttk.Button(update_window, text="Close Window", command=close)
    change_button.pack(ipadx=10, ipady=3)


# Create the main Tkinter window
root = tk.Tk()
root.title("Student Management System")
root.geometry("350x250")
show_button = ttk.Button(root, text="Show Data", command=show_data_window, width=12)
show_button.pack(pady=10, ipady=5, ipadx=2)

add_button = ttk.Button(root, text="Add Data", command=add_data_window, width=12)
add_button.pack(ipady=5, ipadx=2)

delete_button = ttk.Button(
    root, text="Delete Data", command=delete_data_window, width=12
)
delete_button.pack(pady=10, ipady=5, ipadx=2)

update_button = ttk.Button(
    root, text="Update Data", command=update_data_window, width=12
)
update_button.pack(ipady=5, ipadx=2)


# close root window
def close_root():
    root.destroy()


close_button = ttk.Button(root, text="Close App", command=close_root, width=12)
close_button.pack(ipady=5, pady=10, ipadx=2)

root.mainloop()
db.close()
