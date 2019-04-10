from django.shortcuts import render
import random
from django.http import HttpResponseRedirect
from django.urls import reverse
from userauth.models import Defaultpasswords
from userauth.serializers import UserSerializer
from customer.serializers import ProfileSerializer, AccountSerializer, DepositTransactionSerializer
from django.contrib.auth.models import User
from customer.models import Account

# Create your views here.

def generate_random_password():
    return random.randint(1, 1002)

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
    if request.method == 'POST':
        firstname = request.POST['firstname']
        middlename = request.POST['middlename']
        lastname = request.POST['lastname']
        email = request.POST['email']
        date_of_birth = request.POST['d_o_b']

        profile_data = {
        'firstname':firstname,
        'middlename':middlename,
        'lastname':lastname,
        'date_of_birth':date_of_birth
        }

        account_name = request.POST['account_name_hidden']
        account_type = request.POST['account_type']
        account_number = request.POST['account_number']

        account_data = {
        'account_name':account_name,
        'account_type':account_type,
        'account_number':account_number
        }

# check if default password is assigned already
        checkpassword = True
        username = request.POST['user_name_hidden']
        userpassword = None
        while checkpassword:
            userpassword = str(generate_random_password())
            obj,created = Defaultpasswords.objects.get_or_create(password=userpassword)
            if created:
                checkpassword = False
            # Generate password and add  it to the defaults models
        userdata = {
        'username':username,
        'email':email,
        'password':userpassword
        }
        new_user = UserSerializer(data=userdata)
        if new_user.is_valid():
            new_user.save()
            user_id = new_user.data['id']
            profile_data['owner'] = user_id
            account_data['customer'] = user_id
            new_profile = ProfileSerializer(data=profile_data)
            if new_profile.is_valid():
                new_profile.save()
                new_account = AccountSerializer(data=account_data)
                if new_account.is_valid():
                    new_account.save()
                    print(userpassword)
                    return HttpResponseRedirect(reverse('sysadmin:index'))
                else:
                    print('account creation failed',new_account.errors)
            else:
                print('profile failed', new_profile.errors)
        else:
            print('user failed',new_user.errors)

def get_account(account_name, account_number):
    account = None
    try:
        account = Account.objects.get(account_name=account_name, account_number=account_number)
    except Account.DoesNotExist:
        return False
    else:
        return account

def makedeposit(request):
    if request.method== 'GET':
        return render(request, 'sysadmin/makedeposit.html',{})
    elif request.method == 'POST':
        # find if the information corresponds to an account
        account_name = request.POST['account_name']
        account_number = request.POST['account_number']
        account = get_account(account_name, account_number)
        if account:
            amount = request.POST['amount']
            account.available_amount += int(amount)
            account.save()

            deposit_record_data = {
            'account':account.id,
            'amount':amount
            }

            new_deposit_record = DepositTransactionSerializer(data=deposit_record_data)
            if new_deposit_record.is_valid():
                new_deposit_record.save()
                return HttpResponseRedirect(reverse('sysadmin:makedeposit'))
            else:
                print('deposit error', new_deposit_record.errors)
                return HttpResponseRedirect(reverse('sysadmin:index'))
        else:
            print('account issues', 'no account')
            return HttpResponseRedirect(reverse('sysadmin:index'))
