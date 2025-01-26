import requests
from dotenv import load_dotenv
import os

load_dotenv()

class QuickTimeClient:
    def __init__(self):
        self.bearerToken = self.__authenticate()

    def __authenticate(self):
        body = {
            "cpf": os.getenv("BACKEND_USER_CPF"),
            "password": os.getenv("BACKEND_USER_PASSWORD")
        }
        res = requests.post(f'{os.getenv("QUICK_TIME_BACKEND_URL")}/login', json=body)

        if res.status_code == 200:
            data = res.json()["data"]
            return data["accessToken"]
        else:
            print("Error in authenticate")

    def saveSchedule(self, bestSolution, conflicts):
        body = {
            "bestSolution": bestSolution,
            "conflicts": conflicts
        }

        headers = {
            "Authorization": f"Bearer {self.bearerToken}"
        }
        res = requests.post(f'{os.getenv("QUICK_TIME_BACKEND_URL")}/schedules/internal', json=body, headers=headers)

        if res.status_code == 200:
            return
        else:
            print("Error saving schedule")
