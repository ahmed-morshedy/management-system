import sqlite3

db = sqlite3.connect("app.db")
cr = db.cursor()
# create database file
cr.execute(" create table if not exists student(id INTEGER, name TEXT)")
cr.execute(
    "CREATE TABLE IF NOT EXISTS courses ( courses_name TEXT,grade TEXT,student_id INTEGER )"
)


# commit and close
def commit_and_close():
    db.commit()
    db.close()
    print("Coneection to database Is closed ")


# show data of student
def show_data():
    # if id of student have data
    try:
        user_id = int(input("Enter User Id : ").strip())
        cr.execute(f"select * from student where id={user_id}")
        main_data = cr.fetchone()  # main data have name and id
        print(f"Name of student {main_data[1]}")
        print(f"Id of student {main_data[0]}")
        cr.execute(f"select * from courses where student_id={user_id}")
        result = cr.fetchall()  # have courses and grade
        print(f"The student have {len(result)} courses")
        for row in result:
            print(f"Have Course {row[0]}, and grade {row[1]}%")
    # If id has no data
    except:
        print("=> Sorry This Id has No data to show")
    commit_and_close()


# add data to database
def add_data():
    add_message = """
What Do You Want To Add ?
"C" => Add new cousre
"S" => Add New Student
Choose Option:
"""
    option_list = ["c", "s"]
    user_option = input(add_message).strip().lower()
    if user_option in option_list:
        if user_option == "s":
            add_new_studet()
        elif user_option == "c":
            add_new_course()
    else:
        print("Option Not exists")
    commit_and_close()


# add new student
def add_new_studet():
    user_id = int(input("Enter User Id : ").strip())
    cr.execute(f"select * from student where id={user_id}")
    check_id = cr.fetchone()
    if check_id == None:
        user_name = input("Write Student Name : ").strip().capitalize()
        cr.execute(f" insert into student(id,name) values({user_id},'{user_name}')")
        course = input("Course is : ").strip().capitalize()
        grade = input("Grade is : ").strip()
        cr.execute(
            f"insert into courses(courses_name,grade,student_id) values('{course}','{grade}','{user_id}')"
        )
        print("=> Data Saved")
    else:
        print(
            f"=> You can't add, This Id already exists and \n his name is {check_id[1]}"
        )


# add new course
def add_new_course():
    user_id = int(input("Enter User Id : ").strip())
    course = input("Course is : ").strip().capitalize()
    grade = input("Grade is : ").strip()
    cr.execute(
        f"insert into courses(courses_name,grade,student_id) values('{course}','{grade}','{user_id}')"
    )
    print("=> Data Saved")


# delete student or course
def delete_data():
    user_id = int(input("Enter User Id : ").strip())
    option = input(
        """
's'=> to delete student
'c'=> to delete course
"""
    )
    option_list = ["s", "c"]
    if option in option_list:
        if option == "s":
            cr.execute(f" delete from student where id={user_id}")
        elif option == "c":
            course_name = input("Write Course name : ").strip().capitalize()
            cr.execute(
                f"delete from courses where student_id={user_id} and courses_name='{course_name}'"
            )
    else:
        print("option not available")

    print("=> Student data deleted successfully")
    commit_and_close()


# update grade course
def update_data():
    user_op = (
        input("'n'=> update student name\n'c'=> update course grade\n").strip().lower()
    )
    op_list = ["n", "c"]
    if user_op in op_list:
        if user_op == "c":
            update_course()
        elif user_op == "n":
            update_name()
    else:
        print("option not available")
    commit_and_close()


def update_name():
    user_id = int(input("Enter User Id : ").strip())
    cr.execute(f"select * from student where id={user_id}")
    check_id = cr.fetchone()
    if check_id == None:
        print("No student has This id ")
    else:
        try:
            new_name = input("Write New Student Name : ").strip().capitalize()
            cr.execute(f"update student set name ='{new_name}' where id ={user_id}")
            print("=> Data was changed successfully")
        except:
            print("This Id has no data to update")


def update_course():
    try:
        user_id = int(input("Enter User Id : ").strip())
        cr.execute(f"select * from student where id={user_id}")
        check_id = cr.fetchone()
        if check_id == None:
            print("No student has This id ")
        else:
            course_name = input("Write Course Name : ").strip().capitalize()
            cr.execute(f"select * from courses where student_id='{user_id}'")
            check_course = cr.fetchall()
            if course_name in check_course:
                new_grade = input("Write New grade : ")
                cr.execute(
                    f"update courses set grade ={new_grade} where courses_name='{course_name}'  and student_id ={user_id} "
                )
                print("=> Data was changed successfully")
            else:
                print(f"This Id has no course {course_name}")

    except:
        print("This Id has no data to update")


message = """
What Do You Want To Do ?
"s" => Show All Information about Student
"a" => Add New Student
"d" => Delete A Student or course
"u" => Update information Student
"q" => Quit The App
Choose Option:
"""
commands_list = ["s", "a", "d", "u", "q"]

# choose command
user_input = input(message).strip().lower()

if user_input in commands_list:
    if user_input == "s":
        show_data()
    elif user_input == "a":
        add_data()
    elif user_input == "d":
        delete_data()
    elif user_input == "u":
        update_data()
    else:
        print("App is closed")
        commit_and_close()
else:
    print("The command not found")
    commit_and_close()

