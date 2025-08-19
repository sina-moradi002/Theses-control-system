import json
import file_manager
import user
import student
import proffesor
import thesis
import course

def print_courses(courses):
    for course in courses:
        print(f"course id: {course['course_id']}\ttopic: {course['topic']}\tsupervisor id: {course['supervisor']}\tyear : {course['year']}\tsemester: {course['semester']}\tcapacity: {course['capacity']}\tresources: {course['resource'][0]}  {course['resource'][1]}\tunits: {course['units']}")

def course_maker (courses , id):
    for cour in courses:
        if cour['id'] == id:
            obj = course.Course(cour["id"] , cour["title"] , cour["professor_id"] , cour["year"] , cour["semester"] , cour["capacity"] , cour["resources"] , cour["units"] )
            return obj

def is_supervisor (users , ID):
    for user in users:
        if user["id"] == ID and user["role"] == "proffesor":
            return True
    return False

def is_course (courses , ID):
    for course in courses:
        if course["id"] == ID:
            return True
    return False

def is_present(users , ID , course_ID):
    for user in users:
        if user["id"] == ID and course_ID in user["courses"]:
            return True
    return False

def supervisor_capacity (users , ID):
    for user in users:
        if user["id"] == ID and user["capacity"] > 0:
            return True
    return False

def course_capacity (courses , ID):
    for course in courses:
        if course["id"] == ID and course["capacity"] > 0:
            return True
    return False

def is_same_major(users , ID , user):
    for person in users:
        if person["id"] == ID:
            if person["major"] == user["major"]:
                return True
    return False


def student_panel(users , user , courses , theses):
    stu = student.Student(user["id"], user["name"], user['major'] , user["password"])
    print(f"Student Panel\n Welcome dear {user['name']}")
    while True:
        action = input("1 = Request for thesis course\n 2 = View thesis course status\n3 = Request for defence\n4 = Search theses\n5 = log out\nChoose an action: ")
        if action == "1":
            course_in = input("Enter course id : ")
            supervisor_in = input("Enter supervisor id : ")

            if not is_course(courses , course_in):
                print("Invalid course id")
                continue

            if not is_supervisor(users , supervisor_in):
                print("Invalid supervisor id")
                continue

            if not is_same_major (users , supervisor_in , user):
                print("You should choose a supervisor from your major")
                continue

            if not is_present(users , supervisor_in, course_in):
                print("This peroffesor doen't present this course")
                continue

            if not supervisor_capacity(users , supervisor_in):
                print ("This supervisor doesn't have enough capacity")
                continue

            if not course_capacity (courses , course_in):
                print("This course doesn't have enough capacity")
                continue

            print ("This course is available")
            course = course_maker(courses , course_in)
            stu.request_thesis(course , supervisor_in ,theses)


        elif action == "2":
            stu.view_status(theses)
        elif action == "3":
            is_upload = stu.upload_doc(theses)
            if is_upload:
                stu.defence_request(theses)
        elif action == "4":
            pass
        elif action == "5":
            break
        else:
            print("Invalid input")



def proffesor_panel(users , user , courses ,theses):
    prof = proffesor.Proffesor(user["id"], user["name"], user['major'] , user["password"] , user["course"] , user["supervisor_capacity"] , user["reviewer_capacity"])
    print(f"Profesor Panel\n Welcome dear {user['name']}")
    action = ''
    while True:
        action = input ("1 = View theses requests\n2 = View defence requests\n3 = Search theses\n4 = Grade recording\n5 = log out\nChoose an action: ")
        if action == "1":
            prof.see_thesis_request(theses)
        elif action == "2":
            prof. determine_defence_date_and_viewers(theses, users)
        elif action == "3":
            pass
        elif action == "4":
            prof.determine_grade(theses)
        elif action == "5":
            break
        else:
            print("Invalid input")


print ("==================")
print ("|    Main Manu   |")
print ("==================")

# Loading files
users_data = file_manager.FileManager()
data_dict = users_data.load_file("../data/users.json")
users = data_dict["users"]

theses_data = file_manager.FileManager()
theses_dict = theses_data.load_file("../data/theses.json")
theses = theses_dict["theses"]

courses_data = file_manager.FileManager()
courses_dict = courses_data.load_file("../data/courses.json")
courses = courses_dict["courses"]


# Log in panel
while True:
    action = input("1 = log in\n0 = exit\nChoose an action: ")
    if action == "1":
        username_input = input("Enter your username: ")
        password_input = input("Enter your password: ")
        login = False
        role = ''
        found = False
        for user in users:
            if user["id"] == username_input and user["password"] == password_input:
                found = True
                print(f"Dear {user['name']}, you are logged in")
                role = user["role"]
                if role == 'student':
                    student_panel(users , user , courses ,theses)
                if role == 'professor':
                    proffesor_panel(users , user , courses , theses)

        if not found:
            print("Invalid username or password")

    elif action == "0":
        print("Goodbye")
        exit()
    else:
        print("Invalid input. Try again!")