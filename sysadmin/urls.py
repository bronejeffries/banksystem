from django.conf.urls import url
from . import views

app_name = "sysadmin"

urlpatterns = [
        url(r'^home/$',views.index,name='index')
]
