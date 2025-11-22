from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, HttpResponse
from rest_framework import viewsets
from django.http import JsonResponse
from .models import Members, Company, api_data
from .serializers import api_serializers
from django.db import connection
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
import json
from .forms import LoginForm
from django.utils import timezone
from django.views.decorators.cache import never_cache
from .models import UserSession
import pprint

def log_in_page(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # # =========================================> DEBUGGER
            # print ("USERNAME : ", username)
            # print ("PASSWORD : ", password)
            # # =========================================> DEBUGGER
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                request.session['login_time'] = str(timezone.now())
                return redirect('dashboard')
            else:
                return render(request, "Log_In/log_in.html", {
                    'form': form,
                    'error': 'Invalid username or password'
                })
        else:
            return HttpResponse(f"Something Went Wrong") 
    else:
        form = LoginForm()
    return render(request, "Log_In/log_in.html", {"form": form})


def logout_view(request):
    logout_time = timezone.now()
    logout(request)
    return redirect('log_in')


@never_cache
@login_required(login_url='log_in')
def show_dashboard(request):
    user = request.user
    # ====================================================================================> CHANGED
    # get_session_details = UserSession.objects.filter(user=user).order_by('-created_at')
    # ====================================================================================> CHANGED
    get_session_details = UserSession.objects.all().order_by('-created_at')
    session_list = list(get_session_details)
    length_1 = len(session_list)
    start_1 = 0
    stop_1 = length_1
    step_1 = 1

    session_data_list = []

    for i in range(start_1, stop_1, step_1):
        s = session_list[i]
        username = s.user.username
        if s.login_time:
            login_time = s.login_time.strftime("%d:%m:%Y %I:%M:%S %p")
        else:
            login_time = ""
        if s.logout_time:
            logout_time = s.logout_time.strftime("%d:%m:%Y %I:%M:%S %p")
        else:
            logout_time = ""
            
        if s.duration:
            total_seconds = int(s.duration.total_seconds())
            hours = total_seconds // 3600
            remainder = total_seconds - (hours * 3600)
            minutes = remainder // 60
            seconds = remainder - (minutes * 60)
            if hours > 0:
                duration = str(hours) + "h " + str(minutes) + "m " + str(seconds) + "s"
            elif minutes > 0:
                duration = str(minutes) + "m " + str(seconds) + "s"
            else:
                duration = str(seconds) + "s"
        else:
            duration = ""
        # # =====================================> DEBUGGER
        # print("LOGIN TIME :", login_time)
        # print("LOGOUT TIME :", logout_time)
        # print("-"*40)
        # # =====================================> DEBUGGER

        session_data = {
            "username": username,
            "login_time": login_time,
            "logout_time": logout_time,
            "duration": duration
        }

        session_data_list.append(session_data)

    return render(request, "Dashboard/dashboard.html", {
        "session_data": session_data_list
    })

@never_cache
@login_required(login_url='log_in')
def show_member(request):
    members = Members.objects.all()
    member_data = []
    start = 0
    stop = len(members)
    step = 1
    for i in range(start, stop, step):
        obj = members[i]
        name = obj.name
        department = obj.department
        salary = obj.salary
        company_name = obj.company.name
        
        member_data.append({
            'name' : name,
            'department' : department,
            'salary' : salary,
            'company_name' : company_name,
        })
        
    return render(request, "Member/member.html", {
        'member_data' : member_data
    })

@never_cache
@login_required(login_url='log_in')
def show_company(request):
    company = Company.objects.all()
    company_data = []
    start = 0
    stop = len(company)
    step = 1
    for i in range(start, stop, step):
        obj = company[i]
        name = obj.name
        location = obj.location

        company_data.append({
            'name' : name,
            'location' : location
        })
        
    return render(request, "Company/company.html", {
        'company_data' : company_data
    })
        
    
# ===================================================> API 
class api_getdata(viewsets.ModelViewSet):
    queryset = api_data.objects.all()
    serializer_class = api_serializers
# ===================================================> API 

        
# def show_basic_retrieval(request):
#     # =============================== Basic Retrival Queries ==============================
#     # =====================================================================================
#     # | Method                 | Description                                              |
#     # | ---------------------- | -------------------------------------------------------- |
#     # | `.all()`               | Fetch all records                                        |
#     # | `.get()`               | Fetch a single record (raises error if multiple or none) |
#     # | `.filter()`            | Fetch multiple records with conditions                   |
#     # | `.exclude()`           | Exclude certain records from result                      |
#     # | `.first()` / `.last()` | Get first/last record                                    |
#     # | `.exists()`            | Returns `True` if records exist                          |
#     # | `.count()`             | Count number of records                                  |
#     # =====================================================================================
#     return render(request, "Basic_Retrieval/basic_retrieval.html")

# def api_retrieval(request):
#     jobs = Jobs.objects.all().values()
#     return JsonResponse(list(jobs), safe=False)

# def raw_sql_query(request):
#     raw_queryset = Jobs.objects.raw("SELECT * FROM jobs")
#     raw_list = list(raw_queryset)
#     data = []
#     start = 0
#     stop = len(raw_queryset)
#     step = 1
#     for i in range(start, stop, step):
#         print(f"ID : {raw_list[i].id}")
#         print(f"NAME : {raw_list[i].name}")
#         print(f"AGE : {raw_list[i].age}")
#         print(f"DEPARTMENT : {raw_list[i].department}")
#         print(f"CREATED AT: {raw_list[i].created_at.isoformat()}")
#         print(f"UPDATED AT: {raw_list[i].updated_at.isoformat()}")

#         data.append({
#             'id':raw_list[i].id,
#             'name':raw_list[i].name,
#             'age':raw_list[i].age,
#             'department':raw_list[i].department,
#             'salary': str(raw_list[i].salary),
#         })
#     return JsonResponse({'data': data})

# @csrf_exempt
# def api_get(request):
#     if request.method == "POST":
#         try:
#             body = json.loads(request.body)
#             key = body.get("key","id").strip()
#             value = body.get("value", "3").strip()
#             filters = {key: value}
#             if key in ['id', 'age', 'salary']:
#                 try:
#                     filters[key] = int(value)
#                 except ValueError:
#                     return JsonResponse({'error': f'Invalid numeric value for {key}'}, status=400)

#             obj = Jobs.objects.get(**filters)

#             data = {
#                 "id": obj.id,
#                 "name": obj.name,
#                 "age": obj.age,
#                 "department": obj.department,
#                 "salary": str(obj.salary),
#                 "email": obj.email,
#                 "created_at": obj.created_at.isoformat(),
#                 "updated_at": obj.updated_at.isoformat()
#             }

#             return JsonResponse(data)
        
#         except Jobs.DoesNotExist:
#             return JsonResponse({"error": "No matching record found."}, status=404)
#         except Jobs.MultipleObjectsReturned:
#             return JsonResponse({"error": "Multiple records found. 'get()' needs only one."}, status=400)
#         except Exception as e:
#             return JsonResponse({"error": str(e)}, status=500)


# @csrf_exempt
# def all_sql(request):
#     if request.method == "POST":
#         try:
#             body = json.loads(request.body)
#             key = body.get("key", "id").strip()
#             value = body.get("value", "3").strip()

#             valid_keys = ['id', 'name', 'age', 'department', 'salary', 'email']
#             if key not in valid_keys:
#                 return JsonResponse({"error": "Invalid column name"}, status=400)

#             if key in ['id', 'age', 'salary']:
#                 try:
#                     value = int(value)
#                 except ValueError:
#                     return JsonResponse({"error": f"Invalid numeric value for {key}"}, status=400)

#             query = f"SELECT * FROM jobs WHERE {key} = %s"
#             with connection.cursor() as cursor:
#                 cursor.execute(query, [value])
#                 columns = [col[0] for col in cursor.description]
#                 rows = cursor.fetchall()
#                 data = [dict(zip(columns, row)) for row in rows]

#             if not data:
#                 return JsonResponse({"message": "No matching records found."}, status=404)

#             return JsonResponse(data, safe=False)

#         except Exception as e:
#             return JsonResponse({"error": str(e)}, status=500)



# @csrf_exempt
# def fetch_query(request):
#     if request.method == "POST":
#         try:
#             data = json.loads(request.body)
#             key = data.get('key')
#             value = data.get('value')

#             print("Key:", key)
#             print("Value:", value)

#             filters = {key: value}
#             result = Jobs.objects.filter(**filters)

#             if result.exists():
#                 response_data = list(result.values())
#                 return JsonResponse({"message": "Found", "data": response_data}, status=200)
#             else:
#                 return JsonResponse({"message": "No matching records found."}, status=404)

#         except json.JSONDecodeError:
#             return JsonResponse({"error": "Invalid JSON"}, status=400)
#     else:
#         return JsonResponse({"message": "API is working!"}, status=200)


# @csrf_exempt
# def fetch_sql_query(request):
#         if request.method == "POST":
#             try:
#                 data = json.loads(request.body)
#                 key = data.get('key')
#                 value = data.get('value')

#                 response_data = {
#                     key : key,
#                     value : value
#                 }
#                 valid_keys = ['id', 'name', 'age', 'department', 'salary', 'email']
#                 if key not in valid_keys:
#                     return JsonResponse({"error": "Invalid column name"}, status=400)
#                 if key in ['id', 'age', 'salary']:
#                     try:
#                         value = int(value)
#                     except ValueError:
#                         return JsonResponse({"error": f"Invalid numeric value for {key}"}, status=400)

#                 query = f"SELECT * FROM jobs WHERE {key} = %s"
#                 with connection.cursor() as cursor:
#                     cursor.execute(query, [value])
#                     columns = [col[0] for col in cursor.description]
#                     rows = cursor.fetchall()
#                     data = [dict(zip(columns, row)) for row in rows]
#                     return JsonResponse({"message": "Found", "data": data}, status=200)

                
#                 if not data:
#                     return JsonResponse({"message": "No matching records found."}, status=404)

#                 return JsonResponse(data, safe=False)

#             except Exception as e:
#                 return JsonResponse({"error": str(e)}, status=500)


# def show_field_selection(request):
# # ==================== Basic Retrival Queries ====================
# # | Method           | Description                               |
# # | ---------------- | ----------------------------------------- |
# # | `.values()`      | Returns list of dictionaries              |
# # | `.values_list()` | Returns list of tuples                    |
# # | `.only()`        | Fetch only selected fields (optimization) |
# # | `.defer()`       | Defer loading of selected fields          |
# # ================================================================
#     return render(request, "Field_Selection/field_selection.html")



# def show_ordering_uniqueness(request):
# # ======================  ====================== 
# # | Method        | Description                             |
# # | ------------- | --------------------------------------- |
# # | `.order_by()` | Sort query results                      |
# # | `.distinct()` | Remove duplicate rows (based on fields) |
# # | `.reverse()`  | Reverse the order of results            |
#     return render(request, "Ordering_Uniqueness/ordering_uniqueness.html")

# # def show_Jobs(request):
# #     return render(request, "Job/job.html")