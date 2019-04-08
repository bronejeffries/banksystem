from django.conf.urls import url
from . import views

app_name = "sysadmin"

urlpatterns = [
        url(r'^home/$',views.index,name='index'),
        url(r'^home/accounts/transactions/$',views.alltransactions,name='alltransactions'),
        url(r'^home/accountholders/$',views.add_customer,name='add_customer')
]
