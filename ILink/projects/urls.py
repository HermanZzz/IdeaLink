from django.conf.urls import url

from . import views

app_name = 'projects'

urlpatterns = [
	url(r'^$' , views.myProjects , name = 'myProjects') ,
	url(r'^projectDetail$' , views.projectDetail , name='projectDetail'),
	url(r'^quickCreate$' , views.projectQuickCreate , name = 'projectQuickCreate'),
	url(r'^projectDetail/(?P<project_id>[0-9]*)$' , views.project_details , name = 'projectDetailsById'),
	url(r'^projectDetail/(?P<project_id>[0-9]*)/createTask$' , views.create_task , name = 'createTask'),
	url(r'^projectDetail/(?P<project_id>[0-9]*)/deleteTask/(?P<task_id>[0-9]*)$' , views.delete_task , name = 'deleteTask'),
]