from django.shortcuts import render

# Create your views here.

def index(request):
    if request.method=='GET':
        return render(request,'sysadmin/index.html',{})

def alltransactions(request):
    if request.method == 'GET':
        return render(request, 'sysadmin/alltransactions.html',{})

def viewaccounts(request):
    if request.method=='GET':
        return render(request,'sysadmin/viewaccounts.html',{})

def add_customer(request):
    if request.method == 'GET':
        return render(request, 'sysadmin/addcustomer.html',{})

def makedeposit(request):
    if request.method== 'GET':
        return render(request, 'sysadmin/makedeposit.html',{})
