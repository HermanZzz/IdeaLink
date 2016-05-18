from django.shortcuts import render
from datetime import datetime
from datetime import timedelta
from accounts.models import Account
from django.http import HttpResponseRedirect
from .models import Project

# Create your views here.
def index(request) :
	return render(request , 'projects/myProjects.html')

def myProjects(request) :
	press_create = False
	create_project_succeed = False
	# validate user session
	try:
		account = Account.objects.get(_account_name = request.session['account_name'])
	
	except Exception, e:
		return render(request , 'accounts/login.html' , {	
			'is_login_success' : False,
			'is_register_success' : False,
			'is_first_time_to_this_page' : False,
			})

	return render(request , 'projects/myProjects.html',{
		'is_login_success' : True,
		'user_session' : account,
		'press_create' : False,
		'create_project_succeed' : False,
		'target_projects' : account.project_set.all() | Project.objects.filter(project_members__id = account.id)
		})

def projectsByType(request, type):
	press_create = False
	create_project_succeed = False
	# validate user session
	try:
		account = Account.objects.get(_account_name = request.session['account_name'])
	except Exception, e:
		return render(request , 'accounts/login.html' , {	
			'is_login_success' : False,
			'is_register_success' : False,
			'is_first_time_to_this_page' : False,
			})

	if type == 'All' :
		target_projects = account.project_set.all() | Project.objects.filter(project_members__id = account.id)
	elif type == 'Own' :
		target_projects = account.project_set.all()
	elif type == 'Member' :
		target_projects = Project.objects.filter(project_members__id = account.id)	
	else :
		target_projects = account.project_set.all() | Project.objects.filter(project_members__id = account.id)

	return render(request , 'projects/myProjects.html',{
		'is_login_success' : True,
		'user_session' : account,
		'press_create' : False,
		'create_project_succeed' : False,
		'target_projects' : target_projects
		})


def projectDetail(request) :
	# validate user session
	try:
		account = Account.objects.get(_account_name = request.session['account_name'])
	except Exception, e:
		return render(request , 'accounts/login.html' , {	
			'is_login_success' : False,
			'is_register_success' : False,
			'is_first_time_to_this_page' : False,
			})
	return render(request , 'projects/projectDetail.html',{
		'is_login_success' : True,
		'user_session' : account,
		})

def project_details(request , project_id):
	# validate user session
	try:
		account = Account.objects.get(_account_name = request.session['account_name'])
	except Exception, e:
		return render(request , 'accounts/login.html' , {
			'is_login_success' : False,
			'is_register_success' : False,
			'is_first_time_to_this_page' : False,
			})

	# Fetch project info
	current_project = account.project_set.get(id=project_id)
	pending_tasks = current_project.task_set.filter(task_status = 'Pending')
	underway_tasks = current_project.task_set.filter(task_status = 'Underway')
	finished_tasks = current_project.task_set.filter(task_status = 'Finished')
	return render(request , 'projects/projectDetail.html', {
		'is_login_success' : True,
		'user_session' : account,
		'current_project' : current_project,
		'pending_tasks' : pending_tasks,
		'underway_tasks' : underway_tasks,
		'finished_tasks' : finished_tasks
		})

def create_task(request, project_id):
	# validate user session
	try:
		account = Account.objects.get(_account_name = request.session['account_name'])
	except Exception, e:
		return render(request , 'accounts/login.html' , {
			'is_login_success' : False,
			'is_register_success' : False,
			'is_first_time_to_this_page' : False,
			})
	# Fetch project info and create new task
	try:
		current_project = account.project_set.get(id=project_id)

		task_name = request.POST['task_name']
		task_description = request.POST['task_description']

		current_project.task_set.create(task_name = task_name, task_description= task_description, task_start_date = datetime.now(),
			task_expire_time = (datetime.now() + timedelta(days=30)), task_status = 'Pending')
	except Exception, e:
		return HttpResponseRedirect('/projects/projectDetail/' + project_id)
	return HttpResponseRedirect('/projects/projectDetail/' + project_id)

def delete_task(request, project_id, task_id):
	# validate user session
	try:
		account = Account.objects.get(_account_name = request.session['account_name'])
	except Exception, e:
		return render(request , 'accounts/login.html' , {
			'is_login_success' : False,
			'is_register_success' : False,
			'is_first_time_to_this_page' : False,
			})
	# Fetch project info and create new task
	try:
		current_project = account.project_set.get(id=project_id)
		current_task = current_project.task_set.filter(id=task_id)
		for task in current_task :
			task.delete()
	except Exception, e:
		return HttpResponseRedirect('/projects/projectDetail/' + project_id)
	return HttpResponseRedirect('/projects/projectDetail/' + project_id)
	
def projectQuickCreate(request):
	press_create = False
	create_project_succeed = False
	# validate user session
	try:
		account = Account.objects.get(_account_name = request.session['account_name'])
	except Exception, e:
		return render(request , 'accounts/login.html' , {	
			'is_login_success' : False,
			'is_register_success' : False,
			'is_first_time_to_this_page' : False,
			})

	
	# check user input
	try:
		proj_name = request.POST['proj-name']
		proj_description = request.POST['description']
		
		account.project_set.create(project_name = proj_name , project_description = proj_description , 
			project_owner = account,project_start_date = datetime.now(), project_expire_date = (datetime.now() + timedelta(days = 30)))

		
	except Exception, e:
	
		return render(request , 'projects/myProjects.html' , {
			'is_login_success' : True,
			'press_create' : True,
			'create_project_succeed' : False,
			})

	return render(request , 'projects/projectDetail.html',{
		'is_login_success' : True,
		'user_session' : account,
		'press_create' : True,
		'create_project_succeed' : True,
		})
