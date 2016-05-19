from django.conf.urls import url

from . import views

app_name = 'projects'

urlpatterns = [
	url(r'^$' , views.myProjects , name = 'myProjects') ,
	url(r'^myApplications$' , views.myApplications , name = 'myApplications') ,
	url(r'^projectsByType/(?P<type>\w*)$' , views.projectsByType , name = 'projectsByType') ,
	url(r'^projectDetail$' , views.projectDetail , name='projectDetail'),
	url(r'^quickCreate$' , views.projectQuickCreate , name = 'projectQuickCreate'),
	url(r'^projectDetail/(?P<project_id>[0-9]*)$' , views.project_details , name = 'projectDetailsById'),
	url(r'^projectDetail/(?P<project_id>[0-9]*)/createTask$' , views.create_task , name = 'createTask'),
	url(r'^projectDetail/(?P<project_id>[0-9]*)/deleteTask/(?P<task_id>[0-9]*)$' , views.delete_task , name = 'deleteTask'),
	url(r'^projectDetail/(?P<project_id>[0-9]*)/addMember$' , views.add_member , name = 'addMember'),
	url(r'^projectDetail/(?P<project_id>[0-9]*)/deleteMember/(?P<member_id>[0-9]*)$' , views.delete_member , name = 'deleteMember'),
	url(r'^findProject$' , views.findProject , name = 'findProject'),
	url(r'^applyProject/(?P<project_id>[0-9]*)$' , views.applyProject , name = 'applyProject'),
	url(r'^applyForProject/(?P<project_id>[0-9]*)$' , views.applyForProject , name = 'applyForProject'),
	url(r'^reviewProject/(?P<project_id>[0-9]*)$' , views.reviewProject , name = 'reviewProject'),
	url(r'^projectDetail/(?P<project_id>[0-9]*)/changeTask/(?P<task_id>[0-9]*)$' , views.change_task , name = 'changeTask'),
	url(r'^projectDetail/(?P<project_id>[0-9]*)/addApplicant/(?P<member_id>[0-9]*)$' , views.addApplicant , name = 'addApplicant'),
	url(r'^projectDetail/(?P<project_id>[0-9]*)/deleteApplicant/(?P<member_id>[0-9]*)$' , views.deleteApplicant , name = 'deleteApplicant'),

]