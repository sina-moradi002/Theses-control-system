import json
import file_manager
import user
import student
import proffesor
import thesis
import course
import search_engine

def print_courses(courses):
    for course in courses:
        print(f"course id: {course['course_id']}\ttopic: {course['topic']}\tsupervisor id: {course['supervisor']}\tyear : {course['year']}\tsemester: {course['semester']}\tcapacity: {course['capacity']}\tresources: {course['resource'][0]}  {course['resource'][1]}\tunits: {course['units']}")

def course_maker (courses , id_in):
    for cour in courses:
        if cour['id'] == id_in:
            obj = course.Course(cour["id"] , cour["title"] , cour["professor_id"] , cour['major'] , cour["year"] , cour["semester"] , cour["capacity"] , cour["resources"] , cour["units"] )
            return obj

def is_supervisor (users , id_in):
    for User in users:
        if User["id"] == id_in and User["role"] == "professor":
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

def supervisor_capacity (users , id_in):
    for user in users:
        if user["id"] == id_in and user["supervision_capacity"] > 0:
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

def check_if_request_accepted(thesis_id , theses_list):
    for thesis in theses_list:
        if thesis["thesis_id"] == thesis_id and thesis["status"] == "approved":
            return True
    return False

def print_courses(courses):
    for course in courses:
        print("\n___________________________")
        print(course['title'])
        print(f"ID : {course['id']}")
        print(f"Title: {course['title']}")
        print(f"professor : {course['professor_id']}")
        print (f"year : {course['year']}")
        print(f"semester : {course['semester']}")
        print(f"capacity : {course['capacity']}")
        print(f"Resources:\n\t {course['resources'][0]} \n\t {course['resources'][1]}")
        print(f"units: {course['units']}")


def student_panel(users , user , courses , theses):
    stu = student.Student(user["id"], user["name"], user['major'] , user["password"], user["thesis_request"])

    while True:
        print(f"\nStudent Panel\n Welcome dear {user['name']}")
        action = input("1 = Request for thesis course\n2 = View thesis course status\n3 = Request for defence\n4 = Search theses\n5 = Change Password\n6 = log out\nChoose an action: ")
        if action == "1":
            print_courses(courses)
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
                print ( "This supervisor doesn't have enough capacity")
                continue

            if not course_capacity (courses , course_in):
                print("This course doesn't have enough capacity")
                continue

            print ("This course is available")
            course_obj = course_maker(courses , course_in)
            stu.request_thesis(courses, course_obj , supervisor_in , theses , users)
            print ("Your request has been registered.")

        elif action == "2":
            stu.view_status(theses)
        elif action == "3":
            if check_if_request_accepted (stu.thesis_request , theses ):
                is_upload = stu.upload_doc(theses)
                if is_upload:
                    stu.defence_request(theses)
            else:
                print ("Your request should approve by supervision first")
        elif action == "4":
            search_engine.search(theses)
        elif action == "5":
            stu.change_password(users)
        elif action == "6":
            user ['thesis_request'] = stu.thesis_request
            break
        else:
            print("Invalid input")



def proffesor_panel(users , user , courses ,theses):
    prof = proffesor.Proffesor(user["id"], user["name"], user['major'] , user["password"] , user["courses"] , user["supervision_capacity"] , user["review_capacity"])
    action = ''
    while True:
        print(f"\nProfesor Panel\n Welcome dear {user['name']}")
        action = input ("1 = View theses requests\n2 = View defence requests\n3 = Search theses\n4 = Grade recording\n5 = Change Password\n6 = log out\nChoose an action: ")
        if action == "1":
            prof.see_thesis_request(theses)
        elif action == "2":
            prof. determine_defence_date_and_viewers(theses, users)
        elif action == "3":
            search_engine.search(theses)
        elif action == "4":
            prof.determine_grade(theses)
        elif action == "5":
            prof.change_password(users)
        elif action == "6":
            break
        else:
            print("Invalid input")



def main():
    print("==================")
    print("|    Main Manu   |")
    print("==================")

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
                        student_panel(users, user, courses, theses)
                    if role == 'professor':
                        proffesor_panel(users, user, courses, theses)

            if not found:
                print("Invalid username or password")

        elif action == "0":
            print("Goodbye")
            users_data.save_file("../data/users.json" , users , key = "users")
            theses_data.save_file("../data/theses.json" , theses , key = "theses")
            courses_data.save_file("../data/courses.json" , courses , key = "courses")
            exit()
        else:
            print("Invalid input. Try again!")


if __name__ == "__main__":
    main()