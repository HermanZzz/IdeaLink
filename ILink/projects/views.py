from django.shortcuts import render

# Create your views here.
def index(request) :
	return render(request , 'projects/myProjects.html')

def myProjects(request) :
	return render(request , 'projects/myProjects.html')	

def projectDetail(request) :
	return render(request , 'projects/projectDetail.html')	

def projectQuickCreate(request):
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

		account.projects_set.create(project_name = proj_name , project_description = proj_description , 
			project_owner = account)
	except Exception, e:
		raise
	else :
		pass
	