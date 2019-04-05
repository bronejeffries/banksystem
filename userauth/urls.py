from django.conf.urls import url
from . import views

app_name = 'userauth'

urlpatterns = [
            url(r'^$',views.customerindex,name='customerlogin')
]
