"""
URL configuration for employee_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views



urlpatterns = [

    # AUTHENTICATION
    
    path(
    'login/',
    views.login_view,
    name='login'
),

  #LOGOUT

path(
    'logout/',
    views.logout_view,
    name='logout'
),

#REGISTER
path(
    'register/',
    views.register_view,
    name='register'
),

    #DASHBOARD
 path(
        'dashboard/',
        views.dashboard,
        name='dashboard'
    ),


    #USERS
    path(
    'users/',
    views.user_index,
    name='user_index'
),

path(
    'users/create/',
    views.create_user,
    name='create_user'
),

path(
    'users/edit/<int:user_id>/',
    views.edit_user,
    name='edit_user'
),

path(
    'users/delete/<int:user_id>/',
    views.remove_user,
    name='remove_user'
),

    # EMPLOYEES

    path('employees/', views.index, name='index'),

    path(
        'employees/create/',
        views.create_emp,
        name='create_emp'
    ),

    path(
        'employees/<int:emp_id>/',
        views.show_emp,
        name='show_emp'
    ),

    path(
        'employees/<int:emp_id>/edit/',
        views.edit_emp,
        name='edit_emp'
    ),

    path(
        'employees/<int:emp_id>/delete/',
        views.remove_emp,
        name='remove_emp'
    ),


    # ROLES

    path(
        'roles/',
        views.role_index,
        name='role_index'
    ),

    path(
        'roles/create/',
        views.create_role,
        name='create_role'
    ),

    path(
        'roles/<int:role_id>/',
        views.show_role,
        name='show_role'
    ),

    path(
        'roles/<int:role_id>/edit/',
        views.edit_role,
        name='edit_role'
    ),

    path(
        'roles/<int:role_id>/delete/',
        views.remove_role,
        name='remove_role'
    ),


    # DEPARTMENTS

    path(
        'departments/',
        views.department_index,
        name='department_index'
    ),

    path(
        'departments/create/',
        views.create_dep,
        name='create_dep'
    ),

    path(
        'departments/<int:dep_id>/',
        views.show_dep,
        name='show_dep'
    ),

    path(
        'departments/<int:dep_id>/edit/',
        views.edit_dep,
        name='edit_dep'
    ),

    path(
        'departments/<int:dep_id>/delete/',
        views.remove_dep,
        name='remove_dep'
    ),
]

