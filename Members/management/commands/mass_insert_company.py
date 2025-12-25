from django.core.management.base import BaseCommand
from Members.models import Members, Company
print("=== BULK INSERTION USING bulk_create() ===")

class Command(BaseCommand):
    help = "Insert values into the Companies table"
    def handle(self, *args, **kwargs):
        confirm_1 = input("Confirm to start bulk insert? (yes/no): ").strip().lower()
        if confirm_1 != 'yes':
            print("Bulk Insert Cancelled by User!!!")
            return
        
        set_data = [
            Company(
                name="Tata Consultancy Service",
                location="Navi Mumbai"
            ),
            Company(
                name="Infosys",
                location="Pune"
            ),
            Company(
                name="Capegimini",
                location="Aeroli"
            ),
            Company(
                name="Blinkit",
                location="Bandra"
            ),
            Company(
                name="Mobitrial",
                location="Andheri"
            ),
            Company(
                name="HCL Technologies",
                location="Goregoan"
            ),
            Company(
                name="Wipro Limited",
                location="Lower Parel"
            ),
            Company(
                name="LTIMindtree Ltd",
                location="Thane"
            ),
            Company(
                name="Tech Mahindra",
                location="Navi Mumbai"
            )
        ]
        print("=== BULK INSERTION COMPLETE! ===")
        inserted=Company.objects.bulk_create(set_data)
        
        confirm = input("Confirm to check inserted names an count? (yes/no): ").strip().lower()
        if confirm != 'yes':
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

        del set_data, inserted, count, start, stop, step, confirm
