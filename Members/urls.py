from django.urls import include, path
from . import views
from rest_framework.routers import DefaultRouter
from .views import api_getdata

router = DefaultRouter()
router.register('test_1', api_getdata)


urlpatterns = [
    path('log_in/', views.log_in_page, name="log_in"),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.show_dashboard, name="dashboard"),
    
    # ==============> MEMBERS
    path('members/', views.show_member, name="members"),
    path('company/', views.show_company, name="company"),
    
    path('api_data/', views.show_api_page, name="api_data"),
    path('api_page_json/', views.api_page, name="api_page_json"),
    
    path('department/', include(router.urls)),

    # =====================================> CHANGED API TO DEPARTMENT
    # path('', include(router.urls)),
    # =====================================> CHANGED API TO DEPARTMENT

]


from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns += [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
