import requests

class LLM_Integration:
    def __init__(self):
        ROOT_URL = 'http://localhost:5002'
        self.puzzle_url = f"{ROOT_URL}/getpuzzle"

    def getpuzzle(self):
        response = requests.get(self.puzzle_url)
        if response.status_code == 200:
            return response.json()
        else:
            return response