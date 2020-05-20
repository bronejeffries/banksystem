from django.conf.urls import url
from . import views

app_name = 'userauth'

urlpatterns = [
    url(r'^$', views.customerindex, name='customerindex'),
    url(r'^login/signin/$', views.customerlogin, name='customerlogin'),
    url(r'^logout/customer/$', views.customer_logout, name='customer_logout'),
    url(r'^newaccount/setpassword/$', views.setpassword, name='user_set_password'),
    url(r'^resetpassword/admin/sys/$', views.resetPassword, name='user_reset_password'),
    url(r'^sys/admin/$', views.admin_index, name='admin_index'),
    url(r'^logout/admin/$', views.admin_logout, name='admin_logout'),
    url(r'^sys/admin/register/$', views.add_admin, name='add_admin')
]
