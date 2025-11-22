import os
import sys
sys.path.append("/home/hari/development_1/orm")

import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm.settings")
django.setup()

import json
import requests
from django.conf import settings

JSON_PATH = os.path.join(settings.BASE_DIR, "static", "Json_data", "data.json")

API_URL = "http://127.0.0.1:8000/api_data/"
ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzYzODQ2OTQ3LCJpYXQiOjE3NjM4NDY2NDcsImp0aSI6IjU1OTE5NGY1Yjk1ZDQ3ODNiYWE1ODZiY2E5YTFkYzYyIiwidXNlcl9pZCI6MX0.DCD3MwMrWLK4fKlBNbGgnQlh0cTbtS0BRqlrs4QnN_c"

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

def push_json_data():
    if not os.path.exists(JSON_PATH):
        print("JSON file not found!")
        return

    with open(JSON_PATH, "r") as file:
        data = json.load(file)

    success_count = 0
    fail_count = 0

    for record in data:
        payload = {
            "first_name": record["name"],
            "last_name": record["surname"],
            "username": record["username"],
            "employee_id": int(record["employee_id"].replace("EMP", "")),
            "department": record["department"],
            "log_in": record["log_in"],
            "log_out": record["log_out"]
        }

        response = requests.post(API_URL, headers=headers, json=payload)

        if response.status_code in [200, 201]:
            success_count += 1
        else:
            fail_count += 1
            print(f"Error: {response.status_code} → {response.text}")

    print(f"✔ Uploaded: {success_count} | Failed: {fail_count}")


if __name__ == "__main__":
    print("📌 API trigger started...")
    push_json_data()
    print("✅ API trigger completed!")
