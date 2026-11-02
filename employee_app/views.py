from datetime import date
from functools import wraps

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from .models import Employee, Department, Role
from .models import Role, UserProfile
from functools import wraps
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required

#admin
def admin_required(view_func):

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):

        try:
            user_role = request.user.userprofile.role.name

        except UserProfile.DoesNotExist:
            raise PermissionDenied

        if user_role.lower() != 'admin':
            raise PermissionDenied

        return view_func(request, *args, **kwargs)

    return wrapper

#login
def login_view(request):

    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':

        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        if not username:
            messages.error(request, 'Please enter username.')
            return render(request, 'login.html')

        if not password:
            messages.error(request, 'Please enter password.')
            return render(request, 'login.html')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('dashboard')

        messages.error(
            request,
            'Invalid username or password.'
        )

    return render(request, 'login.html')

#register
def register_view(request):

    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':

        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')

        if not username:
            messages.error(request, 'Please enter username.')
            return render(request, 'register.html')

        if not email:
            messages.error(request, 'Please enter email.')
            return render(request, 'register.html')

        if not password:
            messages.error(request, 'Please enter password.')
            return render(request, 'register.html')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return render(request, 'register.html')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        login(request, user)

        return redirect('dashboard')

    return render(request, 'register.html')

#logout
def logout_view(request):
    logout(request)
    return redirect('login')

#dashboard
@login_required
def dashboard(request):
    return render(request, 'dashboard.html')


#user
@login_required
def user_index(request):

    users = User.objects.all()

    search = request.GET.get('search', '').strip()

    if search:
        users = users.filter(
            Q(username__icontains=search) |
            Q(email__icontains=search)
        )

    selected_sort = request.GET.get(
        'sort',
        'username'
    )

    allowed_sorts = [
        'username',
        '-username',
        'email',
        '-email',
        'date_joined',
        '-date_joined',
    ]

    if selected_sort in allowed_sorts:

        users = users.order_by(selected_sort)

    else:

        selected_sort = 'username'

        users = users.order_by('username')


    selected_per_page = request.GET.get(
        'per_page',
        '10'
    )

    if selected_per_page not in [
        '5',
        '10',
        '20',
        '50'
    ]:

        selected_per_page = '10'


    paginator = Paginator(
        users,
        int(selected_per_page)
    )

    page_number = request.GET.get('page')

    page_obj = paginator.get_page(page_number)


    query_params = request.GET.copy()

    query_params.pop('page', None)

    query_string = query_params.urlencode()


    return render(
        request,
        'users/user_index.html',
        {
            'users': page_obj,
            'page_obj': page_obj,
            'search': search,
            'selected_sort': selected_sort,
            'selected_per_page': selected_per_page,
            'query_string': query_string,
        }
    )

@login_required
def create_user(request):

    if request.method == 'POST':

        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        role_id = request.POST.get('role', '')
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')

        errors = {}

        form_data = {
            'username': username,
            'email': email,
            'role': role_id,
        }

        if not username:
            errors['username'] = 'Please enter username.'

        elif User.objects.filter(username=username).exists():
            errors['username'] = 'Username already exists.'

        if not email:
            errors['email'] = 'Please enter email.'

        elif User.objects.filter(email=email).exists():
            errors['email'] = 'Email already exists.'

        if not role_id:
            errors['role'] = 'Please select role.'

        else:
            try:
                role = Role.objects.get(id=role_id)
            except (Role.DoesNotExist, ValueError):
                errors['role'] = 'Please select a valid role.'

        if not password:
            errors['password'] = 'Please enter password.'

        if not confirm_password:
            errors['confirm_password'] = 'Please confirm password.'

        elif password != confirm_password:
            errors['confirm_password'] = 'Passwords do not match.'

        if errors:
            return render(
                request,
                'users/create_user.html',
                {
                    'errors': errors,
                    'form_data': form_data,
                    'roles': Role.objects.all(),
                }
            )

        new_user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        UserProfile.objects.create(
            user=new_user,
            role=role
        )

        messages.success(request, 'User added successfully.')

        return redirect('user_index')

    return render(
        request,
        'users/create_user.html',
        {
            'roles': Role.objects.all(),
        }
    )

