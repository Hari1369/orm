from django.urls import path
from . import views

urlpatterns = [
    path('log_in/', views.log_in_page, name="log_in"),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.show_dashboard, name="dashboard")
]
