import requests
import os
from pathlib import Path

class HangmanDB_Integration:
    def __init__(self):
        self.load_env()
        ROOT_URL = os.getenv("API_URL")
        self.random_url = f"{ROOT_URL}/random"
        self.add_url = f"{ROOT_URL}/add"

    def random(self):
        return requests.get(self.random_url)
    
    def load_env(self):
        env_path = Path('..') / '.env'

        # Open and read the .env file
        if env_path.exists():
            with open(env_path) as f:
                for line in f:
                    # Strip any surrounding whitespace and ignore empty lines or comments
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue

                    # Split the line into key and value
                    key, value = line.split('=', 1)
                    # Set the environment variable
                    os.environ[key] = value