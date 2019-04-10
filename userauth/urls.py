from django.conf.urls import url
from . import views

app_name = 'userauth'

urlpatterns = [
            url(r'^$',views.customerindex,name='customerindex'),
            url(r'^login/$',views.customerlogin,name='customerlogin'),
            url(r'^newaccount/setpassword/$',views.setpassword,name='user_set_password'),
            url(r'^sys/admin/$',views.admin_index,name='admin_index'),
            url(r'^sys/admin/register/$',views.add_admin,name='add_admin')
]
