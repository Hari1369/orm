from django.core.management.base import BaseCommand
from django.db.models import Avg, Sum, Min, Max, Count, F, Value, Count
from django.db.models.functions import Concat
from job.models import Jobs, Company

# ------------------------------------------------------------------------------
# |Sr No | Method                 | Description                           |
# |------| ---------------------- | ------------------------------------- |
# | 1)   | `.all()`               | All rows                              |
# | 2)   | `.filter()`            | Filtered rows                         |
# | 3)   | `.get()`               | Single row (raises error on multiple) |
# | 4)   | `.values()`            | List of dicts                         |
# | 5)   | `.values_list()`       | List of tuples                        |
# | 6)   | `.exclude()`           | Exclude rows                          |
# | 7)   | `.order_by()`          | Sort results                          |
# | 8)   | `.distinct()`          | Unique results                        |
# | 9)   | `.first()` / `.last()` | Get one record                        |
# | 10)  | `.count()`             | Count of rows                         |
# | 11)  | `.aggregate()`         | Min, Max, Avg, Sum                    |
# | 12)  | `.annotate()`          | Grouped values                        |
# | 13)  | `.exists()`            | Boolean check                         |
# | 14)  | `.select_related()`    | JOIN for FK                           |
# | 15)  | `.prefetch_related()`  | JOIN for M2M or reverse FK            |
# | 16)  | `.raw()`               | Custom SQL                            |
# ------------------------------------------------------------------------------

