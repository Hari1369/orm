# import os
# import sys
# sys.path.append("/home/hari/development_1/orm")

# import django
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm.settings")
# django.setup()

# import json
# import requests
# from django.conf import settings

# JSON_PATH = os.path.join(settings.BASE_DIR, "static", "Json_data", "data.json")

# API_URL = "http://127.0.0.1:8000/department/test_1/"
# ACCESS_TOKEN =  "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzY1MDM2Mjk0LCJpYXQiOjE3NjUwMzU5OTQsImp0aSI6IjU3ODVkN2U5OWI4NzQ5NzQ5MTU0NzA1MmJkMWY0ZGZlIiwidXNlcl9pZCI6MX0.sd3YmuhenpUhYWPg2D10g8K4Tjvcn0iJfZ3VGVDgUck"  

# headers = {
#     "Authorization": f"Bearer {ACCESS_TOKEN}",
#     "Content-Type": "application/json"
# }

# def push_json_data():
#     if not os.path.exists(JSON_PATH):
#         print("JSON file not found!")
#         return

#     with open(JSON_PATH, "r") as file:
#         data = json.load(file)

#     success_count = 0
#     fail_count = 0

#     for record in data:
#         payload = {
#             "first_name": record["name"],
#             "last_name": record["surname"],
#             "username": record["username"],
#             "employee_id": int(record["employee_id"].replace("EMP", "")),
#             "department": record["department"],
#             "log_in": record["log_in"],
#             "log_out": record["log_out"]
#         }

#         response = requests.post(API_URL, headers=headers, json=payload)

#         if response.status_code in [200, 201]:
#             success_count += 1
#         else:
#             fail_count += 1
#             print(f"Error: {response.status_code} → {response.text}")

#     print(f"✔ Uploaded: {success_count} | Failed: {fail_count}")


# if __name__ == "__main__":
#     print("📌 API trigger started...")
#     push_json_data()
#     print("✅ API trigger completed!")

# ===============================================================================================================
# ===============================================================================================================
# ===============================================================================================================
# ===============================================================================================================
# ===============================================================================================================
# ===============================================================================================================


import os
import sys
sys.path.append("/home/hari/development_1/orm")

import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm.settings")
django.setup()
import time

import json
import requests
from django.conf import settings

JSON_PATH = os.path.join(settings.BASE_DIR, "static", "Json_data", "data.json")

API_URL = "http://127.0.0.1:8000/department/test_1/"

TOKEN_URL = "http://127.0.0.1:8000/api/token/"
REFRESH_URL = "http://127.0.0.1:8000/api/token/refresh/"

# Add your refresh token here
REFRESH_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc2NzYyODkxNSwiaWF0IjoxNzY1MDM2OTE1LCJqdGkiOiJlNjZmMDFjODIzNjg0MGZjODkyOGZhOGI2N2NiNzRmYyIsInVzZXJfaWQiOjF9.rwCsLF5BT54eFkwi18VzslWMUnit08jl3-0mrUDre94"
ACCESS_TOKEN = None



def get_access_token():
    """Generate new access token from refresh token"""
    global ACCESS_TOKEN

    response = requests.post(REFRESH_URL, data={"refresh": REFRESH_TOKEN})

    if response.status_code == 200:
        ACCESS_TOKEN = response.json()["access"]
        print("🔄 New Access Token Generated Automatically!")
    else:
        print("❌ Refresh Token Expired! Generate new one using /api/token/")
        exit()



def send_request(payload, retries=5, delay=5):
    global ACCESS_TOKEN
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}", "Content-Type": "application/json"}
    
    for attempt in range(retries):
        try:
            response = requests.post(API_URL, headers=headers, json=payload)
            if response.status_code == 401:
                get_access_token()
                headers["Authorization"] = f"Bearer {ACCESS_TOKEN}"
                response = requests.post(API_URL, headers=headers, json=payload)
            return response
        except requests.exceptions.ConnectionError:
            print(f"⚠️ Connection failed. Retry {attempt + 1}/{retries} in {delay}s...")
            time.sleep(delay)
    raise Exception("❌ Max retries exceeded. Could not connect to API.")



def save_json(updated_data):
    """🔥 Save updated JSON after removing processed record"""
    with open(JSON_PATH, "w") as f:
        json.dump(updated_data, f, indent=4)
    print("📝 JSON updated (record removed)")


def push_json_data():

    if not os.path.exists(JSON_PATH):
        print("❌ JSON file not found!")
        return

    # Load JSON
    with open(JSON_PATH, "r") as f:
        data = json.load(f)

    if not data:
        print("📂 JSON EMPTY — Nothing to send!")
        return

    get_access_token()   # get an access token

    success = fail = 0

    # 🔥 Process each record one by one
    index = 0
    while index < len(data):

        record = data[index]

        payload = {
            "first_name": record["name"],
            "last_name": record["surname"],
            "username": record["username"],
            "employee_id": int(record["employee_id"].replace("EMP", "")),
            "department": record["department"],
            "log_in": record["log_in"],
            "log_out": record["log_out"]
        }

        res = send_request(payload)

        if res.status_code in [200, 201]:
            success += 1
            print(f"✔ Sent record: {record['username']}")

            # 🔥 Remove the sent record
            data.pop(index)
            save_json(data)

        else:
            fail += 1
            print("❌ Failed:", res.status_code, res.text)
            index += 1  # move forward (do NOT remove)

    print(f"✔ Uploaded: {success} | ❌ Failed: {fail}")


if __name__ == "__main__":
    print("📌 API trigger started...")
    push_json_data()
    print("✅ API trigger completed!")





