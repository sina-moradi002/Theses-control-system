class Thesis:
    def __init__(self, thesis_id , student_id , course_id , supervisor_id, topic , title , major , year , semester ):
        self.thesis_id = thesis_id
        self.student_id = student_id
        self.course_id = course_id
        self.supervisor_id = supervisor_id
        self.topic = topic
        self.title = title
        self.major = major
        self.year = year
        self.semester = semester
        self.status = "pending"
        self.keywords = []
        self.defence_requested = False
        self.request_date = None
        self.files = {}
        self.reviewers = []
        self.defence_date = None
        self.evaluation = {
            "supervisor" : None ,
            "internal_viewer": None ,
            "external_viewer": None ,
            "final_grade": None
        }
        self.defence_result = None

    def update_status (self, new_status):
        pass
    def caculate_final_grade(self):
        pass
    def session_file_creat (self):
        pass

    def to_dict(self):
        return {
            "thesis_id" : self.thesis_id,
            "student_id" : self.student_id,
            "course_id" : self.course_id,
            "supervisor_id" : self.supervisor_id,
            "topic" : self.topic,
            "title" : self.title,
            "major" : self.major,
            "year" : self.year,
            "semester" : self.semester,
            "status" : self.status,
            "keywords" : self.keywords,
            "defence_requested" : self.defence_requested,
            "request_date" : self.request_date,
            "files" : self.files,
            "reviewers" : self.reviewers,
            "defence_date" : self.defence_date,
            "evaluation" : self.evaluation,
            "defence_result" : self.defence_result
        }
