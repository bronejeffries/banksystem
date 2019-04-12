from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .serializers import TransferTransactionSerializer as TTS
from .models import Account
# Create your views here.

def index(request):
    if request.method=='GET':
        return render(request,'customer/index.html',{})

def viewpendingtransactions(request):
    if request.method == 'GET':
        return render(request, 'customer/viewpendingtransactions.html',{})

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
                        reduce_account_balance(pk=useraccount.id, amount= data['amount'] )
                        new_transaction_record.save()
                        return HttpResponseRedirect(reverse('customer:maketransactions'))
                    else:
                        print("transaction creation errors", new_transaction_record.errors)
                else:
                    print('balance error','insufficient balance')
                    return HttpResponseRedirect(reverse('customer:maketransactions'))
            else:
                print('data error', 'something went wrong')
                return HttpResponseRedirect(reverse('customer:maketransactions'))
        return HttpResponseRedirect(reverse('customer:maketransactions'))

def get_account_by_id(pk):
    account = None
    try:
        account = Account.objects.get(id=pk)
    except Account.DoesNotExist:
        return False
    else:
        return account


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
