from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.

def customerindex(request):
    if request.method == 'GET':
        return render(request,'userauth/customer_index.html',{})

def admin_index(request):
    if request.method == 'GET':
        return render(request,'userauth/admin_index.html',{})

    elif request.method == 'POST':
        return HttpResponseRedirect(reverse('sysadmin:index'))
