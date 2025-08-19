from user import User
from prompter import yesno
from datetime import datetime
from datetime import timedelta
from datetime import date
class Proffesor(User):
    def __init__(self, user_id , name ,major, password , courses , supervisor_cap , reviewer_cap):
        super().__init__(user_id , name , "proffesor" , major ,  password)
        self.courses = courses
        self.supervisor_cap = supervisor_cap
        self.reviewer_cap = reviewer_cap

    def list_thesis (self , theses, for_defence = False):
        print("Your Requests")
        for thesis in theses:
            if thesis["supervisor_id"] == self.user_id:
                print("____________________________")
                print(f"Thesis ID: {thesis['thesis_id']}\nStudent ID: {thesis['student_id']}\nCourse ID: {thesis['course_id']}\t Major: {thesis['major']}")

                if for_defence and thesis["defence_requested"] == True:
                    print("____________________________")
                    print (f"Status: {thesis['status']}\nRequest date : {thesis['requested_date']}\nYear : {thesis['year']}\tSemester : {thesis['semester']}")
                    print (f"Files: \n\t{thesis['files']['pdf']}\n\t{thesis['files']['first_image']}\n\t{thesis['files']['second_image']}\n")
                    print (f"Keywords: \n\t{thesis['keywords']}\n")
                print("____________________________")


    def see_thesis_request (self ,theses):
        self.list_thesis(theses)
        continue_prog = yesno("Do you want to make changes in any requests?")
        if continue_prog:
            thesis_id_get = input("Enter thesis ID: ")
            for thsis in theses:
                if thsis["thesis_id"] == thesis_id_get:
                    action = yesno("Do you want to approve this thesis request?")
                    if action:
                        thsis['status'] = "approved"
                    else:
                        thsis['status'] = "rejected"
    @staticmethod
    def check_time(request_date , defence_date):
        date_format = "%Y-%m-%d"
        try:
            date1 = datetime.strptime(request_date, date_format)
            date2 = datetime.strptime(defence_date, date_format)
            difference = abs((date2 - date1).days)
            return difference > 90
        except ValueError as e:
            print(f"invalid date: {request_date}.\n{e}")
            return False
    @staticmethod
    def prof_exist(prof , users):
        for user in users:
            if user['id'] == prof and user['role'] == 'proffesor':
                return True
        return False

    @staticmethod
    def check_capacity(prof , users):
        for user in users:
            if user['id'] == prof:
                return user['reviewer_cap'] > 0
        return False

    @staticmethod
    def decrease_cpacity(prof, users):
        for user in users:
            if user['id'] == prof:
                user['reviewer_cap'] -= 1

    def check_major(self ,type , id , users):
        for user in users:
            if user['id'] == id:
                if type == 'Internal':
                    if user['major'] == self.major:
                        return True
                    else:
                        return False
                else:
                    if user['major'] != self.major:
                        return True
                    else:
                        return False




    def add_reviewer(self ,viewer_type, users, thesis):
        viewer_id = input(f"{viewer_type} viewer id: ")

        if not self.check_major(viewer_type , viewer_id, users):
            print ("reviewer should not be " , viewer_type)
            return False

        if not self.prof_exist(viewer_id, users):
            print(f"{viewer_type} viewer id not found.")
            return False

        if not self.check_capacity(viewer_id, users):
            print("This professor has not enough capacity.")
            return False

        thesis["reviewers"].append(viewer_id)
        self.decrease_cpacity(viewer_id, users)
        return True

    def determine_defence_date_and_viewers(self , theses , users):
        self.list_thesis(theses , for_defence = True)
        thesis_search = input("Enter thesis ID: ")
        for thesis in theses:
            if thesis["thesis_id"] == thesis_search:
                defence_date = input("Enter date of defence: ")
                if not self.check_time(thesis['request_date'] , defence_date):
                    print("The defense must be held three months after the request.")
                    return
                else:
                    print("Date is ok.")
                    thesis["defence_date"] = defence_date
                    print ("Defence date determined to " , defence_date)

                self.add_reviewer("Internal", users, thesis)
                self.add_reviewer("External", users, thesis)




    def determine_grade(self ,theses):
        thesis_search = input("Enter thesis ID to grade: ")
        for thesis in theses:
            if not thesis["thesis_id"] == thesis_search:
                continue
            role = None
            if thesis['supervisor_id'] == self.user_id:
                role = "supervisor"
            elif self.user_id in thesis['reviewers'] and thesis['reviewers'][0] == self.user_id:
                role = "internal"
            elif self.user_id in thesis['reviewers'] and thesis['reviewers'][1] == self.user_id:
                role = "external"
            else:
                print (" You are not assigned to this thesis.")
                return

            if not thesis['defence_requested'] and thesis['defence_date']:
                print("This thesis has not yet been requested for defence.")
                return

            defence_date_str = thesis.get("defence_date")
            if not defence_date_str:
                print("Defence date has not been set.")
                return
            try:
                defence_date = datetime.strptime(defence_date_str, "%Y-%m-%d").date()
                today = date.today()
                if today < defence_date:
                    print("Defence date has not arrived yet.")
                    return
            except ValueError:
                print("Invalid defence date format.")
                return

            grade = input("Enter grade: ").strip()
            try:
                grade_value = float(grade)
            except ValueError:
                print("Invalid grade format.")
                return

            if role == "supervisor":
                thesis["evaluation"]["supervisor"] = grade_value
            elif role == "internal_reviewer":
                thesis["evaluation"]["internal_viewer"] = grade_value
            elif role == "external_reviewer":
                thesis["evaluation"]["external_viewer"] = grade_value

            print(f"Grade {grade_value} recorded for role: {role}")
            return

