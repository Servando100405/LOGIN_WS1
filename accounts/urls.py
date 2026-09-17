from django.urls import path

from .views import (
    admin_dashboard_view,
    dashboard_view,
    index_view,
    login_view,
    logout_view,
    register_view,
    staff_dashboard_view,
)

urlpatterns = [
    path('', index_view, name='index'),
    path('index/', index_view, name='index'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('admin-dashboard/', admin_dashboard_view, name='admin_dashboard'),
    path('staff-dashboard/', staff_dashboard_view, name='staff_dashboard'),
    path('logout/', logout_view, name='logout'),
]
