from thefuzz import fuzz

def search(theses):
    print ("Search Panel")
    action = input("1 = Search based on users\n2 = Search based on name\nChoose an action: ")
    if action == "1":
        user_based_search(theses)
    elif action == "2":
        name_based_search(theses)
    else:
        print("Invalid input")

def user_based_search(theses):
    ID_search = input("Enter ID: ")
    result = []
    for thesis in theses:
        if (thesis.get("student_id" , "") == ID_search or thesis.get("supervisor_id" , "") == ID_search) and thesis.get('defence_result'):
            result.append(thesis)


    print(f"{len(result)} matches found")

    printer(result)

def name_based_search(theses):
    name_search = input("Enter title , topic or major: ")
    result = []

    def keyword_similarity(name, keys):
        for key in keys:
            similarity = fuzz.ratio(name, key)
            if similarity > 90:
                return True
        return False
    for thesis in theses:
        if thesis.get('defence_result'):


            title_similarity = fuzz.token_sort_ratio(name_search, thesis['title'])
            topic_similarity = fuzz.token_sort_ratio(name_search, thesis['topic'])
            major_similarity = fuzz.token_sort_ratio(name_search, thesis['major'])

            if title_similarity > 70 or topic_similarity > 70 or major_similarity > 70:
                result.append(thesis)

            elif keyword_similarity(name_search, thesis['keywords']):
                result.append(thesis)


    print(f"{len(result)} matches found")

    printer(result)


def printer(result):
    for thesis in result:
        print("\n----------------------")
        print(thesis['title'])
        print(f"Topic: {thesis['topic']}")
        print(f"Thesis course ID : {thesis['course_id']}")
        print(f"Thesis supervisor ID : {thesis['supervisor_id']}")
        print(f"Thesis major : {thesis['major']}")
        print(f"Thesis year : {thesis['year']}", end='\t')
        print(f"Thesis semester : {thesis['semester']}")
        print(f"Thesis request date : {thesis['request_date']}")
        print (f"Keywords: {thesis['keywords']}")
        print(f"Defence date : {thesis['defence_date']}")
        print(f"Reviewers : {thesis['reviewers'][0]} , {thesis['reviewers'][1]}")
        print(f"Files : \n\t {thesis['files']['pdf']} \n\t {thesis['files']['first_image']}\n\t {thesis['files']['second_image']}")

