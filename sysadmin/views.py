from django.shortcuts import render
import random
from django.http import HttpResponseRedirect
from django.urls import reverse
from userauth.models import Defaultpasswords
from customer.models import DepositTransaction, Account, TransferTransaction
from userauth.serializers import UserSerializer
from customer.serializers import ProfileSerializer, AccountSerializer, DepositTransactionSerializer
from django.contrib.auth.models import User
from customer.models import Account
from django.contrib import messages
from django.db.models import Count , Sum , Avg, Q, F, Min
from django.db.models.functions import TruncMonth, TruncYear
from django.contrib.auth.decorators import login_required
from userauth.decorators import permission_check_admin
from customer.views import get_account_by_id

# Create your views here.

def generate_random_password():
    return random.randint(1, 1002)

@login_required(login_url='/sys/admin/')
@permission_check_admin
def index(request):
    if request.method=='GET':
        context = {}
        Deposit_sum = DepositTransaction.objects.aggregate(Deposit_sum=Sum('amount'))['Deposit_sum']
        context['DepositSum'] = Deposit_sum if Deposit_sum is not None else 0
        context['Customer_count'] = Account.objects.count()
        context['transactions_init']= TransferTransaction.objects.count()
        context['pending_transactions'] = TransferTransaction.objects.filter(status='pending')
        return render(request,'sysadmin/index.html',context)

@login_required(login_url='/sys/admin/')
@permission_check_admin
def alltransactions(request):
    if request.method == 'GET':
        context={}
        context['transactions'] = TransferTransaction.objects.all()
        return render(request, 'sysadmin/alltransactions.html',context)

@login_required(login_url='/sys/admin/')
@permission_check_admin
def viewaccounts(request):
    if request.method=='GET':
        context={}
        context['customers'] = Account.objects.all()
        return render(request,'sysadmin/viewaccounts.html',context)

@login_required(login_url='/sys/admin/')
@permission_check_admin
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
        user_id = ""
        not_created = True
        while not_created:
            new_user = UserSerializer(data=userdata)
            if new_user.is_valid():
                new_user.save()
                user_id = new_user.data['id']
                profile_data['owner'] = user_id
                account_data['customer'] = user_id
                not_created = False
            else:
                username = userdata['username'][:-1]
                userdata['username'] = username

        new_profile = ProfileSerializer(data=profile_data)
        if new_profile.is_valid():
            new_profile.save()
            new_account = AccountSerializer(data=account_data)
            if new_account.is_valid():
                new_account.save()
                successmessage = "Customer registered successfully<br>"
                successmessage += "Online account credentials <br>"
                successmessage += "Username: "+ username + "<br>"
                successmessage += "Password: "+ userpassword + "<br>"
                messages.success(request, successmessage)
                return HttpResponseRedirect(reverse('sysadmin:add_customer'))
            else:
                print('account creation failed',new_account.errors)
                messages.danger(request, "Couldnt create account!")
                return HttpResponseRedirect(reverse('sysadmin:add_customer'))
        else:
            print('profile failed', new_profile.errors)
            messages.danger(request, 'Couldnt create profile')
            return HttpResponseRedirect(reverse('sysadmin:add_customer'))

def get_account(account_name, account_number):
    account = None
    try:
        account = Account.objects.get(account_name=account_name, account_number=account_number)
    except Account.DoesNotExist:
        return False
    else:
        return account

@login_required(login_url='/sys/admin/')
@permission_check_admin
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
            deposit_record_data = {
            'account':account.id,
            'amount':amount
            }
            new_deposit_record = DepositTransactionSerializer(data=deposit_record_data)
            if new_deposit_record.is_valid():
                new_deposit_record.save()
                account.available_amount += int(amount)
                account.save()
                messages.success(request,'Deposit successfully made')
                return HttpResponseRedirect(reverse('sysadmin:makedeposit'))
            else:
                print('deposit error', new_deposit_record.errors)
                messages.warning(request,'Transaction unsuccessful\n please check the account details ')
                return HttpResponseRedirect(reverse('sysadmin:makedeposit'))
        else:
            print('account issues', 'no account')
            messages.warning(request,'Transaction unsuccessful <br> please check the account details ')
            return HttpResponseRedirect(reverse('sysadmin:makedeposit'))


def get_transaction_by_id(pk):
    transaction = None;
    try:
        transaction = TransferTransaction.objects.get(id=pk)
    except TransferTransaction.DoesNotExist:
        transaction = False
    finally:
        return transaction

@login_required(login_url='/sys/admin/')
@permission_check_admin
def reverse_transaction(request, pk):
    if request.method == 'GET':
        transaction = get_transaction_by_id(pk)
        if transaction:
            account = get_account_by_id(transaction.from_account.id)
            amount_to_reverse = int(transaction.amount)
            account.available_amount += amount_to_reverse
            account.save()

            transaction.status = "reversed"
            transaction.save()

            messages.success(request, 'Transaction reversed successfully')
            return HttpResponseRedirect(reverse('sysadmin:index'))
        else:
            messages.danger(request, 'request error')
            return HttpResponseRedirect(reverse('sysadmin:index'))

    else:
        return HttpResponseRedirect(reverse('sysadmin:index'))
