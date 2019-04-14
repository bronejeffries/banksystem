from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .serializers import TransferTransactionSerializer as TTS
from .models import Account
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.

@login_required(login_url='/')
def index(request):
    if request.method=='GET':
        context={}
        user_account = find_user_account(request)
        if user_account:
            pending_transactions = user_account.transfertransaction_set.filter(status='pending')
            deposits = user_account.deposittransaction_set.all()
            context['available_amount'] = user_account.available_amount
            context['pending_transactions'] = pending_transactions
            context['deposits'] = deposits
            return render(request,'customer/index.html',context)
        else:
            HttpResponseRedirect(reverse('userauth:customer_logout'))


@login_required(login_url='/')
def viewpendingtransactions(request):
    if request.method == 'GET':
        context={}
        user_account = find_user_account(request)
        if user_account:
            pending_transactions = user_account.transfertransaction_set.filter(status='pending')
            context['pending_transactions'] = pending_transactions
            return render(request, 'customer/viewpendingtransactions.html',context)
        else:
            return HttpResponseRedirect(reverse('userauth:customer_logout'))

@login_required(login_url='/')
def maketransactions(request):
    if request.method=='GET':
        return render(request,'customer/maketransactions.html',{})

    elif request.method=='POST':
        useraccount = None
        try:
            useraccount = request.user.account
        except RelatedObjectDoesNotExist:
            useraccount = False

        if useraccount:
            data = get_data_From_request(account = useraccount, request = request.POST)
            if data is not None:
                if check_sufficient_balance(account = useraccount, amount_threshold = data['amount']):
                    new_transaction_record = TTS(data=data)
                    if new_transaction_record.is_valid():
                        new_transaction_record.save()
                        reduce_account_balance(pk=useraccount.id, amount= data['amount'] )
                        messages.success(request,"successful transaction")
                        return HttpResponseRedirect(reverse('customer:maketransactions'))
                    else:
                        messages.warning(request,"something went wrong!")
                        print("transaction creation errors", new_transaction_record.errors)
                        return HttpResponseRedirect(reverse('customer:maketransactions'))
                else:
                    print('balance error','insufficient balance')
                    messages.warning(request,"unsuccessful Transaction<br>insufficient balance")
                    return HttpResponseRedirect(reverse('customer:maketransactions'))
            else:
                print('data error', 'something went wrong')
                return HttpResponseRedirect(reverse('customer:maketransactions'))
        else:
            messages.warning(request,"No account details Found for this session")
            return HttpResponseRedirect(reverse('customer:maketransactions'))

def get_account_by_id(pk):
    account = None
    try:
        account = Account.objects.get(id=pk)
    except Account.DoesNotExist:
        return False
    else:
        return account

def find_user_account(request):
    user_account = None
    try:
        user_account = request.user.account
    except RelatedObjectDoesNotExist:
        user_account = False
    finally:
        return user_account


def reduce_account_balance(pk=None, amount=None):
    if pk is not None and amount is not None:
        account = get_account_by_id(pk)
        if account:
            account.available_amount -= amount
            account.save()


def check_sufficient_balance(account=None,amount_threshold=None):
    sufficiency = False
    if account is not None and amount_threshold is not None:
        available_amount = account.available_amount
        if int(int(available_amount)-int(amount_threshold))>0:
            sufficiency = True
        return sufficiency
    else:
        return False

def get_data_From_request(account = None, request = None):
    transaction_data = {}
    if account is not None and request is not None:
        transaction_data['from_account'] = account.id
        transaction_data['bank_name'] = request['bank_name']
        transaction_data['country'] = request['country']
        transaction_data['account_name'] = request['account_name']
        transaction_data['account_number'] = request['account_number']
        transaction_data['amount'] = request['amount']

        return transaction_data
    else:
        return None
