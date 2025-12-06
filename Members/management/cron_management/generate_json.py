from django.utils import timezone
from datetime import datetime, timedelta
from django.conf import settings
import os, json, random, string, pytz
import sys
sys.path.append("/home/hari/development_1/orm")

import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm.settings")
django.setup()

from django.utils import timezone
from datetime import datetime, timedelta
from django.conf import settings
import json, random, string, pytz


IST = pytz.timezone('Asia/Kolkata')

def random_string(length=6):
    return ''.join(random.choices(string.ascii_lowercase, k=length))

def my_scheduled_job():
    departments = ["HR", "Finance", "Engineering", "Marketing", "Sales", "Support"]
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

        data.append({
            "id": last_id + i,
            "name": random_string(5).capitalize(),
            "surname": random_string(7).capitalize(),
            "username": random_string(8),
            "employee_id": f"EMP{random.randint(1000, 9999)}",
            "department": random.choice(departments),
            "log_in": login_time.isoformat(),
            "log_out": logout_time.isoformat()
        })

        last_datetime = logout_time

    final_data = old_data + data
    with open(file_path, "w") as json_file:
        json.dump(final_data, json_file, indent=4)

    print(f"Appended {len(data)} new records. Total: {len(final_data)} — {datetime.now().astimezone(IST)}")




# ==========================
# 🔥 Call function here
# ==========================
if __name__ == "__main__":
    print("Running JSON generator cron...")
    my_scheduled_job()
    print("Completed!")