from django.shortcuts import render
from accounts.models import Account

# Create your views here.
def index(request) :
	return render(request , 'projects/myProjects.html')

def myProjects(request) :
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
	