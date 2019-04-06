from django.conf.urls import url
from . import views

app_name = 'userauth'

urlpatterns = [
            url(r'^$',views.customerindex,name='customerlogin'),
            url(r'^sys/admin/$',views.admin_index,name='admin_index')
]
