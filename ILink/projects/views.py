from django.shortcuts import render
from datetime import datetime
from datetime import timedelta
from accounts.models import Account

# Create your views here.
def index(request) :
	return render(request , 'projects/myProjects.html')

def myProjects(request) :
	press_create = False
	create_project_succeed = False
	# import pdb
	# pdb.set_trace()
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
