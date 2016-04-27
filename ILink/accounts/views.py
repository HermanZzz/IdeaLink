from django.shortcuts import render

import hashlib

from .models import Account

def index(request) :
	return render(request , 'home.html')

# Unfinished
def setting(request) :
	# validate user session
	try:
		account = Account.objects.get(_account_name = request.session['account_name'])
	except Exception, e:
		return render(request , 'accounts/login.html' , {
			'is_login_success' : False,
			'is_register_success' : False,
			'is_first_time_to_this_page' : False,
			})

	# check profile info
	

	return render(request , 'accounts/setting.html',{
		'is_login_success' : True,
		'user_session' : account
		})

# Basic function done , need to be updated according to the issue pushed on the github
def settingContact(request) :
	# validate user session
	try:
		account = Account.objects.get(_account_name = request.session['account_name'])
	except Exception, e:
		return render(request , 'accounts/login.html' , {
			'is_login_success' : False,
			'is_register_success' : False,
			'is_first_time_to_this_page' : False,
			})

	# Fetch user configuration
	try:
		job_title = request.POST['title']
		start_date = request.POST['start']
		end_date = request.POST['end']
		job_description = request.POST['description']

		account.experience_set.create(_job_title = job_title , _description = job_description , 
			_start_date = start_date , _end_date = end_date)
	except Exception, e:
		# representation page
		return render(request , 'accounts/setting/contact.html',{
		'is_login_success' : True,
		'user_session' : account,
		'user_experience_list' : account.experience_set.all(),
		})	
	
	return render(request , 'accounts/setting/contact.html',{
		'is_login_success' : True,
		'user_session' : account,
		'user_experience_list' : account.experience_set.all(),
		})

# Basic function done , need to be updated according to the issue pushed on the github
def settingExperience(request) :
	# validate user session
	try:
		account = Account.objects.get(_account_name = request.session['account_name'])
	except Exception, e:
		return render(request , 'accounts/login.html' , {
			'is_login_success' : False,
			'is_register_success' : False,
			'is_first_time_to_this_page' : False,
			})

	# Fetch user configuration
	try:
		job_title = request.POST['title']
		start_date = request.POST['start']
		end_date = request.POST['end']
		job_description = request.POST['description']

		account.experience_set.create(_job_title = job_title , _description = job_description , 
			_start_date = start_date , _end_date = end_date)
	except Exception, e:
		# representation page
		return render(request , 'accounts/setting/experience.html',{
		'is_login_success' : True,
		'user_session' : account,
		'user_experience_list' : account.experience_set.all(),
		})	
	
	return render(request , 'accounts/setting/experience.html',{
		'is_login_success' : True,
		'user_session' : account,
		'user_experience_list' : account.experience_set.all(),
		})

# Basic function done , need to be updated according to the issue pushed on the github
def settingSkill(request) :
	# validate user session
	try:
		account = Account.objects.get(_account_name = request.session['account_name'])
	except Exception, e:
		return render(request , 'accounts/login.html' , {
			'is_login_success' : False,
			'is_register_success' : False,
			'is_first_time_to_this_page' : False,
			})

	# Fetch user configuration
	try:
		skill_type = request.POST['skill_type']
		skill_proficiency = request.POST['skill_proficiency']
		skill_description = request.POST['skill_description']
		account.skill_set.create(_skill_type = skill_type , _skill_proficiency=skill_proficiency , _skill_description = skill_description)
	except Exception, e:
		# representation page
		return render(request , 'accounts/setting/skill.html',{
		'is_login_success' : True,
		'user_session' : account,
		'user_skill_list' : account.skill_set.all(),
		})	
	
	return render(request , 'accounts/setting/skill.html',{
		'is_login_success' : True,
		'user_session' : account,
		'user_skill_list' : account.skill_set.all(),
		})

def home(request) :
	# validate user session
	try:
		account = Account.objects.get(_account_name = request.session['account_name'])
	except Exception, e:
		return render(request , 'accounts/login.html' , {
			'is_login_success' : False,
			'is_register_success' : False,
			'is_first_time_to_this_page' : False,
			})

	return render(request , 'home.html' , {
			'is_login_success' : True,
			'user_session' : account,
			})

def logout(request):
	del request.session['account_name']
	return render(request , 'home.html')

def register(request) :

	is_register_success = False

	# Fetch register information
	try :
		account_name = request.POST['account_name']
		account_password = request.POST['account_password']
		if '' == account_name or '' == account_password :
			raise KeyError('Invalid account')
	except (KeyError):
		return render(request , 'accounts/register.html' , {
			'is_register_success' : is_register_success ,
			'is_first_time_to_this_page' : True,
			})

	# Encode account password
	md5 = hashlib.md5()
	md5.update(account_password.encode('utf-8'))
	account_password = md5.hexdigest()

	# Create new account
	new_account = Account.create(account_name , account_password)
	try :
		new_account.save()
	except BaseException  :
		return render(request , 'accounts/register.html' , {
			'is_register_success' : is_register_success ,
			'is_first_time_to_this_page' : False,
			})

	# Success		
	is_register_success = True	

	return render(request , 'accounts/login.html' , {
		'is_register_success' : True,
		'is_first_time_to_this_page' : False,
		})

def login(request) :

	is_login_success = False

	# Fetch user configuration
	try:
		account_name = request.POST['account_name']
		account_password = request.POST['account_password']
		if '' == account_name or '' == account_password :
			raise KeyError('Invalid input')
	except(KeyError):
		return render(request , 'accounts/login.html' , {
			'is_login_success' : False,
			'is_register_success' : False,
			'is_first_time_to_this_page' : True,
			})

	# Encode account password
	md5 = hashlib.md5()
	md5.update(account_password.encode('UTF-8'))
	account_password = md5.hexdigest()

	# Account validation
	try:
		account_for_validation = Account.objects.get(_account_name = account_name)
	except Exception, e:
		return render(request , 'accounts/login.html' , {
			'is_login_success' : False,
			'is_register_success' : False,
			'is_first_time_to_this_page' : False,
			})
		
	
	if account_for_validation :
		if account_for_validation.account_passwd == account_password :
			is_login_success = True
			
			request.session['account_name'] = account_name
			request.session.SESSION_EXPIRE_AT_BROWSER_CLOSE = True

			return render(request , 'home.html' , {
			'is_login_success' : is_login_success,
			'user_session' : Account.objects.get(_account_name = account_name),
			})

	return render(request , 'accounts/login.html' , {
			'is_login_success' : False,
			'is_register_success' : False,
			'is_first_time_to_this_page' : False,
			})
