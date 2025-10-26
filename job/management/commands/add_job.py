from django.core.management.base import BaseCommand
from job.models import Jobs
print("=== SINGLE INSERTION USING save() ===")

class Command(BaseCommand):
    help = "Insert values into the Jobs table"

    def handle(self, *args, **kwargs):
        confirm_1 = input("Confirm to start single insert? (yes/no): ").strip().lower()
        if confirm_1 != 'yes':
            print("Single Insert Cancelled by User!!!")
            return

        print("=== SINGLE INSERTION COMPLETE! ===")
        obj_1 = Jobs(name="Ashish",age=23, department="Finance", salary=18000, email="ashish@gmail.com", company_id=1)
        obj_1.save()


        confirm_2 = input("Confirm to check inserted names an count? (yes/no): ").strip().lower()
        if confirm_2 != 'yes':
            print("Cancelled by User!!!")
            return
        
        # =================================> CONDITIONAL LOGIC
        count = 1
        if obj_1:
            count = 1
        else:
            count = 0
        print(f"COUNT {count}")
        # =================================> CONDITIONAL LOGIC

        del count, obj_1, confirm_1, confirm_2

