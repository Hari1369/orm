from django.core.management.base import BaseCommand
from django.db.models import F, Q
from Members.models import Jobs, Company

# | Lookup        | Meaning                    |
# | ------------- | -------------------------- |
# | `__lt`        | Less than `<`              |
# | `__lte`       | Less than or equal `<=`    |
# | `__gt`        | Greater than `>`           |
# | `__gte`       | Greater or equal `>=`      |
# | `__exact`     | Equal `=`                  |
# | `__icontains` | Case-insensitive substring |



class Command(BaseCommand):
    help = "Demonstrate various types of UPDATE operations using Django ORM"

    def handle(self, *args, **kwargs):

        print("========== ORM UPDATE MENU ==========")
        print("| 1. Update single record using save()       |")
        print("| 2. Update multiple records using update()  |")
        print("| 3. Update with F expression                |")
        print("| 4. Update with Q condition                 |")
        print("| 5. Bulk update using bulk_update()         |")
        print("| 6. Update or create                        |")
        print("| 7. Get or create (upsert)                  |")
        print("============================================")

        choice_2 = input("Choose a method number to run : ").strip()
        print("-----" * 5)

        if choice_2 == "1":
            confirmation_2 = input("Salary Increase (yes/no) : ").strip()
            if confirmation_2 != "yes":
                print("ABORT!!!")
                return
            else:
                obj1 = Jobs.objects.first()
                if obj1:
                    obj1.salary = obj1.salary + 1000
                    obj1.save()
                    print(f"Updated {obj1.name} Salary : {obj1.salary}")
                else:
                    print("No records found.")
                # ====================> OPTIONAL|||
                del obj1
                # ====================> OPTIONAL|||


        elif choice_2 == '2':
            confirmation_2 = input("Salary Increase (yes/no) : ").strip()

            if confirmation_2 != "yes":
                print("ABORT!!!")
                return
            else:
                obj2 = Jobs.objects.filter(department='Finance')
                start=0
                stop=len(obj2)
                step=1
                if obj2.exists():
                    count = obj2.update(salary=25000)
                    for i in range(start, stop, step):
                        print(f"Name : {obj2[i].name} SALARY {obj2[i].salary}")
                    if count > 0:
                        print(f"UPDATED COUNT {count}!")
                    else:
                        print(f"NO RECORDS FOUND!")
            # ====================> OPTIONAL|||
            del obj2, count, start, stop, step, confirmation_2
            # ====================> OPTIONAL|||


        elif choice_2 == '3':
            confirmation_3 = input("Increase Salary by 2000 for All Employees (yes/no) : ").strip()
            if confirmation_3 != "yes":
                print("ABORTED!!!")
                return
            else:
                obj3 = Jobs.objects.update(salary=F('salary') + 2000)
                count = obj3
                if obj3 > 0:
                    print(f"TOTAL COUNT : {count}")
                else:
                    print(f"NOTHING UPDATE!")
            # ====================> OPTIONAL|||
            del confirmation_3, obj3
            # ====================> OPTIONAL|||

        elif choice_2 == "4":
            confirmation_4 = input("Updated salaries where condition matched (yes/no) : ").strip()
            if confirmation_4 != "yes":
                print("ABORT!!!")
                return
            else:
                obj4 = Jobs.objects.filter(Q(salary__lt=23000) | Q(department='Perl Developer')).update(salary=23000)
                count = obj4
                if count > 0:
                    print(f"Updated salaries where condition matched {count}")
                else:
                    print("NOTHING FOUND!!!")

        elif choice_2 == "5":
            confirmation_4 = input("Bulk update using bulk_update() (yes/no) : ").strip()
            if confirmation_4 != "yes":
                print("ABORT!!!")
                return
            else:
                objs = list(Jobs.objects.all())
                for obj in objs:
                    obj.salary = obj.salary + 500
                Jobs.objects.bulk_update(objs, ['salary'])
                print("Bulk updated all salaries by +500")
        
        elif choice_2 == "6":
            data = [
                {
                    'name': "Hari",
                    'defaults': {
                        'age': 23,
                        'department': "BackEnd-Developer",
                        'salary': 24000,
                        'email': "hari@gmail.com",
                        'company_id': 4
                    }
                },
                {
                    'name': "Swaraj",
                    'defaults': {
                        'age': 25,
                        'department': "React Developer",
                        'salary': 24000,
                        'email': "swaraj@gmail.com",
                        'company_id': 2
                    }
                },
                {
                    'name': "Rakshita",
                    'defaults': {
                        'age': 22,
                        'department': "FrontEnd Developer",
                        'salary': 24000,
                        'email': "rakshita@gmail.com",
                        'company_id': 3
                    }
                },
                {
                    'name': "Sathish",
                    'defaults': {
                        'age': 26,
                        'department': "Perl Developer",
                        'salary': 21000,
                        'email': "sathish@gmail.com",
                        'company_id': 1
                    }
                }
            ]

            updated = 0
            created = 0

            for item in data:
                obj, created_flag = Jobs.objects.update_or_create(name=item['name'], defaults=item['defaults'])
                if created_flag:
                    print(f"Created: {obj.name}")
                    created += 1
                else:
                    print(f"Updated: {obj.name}")
                    updated += 1

            print(f"\nSummary:")
            print(f"✅ Created: {created}")
            print(f"✅ Updated: {updated}")
