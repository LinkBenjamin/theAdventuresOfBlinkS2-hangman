import requests

class HangmanDB_Integration:
    def __init__(self):
        ROOT_URL = 'http://localhost:5001'
        self.random_url = f"{ROOT_URL}/random"
        self.add_url = f"{ROOT_URL}/add"

    def random(self):
        return requests.get(self.random_url)

    def add(self):
        pass