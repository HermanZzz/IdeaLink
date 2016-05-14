from django.conf.urls import url

from . import views

app_name = 'projects'

urlpatterns = [
	url(r'^$' , views.myProjects , name = 'myProjects') ,
	url(r'^projectDetail$' , views.projectDetail , name='projectDetail'),
]