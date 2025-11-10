from django.core.management.base import BaseCommand
from Members.models import Members
print("=== BULK INSERTION USING bulk_create() ===")

class Command(BaseCommand):
    help = "Insert values into the Members table"

    def handle(self, *args, **kwargs):
        confirm_1 = input("Confirm to start bulk insert? (yes/no): ").strip().lower()
        if confirm_1 != 'yes':
            print("Bulk Insert Cancelled by User!!!")
            return

        set_data = [
            Members(
                    name="Hari",
                    age=23,
                    department="BackEnd-Developer",
                    salary=24000,
                    email="hari@gmail.com",
                    company_id=4
                ),
                Members(
                    name="Swaraj",
                    age=25,
                    department="React Developer",
                    salary=24000,
                    email="swaraj@gmail.com",
                    company_id=2
                ),
                Members(
                    name="Rakshita",
                    age=22,
                    department="FrontEnd Developer",
                    salary=24000,
                    email="rakshita@gmail.com",
                    company_id=3
                ),
                Members(
                    name="Sathish",
                    age=26,
                    department="Perl Developer",
                    salary=21000,
                    email="sathish@gmail.com",
                    company_id=1
                )
        ]
        print("=== BULK INSERTION COMPLETE! ===")
        inserted=Members.objects.bulk_create(set_data)

        # =================================> CONDITIONAL LOGIC

        confirm_2 = input("Confirm to check inserted names an count? (yes/no): ").strip().lower()
        if confirm_2 != 'yes':
            print("Cancelled by user to check Inserted Details!!!")
            return

        count=0
        start=0
        stop=len(inserted)
        step=1
        for i in range(start, stop, step):
            print(f"Inserted : {inserted[i]}")
            count = count + 1
        print(f"TOTAL INSERTED {count}")
        # =================================> CONDITIONAL LOGIC

        del set_data, inserted, count, start, stop, step, confirm_1, confirm_2