@login_required
def edit_user(request, user_id):

    user = get_object_or_404(User, id=user_id)

    user_profile, created = UserProfile.objects.get_or_create(
        user=user,
        defaults={
            'role': Role.objects.first()
        }
    )

    if request.method == 'POST':

        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        role_id = request.POST.get('role', '')
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')

        errors = {}

        form_data = {
            'username': username,
            'email': email,
            'role': role_id,
        }

        if not username:
            errors['username'] = 'Please enter username.'

        elif User.objects.filter(
            username=username
        ).exclude(id=user.id).exists():
            errors['username'] = 'Username already exists.'

        if not email:
            errors['email'] = 'Please enter email.'

        elif User.objects.filter(
            email=email
        ).exclude(id=user.id).exists():
            errors['email'] = 'Email already exists.'

        if not role_id:
            errors['role'] = 'Please select role.'

        else:
            try:
                role = Role.objects.get(id=role_id)
            except (Role.DoesNotExist, ValueError):
                errors['role'] = 'Please select a valid role.'

        # Password is optional while editing

        if password:

            if not confirm_password:
                errors['confirm_password'] = (
                    'Please confirm new password.'
                )

            elif password != confirm_password:
                errors['confirm_password'] = (
                    'Passwords do not match.'
                )

        if errors:
            return render(
                request,
                'users/edit_user.html',
                {
                    'user': user,
                    'user_profile': user_profile,
                    'errors': errors,
                    'form_data': form_data,
                    'roles': Role.objects.all(),
                }
            )

        user.username = username
        user.email = email

        if password:
            user.set_password(password)

        user.save()

        user_profile.role = role
        user_profile.save()

        messages.success(
            request,
            'User updated successfully.'
        )

        return redirect('user_index')

    return render(
        request,
        'users/edit_user.html',
        {
            'user': user,
            'user_profile': user_profile,
            'roles': Role.objects.all(),
        }
    )

@login_required
def remove_user(request, user_id):

    user = get_object_or_404(User, id=user_id)

    if user == request.user:
        messages.error(request, 'You cannot delete your own account.')
        return redirect('user_index')

    user.delete()

    messages.success(request, 'User deleted successfully.')

    return redirect('user_index')

# employee  
@login_required
def index(request):

    search = request.GET.get('search', '').strip()

    employees = Employee.objects.select_related(
        'dept',
        'role'
    ).all()

    if search:
        employees = employees.filter(
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(phone__icontains=search) |
            Q(role__name__icontains=search) |
            Q(dept__name__icontains=search)
        )

    sort = request.GET.get('sort', '-id')

    allowed_sort_fields = {
        'first_name': 'first_name',
        '-first_name': '-first_name',
        'last_name': 'last_name',
        '-last_name': '-last_name',
        'phone': 'phone',
        '-phone': '-phone',
        'role': 'role__name',
        '-role': '-role__name',
        'department': 'dept__name',
        '-department': '-dept__name',
        'salary': 'salary',
        '-salary': '-salary',
        'hire_date': 'hire_date',
        '-hire_date': '-hire_date',
    }

    sort_value = allowed_sort_fields.get(sort, '-id')

    employees = employees.order_by(sort_value)

    per_page = request.GET.get('per_page', '10')

    if per_page not in ['5', '10', '20', '50']:
        per_page = '10'

    paginator = Paginator(
        employees,
        int(per_page)
    )

    page_number = request.GET.get('page')

    page_obj = paginator.get_page(page_number)

    query_params = request.GET.copy()
    query_params.pop('page', None)

    context = {
        'employees': page_obj,
        'page_obj': page_obj,
        'search': search,
        'selected_sort': request.GET.get('sort', '-id'),
        'selected_per_page': per_page,
        'query_string': query_params.urlencode(),
    }

    return render(
        request,
        'employees/index.html',
        context
    )

@login_required

def create_emp(request):

    departments = Department.objects.all()
    roles = Role.objects.all()

    if request.method == 'POST':

        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        phone = request.POST.get('phone', '').strip()
        salary = request.POST.get('salary', '').strip()
        bonus = request.POST.get('bonus', '').strip()
        dept = request.POST.get('dept', '').strip()
        role = request.POST.get('role', '').strip()

        errors = {}

        if not first_name:
            errors['first_name'] = 'Please enter first name.'

        if not last_name:
            errors['last_name'] = 'Please enter last name.'

        if not phone:
            errors['phone'] = 'Please enter phone number.'
        elif not phone.isdigit():
            errors['phone'] = 'Please enter a valid phone number.'

        if not salary:
            errors['salary'] = 'Please enter salary.'
        elif not salary.isdigit():
            errors['salary'] = 'Please enter a valid salary.'

        if not bonus:
            errors['bonus'] = 'Please enter bonus.'
        elif not bonus.isdigit():
            errors['bonus'] = 'Please enter a valid bonus.'

        if not dept:
            errors['dept'] = 'Please select department.'

        if not role:
            errors['role'] = 'Please select role.'

        if errors:
            return render(
                request,
                'employees/create_emp.html',
                {
                    'departments': departments,
                    'roles': roles,
                    'errors': errors,
                    'form_data': request.POST,
                }
            )

        employee = Employee(
            first_name=first_name,
            last_name=last_name,
            salary=int(salary),
            bonus=int(bonus),
            phone=int(phone),
            dept_id=int(dept),
            role_id=int(role),
            hire_date=date.today()
        )

        employee.save()

        messages.success(
            request,
            'Employee created successfully!'
        )

        return redirect('index')

    return render(
        request,
        'employees/create_emp.html',
        {
            'departments': departments,
            'roles': roles,
        }
    )
