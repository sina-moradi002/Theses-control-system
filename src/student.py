from shutil import SameFileError
from user import User
from thesis import Thesis
from datetime import datetime , date , timedelta
from prompter import yesno
import shutil
import os

class Student(User):
    def __init__(self, user_id , name , major ,  password):
        super().__init__(user_id , name , "student" ,major , password)
        self.thesis_request = None

    def thesis_id_create (self, course_id , supervisor_id):
        return f"{self.user_id[-3:]}{course_id[-3:]}-{supervisor_id[-3:]}"

    @staticmethod
    def keyword_getter():
        l =[]
        number = input("How many keywords do you have?")
        for i in range(int(number)):
            keyword=input("Enter keyword :")
            l.append(keyword)
        return l

    @staticmethod
    def print_basic_thesis_info (thesis):
        print("Thesis Information")
        print("----------------------")
        print(f"Thesis ID : {thesis['thesis_id']}")
        print(f"Thesis course ID : {thesis['course_id']}")
        print(f"Thesis supervisor ID : {thesis['supervisor_id']}")
        print(f"Thesis major : {thesis['major']}")
        print(f"Thesis year : {thesis['year']}", end='\t')
        print(f"Thesis semester : {thesis['semester']}")
        print(f"Thesis request date : {thesis['request_date']}")


    def is_new_thesis(self , new_id , theses ):
        for thesis in theses:
            if thesis['thesis_id'] == new_id and thesis['status'] != 'rejected':
                print("This thesis has been created before")
                return False
            elif thesis['thesis_id'] == new_id and thesis['status'] == 'rejected':
                print("This thesis has been rejected")
                wanna_new_thesis = yesno("Do you want to create a new thesis?")
                if wanna_new_thesis:
                    theses.remove(thesis)
                    self.thesis_request = None
                    # increasing capacity of prof and course
                else:
                    print("You can not create a new thesis")
                return False
            else:
                return True

    def request_thesis(self , course, supervisor_id , theses):
        new_id = self.thesis_id_create (course.course_id, supervisor_id)
        continue_prog = self.is_new_thesis(new_id , theses)
        if continue_prog:
            new_thesis = Thesis(new_id , self.user_id , course.course_id , supervisor_id , course.year , course.semester)
            new_thesis.keywords = self.keyword_getter()
            new_thesis.request_date = date.today()
            new_thesis.major = self.major
            theses.append(new_thesis.to_dict())


    def view_status (self , theses):
        found = False
        for thesis in theses:
            if thesis["thesis_id"] == self.thesis_request and thesis["student_id"] == self.user_id:
                found = True
                self.print_basic_thesis_info (thesis)
                print ("_________________________________________________")
                print (f"Status : {thesis['status']}")
                if thesis["status"] == "rejected":
                    print ("Your request has been rejected. make a new request")
                if thesis["status"] == "approved" and thesis["defence_requested"] == False:
                    print("_________________________________________________")
                    print (f"You can request for defence in 3 month after {thesis['request_date']}")
                if thesis["status"] == "approved" and thesis["defence_requested"] == True and not thesis["defence_date"]:
                    print ("You should wait until the defence date is set.")
                if thesis["status"] == "approved" and thesis["defence_requested"] == True and thesis["defence_date"]:
                    print("Defence Information")
                    print("----------------------")
                    if not thesis["files"] :
                        print ("No file has been uploaded")
                    else:
                        print (f"File : {thesis['files']}")
                    print (f"Defence date : {thesis['defence_date']}")
                    print (f"Reviewers : {thesis['reviewers'][0]} , {thesis['reviewers'][1]}")
                    print ("Evaluation Information")
                    print("----------------------")
                    if not thesis["defence_result"]:
                        print (f"Evaluations : \n"
                               f"Supervisor grade : {thesis['evaluations']['supervisor']}\tInternal viewer : {thesis['evaluations']['internal_viewer']}\tExternal viewer : {thesis['evaluations']['external_viewer']}\n"
                               f"Final grade: {thesis['evaluations']['final_grade']}")
                        print (f"Defence result: {thesis['defence_result']}")

        if not found:
            print ("There is no thesis for you")


    @staticmethod
    def check_time (request_date):
        date_format = "%Y-%m-%d"
        try:
            input_date = datetime.strptime(request_date, date_format)
            three_months_later = input_date + timedelta(days=90)
            return datetime.now() >= three_months_later
        except ValueError:
            print("Invalid date format.")
            return False

    def defence_request (self , theses):
        found = False
        for thesis in theses:
            if thesis["student_id"] == self.user_id:
                found = True
                if thesis["status"] == "approved" and thesis["defence_requested"] == True:
                    print ("You have requested later. You should wait until the defence date is set.")
                elif not thesis["status"] == "approved":
                    print ("Your request has not been approved by supervisor")
                elif thesis["status"] == "approved" and thesis["defence_requested"] == False:
                    if not thesis["files"] and not thesis["keywords"]:
                        if not self.check_time(thesis["request_date"]):
                            print(f"You can request for defence in 3 month after {thesis['request_date']}")
                        else:
                            self.print_basic_thesis_info (thesis)
                            if yesno("Do you want to request for defence? "):
                                thesis["defence_requested"] = True
                                break

        if not found :
            print ("There is no thesis for you")

    def upload_doc (self , theses):
        found = False
        for thesis in theses:
            if thesis["student_id"] == self.user_id:
                found = True
                pdf_path = input ("Enter the path of the PDF file: ")
                first_image = input ("Enter the name of the first image: ")
                second_image = input ("Enter the name of the second image: ")
                pdf_des = "../files/PDfs"
                images_des = "../files/Images"
                pdf_name = f"{thesis['thesis_id']}_{os.path.basename(pdf_path)}"
                pdf_destination_path = os.path.join(pdf_des, pdf_name)
                first_image_name = f"{thesis['thesis_id']}_{os.path.basename(first_image)}"
                first_image_destination_path = os.path.join(images_des, first_image_name)
                second_image_name = f"{thesis['thesis_id']}_{os.path.basename(second_image)}"
                second_image_destination_path = os.path.join(images_des, second_image_name)

                try:
                    shutil.copy(pdf_path , pdf_destination_path)
                    shutil.copy(first_image , first_image_destination_path)
                    shutil.copy(second_image , second_image_destination_path)
                    thesis["files"]["pdf"] = pdf_destination_path
                    thesis["files"]["first_image"] = first_image_destination_path
                    thesis["files"]["second_image"] = second_image_destination_path
                    print ("files has been uploaded successfully")
                    print(f"New path is : {pdf_destination_path} and {first_image_destination_path} and {second_image_destination_path}")
                    return True
                except SameFileError as e:
                    print("Source and destination represents the same file.")
                    print(e)
                    return False
                except IsADirectoryError:
                    print ("Destination is a directory. write complete path.")
                    return False
                except FileNotFoundError as e:
                    print ("File not found.")
                    print(e)
                    return False
                except Exception as e:
                    print("Something went wrong.")
                    print(e)
                    return False

