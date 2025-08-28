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

    def save_file(self, file_path, data, key=None):
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                if key:
                    json.dump({key: data}, f, indent=4, ensure_ascii=False)
                else:
                    json.dump(data, f, indent=4, ensure_ascii=False)
        except FileNotFoundError as e:
            print(f"❌ File not found: {e}")
        except Exception as e:
            print(f"❌ Error saving data: {e}")