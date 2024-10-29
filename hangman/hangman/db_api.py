import requests

class HangmanDB_Integration:
    def __init__(self):
        ROOT_URL = 'http://localhost:5001'
        self.random_url = f"{ROOT_URL}/random"
        self.add_url = f"{ROOT_URL}/add"
        self.getall_url = f"{ROOT_URL}/getall"
        self.edit_url = f"{ROOT_URL}/edit"
        self.delete_url = f"{ROOT_URL}/delete"

    def random(self):
        return requests.get(self.random_url)
        
    def getall(self):
        try:
            response = requests.get(self.getall_url)
            if response.status_code == 200:
                return response.json()
            else:
                return {
                    "status_code":response.status_code,
                    "message": "Failed to fetch phrases from database."
                }
        except Exception as e:
            return {
                "Error": e
            }

    def add(self, phrase, hint):
        return requests.post(self.add_url, json={"phrase":phrase, "hint":hint})

    def edit(self, original_phrase, new_phrase, hint):
        return requests.put(self.edit_url, json={"original_phrase":original_phrase, "phrase": new_phrase, "hint": hint})
    
    def delete(self, phrase):
        data = {
            "phrase": phrase
        }
        return requests.delete(self.delete_url, json=data)