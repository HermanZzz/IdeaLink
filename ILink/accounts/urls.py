from django.conf.urls import url

from . import views

app_name = 'accounts'

urlpatterns = [
	url(r'^$' , views.index , name = 'index') ,
	url(r'^register$' , views.register , name = 'register') ,
	url(r'^login$' , views.login , name = 'login') ,
	url(r'^home$' , views.home , name='home'),
	url(r'^index$' , views.logout , name='logout'),
	url(r'^setting$' , views.setting , name='setting')
]