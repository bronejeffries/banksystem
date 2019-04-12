from django.conf.urls import url
from . import views

app_name='customer'

urlpatterns=[
        url(r'^$',views.index,name='index'),
        url(r'^transaction/init/$',views.maketransactions,name='maketransactions'),
        url(r'^viewtransactions/pending/$',views.viewpendingtransactions,name='viewpending')
]