@login_required

def show_emp(request, emp_id):

    employee = get_object_or_404(
        Employee.objects.select_related(
            'dept',
            'role'
        ),
        id=emp_id
    )

    return render(
        request,
        'employees/show_emp.html',
        {
            'employee': employee
        }
    )

@login_required

def edit_emp(request, emp_id):

    employee = get_object_or_404(
        Employee,
        id=emp_id
    )

    departments = Department.objects.all()
    roles = Role.objects.all()

    if request.method == 'POST':

        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        phone = request.POST.get('phone', '').strip()
        salary = request.POST.get('salary', '').strip()
        bonus = request.POST.get('bonus', '').strip()
        dept = request.POST.get('dept', '').strip()
        role = request.POST.get('role', '').strip()

        errors = {}

        if not first_name:
            errors['first_name'] = 'Please enter first name.'

        if not last_name:
            errors['last_name'] = 'Please enter last name.'

        if not phone:
            errors['phone'] = 'Please enter phone number.'
        elif not phone.isdigit():
            errors['phone'] = 'Please enter a valid phone number.'

        if not salary:
            errors['salary'] = 'Please enter salary.'
        elif not salary.isdigit():
            errors['salary'] = 'Please enter a valid salary.'

        if not bonus:
            errors['bonus'] = 'Please enter bonus.'
        elif not bonus.isdigit():
            errors['bonus'] = 'Please enter a valid bonus.'

        if not dept:
            errors['dept'] = 'Please select department.'

        if not role:
            errors['role'] = 'Please select role.'

        if errors:
            return render(
                request,
                'employees/edit_emp.html',
                {
                    'employee': employee,
                    'departments': departments,
                    'roles': roles,
                    'errors': errors,
                    'form_data': request.POST,
                }
            )

        employee.first_name = first_name
        employee.last_name = last_name
        employee.salary = int(salary)
        employee.bonus = int(bonus)
        employee.phone = int(phone)
        employee.dept_id = int(dept)
        employee.role_id = int(role)

        employee.save()

        messages.success(
            request,
            'Employee updated successfully!'
        )

        return redirect('index')

    return render(
        request,
        'employees/edit_emp.html',
        {
            'employee': employee,
            'departments': departments,
            'roles': roles,
        }
    )
@login_required

def remove_emp(request, emp_id):

    if request.method == 'POST':

        employee = get_object_or_404(
            Employee,
            id=emp_id
        )

        employee.delete()

        messages.success(
            request,
            'Employee deleted successfully!'
        )

    return redirect('index')

#roles
@login_required

def role_index(request):

    roles = Role.objects.all()

    search = request.GET.get('search', '').strip()

    if search:
        roles = roles.filter(
            name__icontains=search
        )

    selected_sort = request.GET.get('sort', 'name')

    if selected_sort in ['name', '-name']:
        roles = roles.order_by(selected_sort)
    else:
        selected_sort = 'name'
        roles = roles.order_by('name')

    selected_per_page = request.GET.get('per_page', '10')

    if selected_per_page not in ['5', '10', '20', '50']:
        selected_per_page = '10'

    paginator = Paginator(
        roles,
        int(selected_per_page)
    )

    page_number = request.GET.get('page')

    page_obj = paginator.get_page(page_number)

    query_params = request.GET.copy()
    query_params.pop('page', None)

    query_string = query_params.urlencode()

    return render(
        request,
        'roles/role_index.html',
        {
            'roles': page_obj,
            'page_obj': page_obj,
            'search': search,
            'selected_sort': selected_sort,
            'selected_per_page': selected_per_page,
            'query_string': query_string,
        }
    )

@login_required

