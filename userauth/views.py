from django.shortcuts import render

# Create your views here.

def customerindex(request):
    return render(request,'userauth/customer_index.html',{})
