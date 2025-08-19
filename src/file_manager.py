'''
This class can load / save data from files
'''

import json

class FileManager:
    def __init__(self):
        pass
    def load_file(self, file_path):
        try:
            json_data = json.load(open(file_path, 'r' , encoding='utf-8'))
            return json_data
        except FileNotFoundError as e:
            print(e)
            return None
        except Exception as e:
            print(e)
            return None
    def save_file(self, file_path , json_data):
        try:
            open(file_path, 'w').write(json.dumps(json_data))
        except FileNotFoundError as e:
            print(e)
        except:
            print("Error saving data")
            return None
