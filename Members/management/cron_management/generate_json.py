from django.utils import timezone
from datetime import datetime, timedelta
from django.conf import settings
import os, json, random, string, pytz
import sys
import psycopg2
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

import django

sys.path.append("/app")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "modules.settings")
django.setup()

from django.utils import timezone
from datetime import datetime, timedelta
from django.conf import settings
import json, random, string, pytz


IST = pytz.timezone('Asia/Kolkata')

# =======================================> DATABASE CONFIGURATION
DB_NAME = "project_1"
DB_USER = "quantumd"
DB_PASSWORD = "admlqq"
# ==========================> LOCAL
# DB_HOST = "localhost"
# ==========================> LOCAL

# ==========================> DOCKER
DB_HOST = "modules_db"
# ==========================> DOCKER

conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST
)

cursor = conn.cursor()
# =======================================> DATABASE CONFIGURATION


cursor.execute("SELECT version();")
result_1 = cursor.fetchone()

if result_1:
    print("=====================")
    print("DATABASE CONFIGURED")
    print("=====================")
    
    def random_string(length=6):
        return ''.join(random.choices(string.ascii_lowercase, k=length))

    def my_scheduled_job():
        print("\n\n\nTRIGERERED")
        members_list = []
        
        get_name_department = "select id, name, department from members;"
        cursor.execute(get_name_department)
        result_2 = cursor.fetchall()

        start_1 = 0
        stop_1 = len(result_2)
        step_1 = 1

        for i in range(start_1, stop_1, step_1):
            employee_id     = result_2[i][0]
            name            = result_2[i][1]
            department      = result_2[i][2]

            # # ==========================================> DEBUGGER
            # print(f"EMPLOYEE ID   : {employee_id}")
            # print(f"NAME          : {name}")
            # print(f"DEPARTMENT    : {department}")
            # # ==========================================> DEBUGGER
            
            members_list.append({
                "id": result_2[i][0],
                "name": result_2[i][1],
                "department": result_2[i][2]
            })

        # # ==========================================> DEBUGGER
        # print(f"NAME        : {names}")
        # print(f"DEPARTMENT  : {departments}")
        # # ==========================================> DEBUGGER
        
        file_dir = os.path.join(settings.BASE_DIR, "static", "Json_data")
        os.makedirs(file_dir, exist_ok=True)
        file_path = os.path.join(file_dir, "data.json")

        if os.path.exists(file_path):
            with open(file_path, "r") as json_file:
                old_data = json.load(json_file)
        else:
            old_data = []

        if old_data:
            last_id = old_data[-1]["id"]
            last_datetime = datetime.fromisoformat(old_data[-1]["log_out"]).astimezone(IST)
        else:
            last_id = 0
            last_datetime = timezone.now().astimezone(IST).replace(hour=7, minute=0, second=0, microsecond=0)

        data = []
        total_records = 100

        for i in range(1, total_records + 1):
            # Generate IST timestamps properly
            login_time = (last_datetime + timedelta(minutes=random.randint(5, 30))).astimezone(IST)
            logout_time = (login_time + timedelta(hours=random.randint(8, 12))).astimezone(IST)

            member = random.choice(members_list)

            data.append({
                "id": last_id + i,
                "name": member["name"],
                "surname": random_string(7).capitalize(),
                "username": member["name"],
                "employee_id": member["id"],  # <-- THIS IS OK now, it matches real IDs
                "department": member["department"],
                "log_in": login_time.isoformat(),
                "log_out": logout_time.isoformat()
            })
            
            
            last_datetime = logout_time

        final_data = old_data + data
        with open(file_path, "w") as json_file:
            json.dump(final_data, json_file, indent=4)

        print(f"Appended {len(data)} new records. Total: {len(final_data)} — {datetime.now().astimezone(IST)}")

    # ==========================
    # Call function here
    # ==========================
    if __name__ == "__main__":
        my_scheduled_job()
else:
    print("=====================")
    print("SOMETHING WENT WRONG")
    print("=====================")