class Command(BaseCommand):
    help = "Insert values into the Jobs table"

    def handle(self, *args, **kwargs):

        print("========== ORM QUERY MENU ==========")
        print("| 1. all()              |")
        print("| 2. values()           |")
        print("| 3. get()              |")
        print("| 4. values_list()      |")
        print("| 5. exclude()          |")
        print("| 6. order_by()         |")
        print("| 7. distinct()         |")
        print("| 8. first() / last()   |")
        print("| 9. count()            |")
        print("| 10. aggregate()       |")
        print("| 11. annotate()        |")
        print("| 12. exists()          |")
        print("| 13. select_related()  |")
        print("| 14. prefetch_related()|")
        print("| 15. raw()             |")
        print("=====================================")


        choices_1 = input("Choose a method number to run : ").strip()
        print("-----" * 4)
        if choices_1 == '1':
            obj1 = Jobs.objects.all()
            start=0
            stop=len(obj1)
            step=1
            for i in range(start, stop, step):
                print(f" NAME : {obj1[i].name}")
                print(f" AGE : {obj1[i].age}")
                print(f" DEPARTMENT : {obj1[i].department}")
                print(f" SALARY : {obj1[i].salary}")
                print(f" EMAIL : {obj1[i].email}")
                print(f" COMPANY NAME : {obj1[i].company.name}")
            print("-----" * 4)
            # ====================> OPTIONAL|||
            del start, stop, step, obj1     
            # ====================> OPTIONAL|||

        elif choices_1 == '2':
            obj2 = Jobs.objects.values('name')
            start=0
            stop=len(obj2)
            step=1
            for i in range(start, stop, step):
                print(f"NAMES : {obj2[i]['name']}")
            print("-----" * 4)
            # ====================> OPTIONAL|||
            del start, stop, step, obj2     
            # ====================> OPTIONAL|||

        elif choices_1 == '3':
            obj3 = Jobs.objects.get(name='Hari')
            print(f"NAME : {obj3.name}")
            print(f"SALARY : {obj3.salary}")
            print(f"AGE : {obj3.age}")
            print(f"DEPARTMENT : {obj3.department}")
            print(f"COMPANY NAME : {obj3.company.name}")
            print("-----" * 4)
            # ====================> OPTIONAL|||
            del obj3     
            # ====================> OPTIONAL|||

        elif choices_1 == '4':
            obj4 = Jobs.objects.values_list('name', 'salary')
            start = 0
            stop = len(obj4)
            step = 1
            for i in range(start, stop, step):
                print(f"NAME   : {obj4[i][0]}")
                print(f"SALARY : {obj4[i][1]}")
            print("-----" * 4)
            # ====================> OPTIONAL|||
            del start, stop, step, obj4
            # ====================> OPTIONAL|||

        elif choices_1 == '5':
            obj5 = Jobs.objects.exclude(department='BackEnd-Developer')
            start=0
            stop=len(obj5)
            step=1
            for i in range(start, stop, step):
                print(f"NAME : {obj5[i].name}")
                print(f"DEPARTMENT : {obj5[i].department}")                
            print("-----" * 4)
            # ====================> OPTIONAL|||
            del start,stop, step, obj5     
            # ====================> OPTIONAL|||

        elif choices_1 == '6':
            obj6 = Jobs.objects.order_by('salary')
            start=0
            stop=len(obj6)
            step=1
            for i in range(start, stop, step):
                print(f"NAME : {obj6[i].name} --> ₹{obj6[i].salary}")
            print("-----" * 4)
            # ====================> OPTIONAL|||
            del start, stop, step, obj6
            # ====================> OPTIONAL|||
            

        elif choices_1 == '7':
            obj7 = Jobs.objects.values('department').distinct()
            start=0
            stop=len(obj7)
            step=1
            for i in range(start, stop, step):
                print(f"DISTINCT DATA : {obj7[i]['department']}")
            print("-----" * 4)
            # ====================> OPTIONAL|||
            del start, stop, step, obj7
            # ====================> OPTIONAL|||

        elif choices_1 == '8':
            first_1 = Jobs.objects.first()
            last_1 = Jobs.objects.last()
            print(f"FIRST NAME  : {first_1.name}")
            print(f"LAST NAME   : {last_1.name}")
            print("-----" * 4)
            # ====================> OPTIONAL|||
            del first_1, last_1
            # ====================> OPTIONAL|||

        elif choices_1 == '9':
            obj8 = Jobs.objects.count()
            print(f"TOTAL COUNT : {obj8}")
            print("-----" * 4)
            # ====================> OPTIONAL|||
            del obj8
            # ====================> OPTIONAL|||

        elif choices_1 == '10':
            obj9 = Jobs.objects.values('department').annotate(count=Count('id'))
            start=0
            stop=len(obj9)
            step=1
            for i in range(start, stop, step):
                department = obj9[i]['department']
                count = obj9[i]['count']
                print(f"DEPARTMENT : {department}")
                print(f"COUNT : {count}")
            print("-----" * 4)
            # ====================> OPTIONAL|||
            del obj9, start, stop, step, department, count
            # ====================> OPTIONAL|||

        elif choices_1 == '11':
            obj10 = Jobs.objects.aggregate(MinSalary=Min('salary'), MaxSalary=Max('salary'), AvgSalary=Avg('salary'), TotalSalary=Sum('salary'))
            print(f"MAX SALARY : {obj10['MinSalary']}")
            print(f"MIN SALARY : {obj10['MaxSalary']}")
            print(f"AVG SALARY : {obj10['AvgSalary']}")
            print(f"TOTAL SALARY : {obj10['TotalSalary']}")
            print("-----" * 4)
            # ====================> OPTIONAL|||
            del obj10
            # ====================> OPTIONAL|||

        elif choices_1 == '12':
            obj11 = Jobs.objects.filter(department='Perl Developer').exists()
            if obj11:
                print("IT EXIST!")
            else:
                print("NOT EXIST!")
            print("-----" * 4)
            # ====================> OPTIONAL|||
            del obj11
            # ====================> OPTIONAL|||
        
        elif choices_1 == '13':
            obj12 = Jobs.objects.select_related('company')
            start=0
            stop=len(obj12)
            step=1
            for i in range(start, stop, step):
                company_name = obj12[i].company.name
                print("COMPANY NAMES : ",company_name)
            print("-----" * 4)
            # ====================> OPTIONAL|||
            del obj12, start, stop, step
            # ====================> OPTIONAL|||

        elif choices_1 == '14':
            obj13 = Jobs.objects.prefetch_related('company')
            start=0
            stop=len(obj13)
            step=1
            for i in range(start, stop, step):
                name = obj13[i].name
                company_works = obj13[i].company.name
                location = obj13[i].company.location

                print(f"NAME : {name}")
                print(f"COMPANY NAME : {company_works}")
                print(f"LOCATION : {location}")
            print("-----" * 4)
            
        elif choices_1 == '15':
                obj14 = Company.objects.raw('SELECT id, name FROM company')
                for row in obj14:
                    print(f"COMPANY NAME : {row.name}")