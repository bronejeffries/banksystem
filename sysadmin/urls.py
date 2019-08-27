from django.conf.urls import url
from . import views

app_name = "sysadmin"

urlpatterns = [
        url(r'^home/$',views.index,name='index'),
        url(r'^home/accounts/transactions/$',views.alltransactions,name='alltransactions'),
        url(r'^home/accounts/$',views.viewaccounts,name='viewaccounts'),
        url(r'^home/accountholders/$',views.add_customer,name='add_customer'),
        url(r'^home/accountholders/deposit/$',views.makedeposit,name='makedeposit'),
        url(r'^home/transactions/(?P<pk>[0-9]+)/reverse/$',views.reverse_transaction,name='reverse'),
        url(r'^home/accounts/(?P<id>[0-9]+)/delete/$',views.delete_customer,name='delete_account')
]
