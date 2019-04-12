from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .serializers import AdminuserSerializer
from django.contrib.auth import authenticate, login, logout
from .models import Defaultpasswords
from django.contrib.auth.models import User
from django.contrib import messages
# Create your views here.

def customerindex(request):
    if request.method == 'GET':
        return render(request,'userauth/customer_index.html',{})

def check_if_password_default(password):
    password_obj = None
    try:
        password_obj = Defaultpasswords.objects.get(password=password)
    except Defaultpasswords.DoesNotExist:
        return False
    else:
        return password_obj

def get_user(pk):
    user = None
    try:
        user = User.objects.get(id=pk)
    except User.DoesNotExist:
        return False
    else:
        return user

def customerlogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # authenticate and check whether password is in defaults
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_active and not user.is_staff:
            password_obj = check_if_password_default(password)
                    # redirect to corresponding view function
            if password_obj:
                login(request,user)
                return HttpResponseRedirect(reverse('userauth:user_set_password'))
            else:
                login(request,user)
                print('user logined in successfully')
                return HttpResponseRedirect(reverse('customer:index'))

        else:
            return HttpResponseRedirect(reverse('userauth:customerindex'))
    else:
        raise Exception("method not allowed")

def setpassword(request):
    if request.method == 'GET':
        return render(request,'userauth/user_set_password.html',{})

    elif request.method == 'POST':
        user = get_user(request.user.id)
        new_password = request.POST['password']
        print(request.user.id)
        if user:
            if len(new_password) > 0:
                user.set_password(new_password)
                user.save()
                login(request,user)
                return HttpResponseRedirect(reverse('customer:index'))
            else:
                print('no password set')
                return HttpResponseRedirect(reverse('userauth:user_set_password'))
        else:
            return HttpResponseRedirect(reverse('userauth:customerindex'))


def admin_index(request):
    if request.method == 'GET':
        return render(request,'userauth/admin_index.html',{})

    elif request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']
        user = authenticate(request, username=username, password=password )
        if user is not None and user.is_staff:
            login(request,user)
            return HttpResponseRedirect(reverse('sysadmin:index'))
        else:
            return HttpResponseRedirect(reverse('userauth:admin_index'))

def add_admin(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        userdata={
        'username':username,
        'email':email,
        'password':password
        }

        new_admin = AdminuserSerializer(data=userdata)
        if new_admin.is_valid():
            new_admin.save()
            messages.success(request,'New admin registered successfully')
            return HttpResponseRedirect(reverse('sysadmin:index'))
        else:
            messages.warning(request, new_admin.errors['username'][0] if new_admin.errors['username'] else "Registration Error")
            return HttpResponseRedirect(reverse('sysadmin:index'))