def create_role(request):

    if request.method == 'POST':

        name = request.POST.get('name', '').strip()

        errors = {}

        if not name:
            errors['name'] = 'Please enter role name.'

        if errors:
            return render(
                request,
                'roles/create_role.html',
                {
                    'errors': errors,
                    'form_data': request.POST,
                }
            )

        Role.objects.create(
            name=name
        )

        messages.success(
            request,
            'Role created successfully!'
        )

        return redirect('role_index')

    return render(
        request,
        'roles/create_role.html'
    )

@login_required

def show_role(request, role_id):

    role = get_object_or_404(
        Role,
        id=role_id
    )

    return render(
        request,
        'roles/show_role.html',
        {
            'role': role
        }
    )

@login_required

def edit_role(request, role_id):

    role = get_object_or_404(
        Role,
        id=role_id
    )

    if request.method == 'POST':

        name = request.POST.get('name', '').strip()

        errors = {}

        if not name:
            errors['name'] = 'Please enter role name.'

        if errors:
            return render(
                request,
                'roles/edit_role.html',
                {
                    'role': role,
                    'errors': errors,
                    'form_data': request.POST,
                }
            )

        role.name = name

        role.save()

        messages.success(
            request,
            'Role updated successfully!'
        )

        return redirect('role_index')

    return render(
        request,
        'roles/edit_role.html',
        {
            'role': role
        }
    )
@login_required

def remove_role(request, role_id):

    if request.method == 'POST':

        role = get_object_or_404(
            Role,
            id=role_id
        )

        role.delete()

        messages.success(
            request,
            'Role deleted successfully!'
        )

    return redirect('role_index')

@login_required

#departments
def department_index(request):

    departments = Department.objects.all()

    search = request.GET.get('search', '').strip()

    if search:
        departments = departments.filter(
            name__icontains=search
        )

    selected_sort = request.GET.get('sort', 'name')

    if selected_sort in [
        'name',
        '-name',
        'location',
        '-location'
    ]:
        departments = departments.order_by(
            selected_sort
        )
    else:
        selected_sort = 'name'
        departments = departments.order_by('name')

    selected_per_page = request.GET.get(
        'per_page',
        '10'
    )

    if selected_per_page not in [
        '5',
        '10',
        '20',
        '50'
    ]:
        selected_per_page = '10'

    paginator = Paginator(
        departments,
        int(selected_per_page)
    )

    page_number = request.GET.get('page')

    page_obj = paginator.get_page(
        page_number
    )

    query_params = request.GET.copy()
    query_params.pop('page', None)

    query_string = query_params.urlencode()

    return render(
        request,
        'departments/department_index.html',
        {
            'departments': page_obj,
            'page_obj': page_obj,
            'search': search,
            'selected_sort': selected_sort,
            'selected_per_page': selected_per_page,
            'query_string': query_string,
        }
    )

@login_required

def create_dep(request):

    if request.method == 'POST':

        name = request.POST.get('name', '').strip()
        location = request.POST.get('location', '').strip()

        errors = {}

        if not name:
            errors['name'] = 'Please enter department name.'

        if not location:
            errors['location'] = 'Please enter department location.'

        if errors:
            return render(
                request,
                'departments/create_dep.html',
                {
                    'errors': errors,
                    'form_data': request.POST,
                }
            )

        Department.objects.create(
            name=name,
            location=location
        )

        messages.success(
            request,
            'Department created successfully!'
        )

        return redirect('department_index')

    return render(
        request,
        'departments/create_dep.html'
    )

@login_required

def show_dep(request, dep_id):

    department = get_object_or_404(
        Department,
        id=dep_id
    )

    return render(
        request,
        'departments/show_dep.html',
        {
            'department': department
        }
    )

@login_required

def edit_dep(request, dep_id):

    department = get_object_or_404(
        Department,
        id=dep_id
    )

    if request.method == 'POST':

        name = request.POST.get('name', '').strip()
        location = request.POST.get('location', '').strip()

        errors = {}

        if not name:
            errors['name'] = 'Please enter department name.'

        if not location:
            errors['location'] = 'Please enter department location.'

        if errors:
            return render(
                request,
                'departments/edit_dep.html',
                {
                    'department': department,
                    'errors': errors,
                    'form_data': request.POST,
                }
            )

        department.name = name
        department.location = location

        department.save()

        messages.success(
            request,
            'Department updated successfully!'
        )

        return redirect('department_index')

    return render(
        request,
        'departments/edit_dep.html',
        {
            'department': department
        }
    )

@login_required

def remove_dep(request, dep_id):

    if request.method == 'POST':

        department = get_object_or_404(
            Department,
            id=dep_id
        )

        department.delete()

        messages.success(
            request,
            'Department deleted successfully!'
        )

    return redirect('department_index')