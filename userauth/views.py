from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .serializers import AdminuserSerializer
from django.contrib.auth import authenticate, login, logout
from .models import Defaultpasswords
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
# Create your views here.

def customerindex(request):
    if request.method == 'GET':
        return render(request,'customer/guest.html',{})

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
                messages.info(request,"The password you used is just temporary<br>please set a new one")
                return HttpResponseRedirect(reverse('userauth:user_set_password'))
            else:
                login(request,user)
                return HttpResponseRedirect(reverse('customer:index'))
        else:
            messages.warning(request,"Wrong credentials!")
            return HttpResponseRedirect(reverse('userauth:customerlogin'))
    else:
        if request.user is not None:
            logout(request)
        return render(request, 'userauth/customer_index.html', {})

def customer_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('userauth:customerindex'))

def admin_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('userauth:admin_index'))

def setpassword(request):
    if request.method == 'GET':
        return render(request,'userauth/user_set_password.html',{})

    elif request.method == 'POST':
        user = get_user(request.user.id)
        new_password = (request.POST['password']).strip()
        old_password = request.POST['old_password'].strip()
        if user:
            if len(new_password) > 0:
                default_password = check_if_password_default(old_password)
                if default_password:
                    default_password.delete()
                    user.set_password(new_password)
                    user.save()
                    login(request,user)
                    messages.success(request,"Password changed successfully!")
                    return HttpResponseRedirect(reverse('customer:index'))
                else:
                    messages.warning(request, "Password does not exist")
                    return HttpResponseRedirect(reverse('userauth:user_set_password'))
            else:
                messages.warning(request,"Password cannot be empty!")
                return HttpResponseRedirect(reverse('userauth:user_set_password'))
        else:
            messages.warning(request,"session expired")
            return HttpResponseRedirect(reverse('userauth:customerindex'))

@login_required(login_url='/sys/admin/')
def resetPassword(request):
    if request.method=='GET':
        return render(request,'userauth/admin_reset_password.html',{})
    elif request.method == 'POST':
        user = get_user(request.user.id)
        new_password = (request.POST['password']).strip()
        old_password = (request.POST['old_password']).strip()
        if user:
            if len(new_password)>0:
                true_old_password = user.check_password(old_password)
                if true_old_password:
                    user.set_password(new_password)
                    user.save()
                    login(request,user)
                    messages.success(request,"Password changed successfully!")
                    return HttpResponseRedirect(reverse('sysadmin:index'))

                else:
                    messages.warning(request, "Incorrect old password!")
                    return HttpResponseRedirect(reverse('userauth:user_reset_password'))
            else:
                messages.warning(request,"Password cannot be empty!")
                return HttpResponseRedirect(reverse('userauth:user_reset_password'))
        else:
            messages.warning(request,"session expired")
            return HttpResponseRedirect(reverse('userauth:admin_index'))


def admin_index(request):
    if request.method == 'GET':
        return render(request,'userauth/admin_index.html',{})

    elif request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']
        user = authenticate(request, username=username, password=password )
        print(user)
        print(username)
        print(password)
        if user is not None and user.is_staff:
            login(request,user)
            return HttpResponseRedirect(reverse('sysadmin:index'))
        else:
            messages.warning(request,"Wrong credentials!")
            return HttpResponseRedirect(reverse('userauth:admin_index'))

@login_required(login_url='/sys/admin/')
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
            # print(new_admin.errors)
            messages.warning(request,"Admin Registration Error Check email or username")
            return HttpResponseRedirect(reverse('sysadmin:index'))
