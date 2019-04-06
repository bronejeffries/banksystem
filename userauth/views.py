from django.shortcuts import render

# Create your views here.

def customerindex(request):
    if request.method == 'GET':
        return render(request,'userauth/customer_index.html',{})

def admin_index(request):
    if request.method == 'GET':
        return render(request,'userauth/admin_index.html',{})
