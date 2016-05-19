from django.conf.urls import url

from . import views

app_name = 'projects'

urlpatterns = [
	url(r'^$' , views.myProjects , name = 'myProjects') ,
	url(r'^projectsByType/(?P<type>\w*)$' , views.projectsByType , name = 'projectsByType') ,
	url(r'^projectDetail$' , views.projectDetail , name='projectDetail'),
	url(r'^quickCreate$' , views.projectQuickCreate , name = 'projectQuickCreate'),
	url(r'^projectDetail/(?P<project_id>[0-9]*)$' , views.project_details , name = 'projectDetailsById'),
	url(r'^projectDetail/(?P<project_id>[0-9]*)/createTask$' , views.create_task , name = 'createTask'),
	url(r'^projectDetail/(?P<project_id>[0-9]*)/deleteTask/(?P<task_id>[0-9]*)$' , views.delete_task , name = 'deleteTask'),
	url(r'^projectDetail/(?P<project_id>[0-9]*)/addMember$' , views.add_member , name = 'addMember'),
	url(r'^projectDetail/(?P<project_id>[0-9]*)/deleteMember/(?P<member_id>[0-9]*)$' , views.delete_member , name = 'deleteMember'),
	url(r'^findProject$' , views.findProject , name = 'findProject'),
	url(r'^applyProject$' , views.applyProject , name = 'applyProject'),
	url(r'^projectDetail/(?P<project_id>[0-9]*)/changeTask/(?P<task_id>[0-9]*)$' , views.change_task , name = 'changeTask'),
]