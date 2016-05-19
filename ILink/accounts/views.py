from django.shortcuts import render
from django.http import HttpResponseRedirect

import hashlib
import datetime

from .models import Account , ContactInfo

def index(request) :
	return render(request , 'home.html')

# Unfinished
def settingProfile(request) :
	# validate user session
	try:
		account = Account.objects.get(_account_name = request.session['account_name'])
	except Exception, e:
		return render(request , 'accounts/login.html' , {
			'is_login_success' : False,
			'is_register_success' : False,
			'is_first_time_to_this_page' : False,
			})

	#import pdb; pdb.set_trace()

	if not hasattr(account , 'contactinfo') :
		ContactInfo.objects.create( account = account ,
			_contactinfo_name = '' , _contactinfo_gender = '' ,
			_contactinfo_birthdate = datetime.datetime.today() , 
			_contactinfo_cellphone = '' , _contactinfo_address = '' , 
			_contactinfo_description = '')

	# check profile info
	try:
		user_name = request.POST['username']
		if request.POST['gender'] == 'Option one' :
			user_gender = 'Male'
		else :
			user_gender = 'Female'
		user_birthdate = request.POST['birthdate']
		user_cellphone = request.POST['cellphone']
		user_address = request.POST['address']
		user_description = request.POST['description']

		account.contactinfo.update_contact_info(user_name , user_cellphone ,
			user_birthdate , user_gender , user_address , user_description)
		account.contactinfo.save()

	except Exception, e:
		return render(request , 'accounts/setting/profile.html',{
		'is_login_success' : True,
		'user_session' : account,
		'contactinfo' : account.contactinfo
		})
		
	

	return render(request , 'accounts/setting/profile.html',{
		'is_login_success' : True,
		'user_session' : account,
		'contactinfo' : account.contactinfo
		})

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
		start_date = datetime.datetime.strptime(request.POST['startDate'] , '%d-%m-%Y')
		end_date = datetime.datetime.strptime(request.POST['endDate'] , '%d-%m-%Y')
		job_description = request.POST['description']

		account.experience_set.create(_job_title = job_title , _description = job_description , 
			_start_date = start_date , _end_date = end_date)
	except Exception, e:
		# representation page
		return render(request , 'accounts/setting/experience.html',{
		'is_login_success' : True,
		'user_session' : account,
		'user_experience_list' : account.experience_set.all().order_by('-_start_date'),
		})	
	
	return render(request , 'accounts/setting/experience.html',{
		'is_login_success' : True,
		'user_session' : account,
		'user_experience_list' : account.experience_set.all().order_by('-_start_date'),
		})

def deleteExperience(request , experience_id):
	# validate user session
	try:
		account = Account.objects.get(_account_name = request.session['account_name'])
	except Exception, e:
		return render(request , 'accounts/login.html' , {
			'is_login_success' : False,
			'is_register_success' : False,
			'is_first_time_to_this_page' : False,
			})

	# Delete
	experience_for_delete = account.experience_set.filter(id = experience_id)
	for experience in experience_for_delete :
		experience.delete()

	return HttpResponseRedirect('/accounts/setting/experience')

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
		'user_skill_list' : account.skill_set.all().order_by('-_skill_proficiency'),
		})	
	
	return render(request , 'accounts/setting/skill.html',{
		'is_login_success' : True,
		'user_session' : account,
		'user_skill_list' : account.skill_set.all().order_by('-_skill_proficiency'),
		})

def deleteSkill(request , skill_id):
	# validate user session
	try:
		account = Account.objects.get(_account_name = request.session['account_name'])
	except Exception, e:
		return render(request , 'accounts/login.html' , {
			'is_login_success' : False,
			'is_register_success' : False,
			'is_first_time_to_this_page' : False,
			})

	# Delete
	skill_for_delete = account.skill_set.filter(id = skill_id)
	for skill in skill_for_delete :
		skill.delete()

	return HttpResponseRedirect('/accounts/setting/skill')

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

def showResume(request) :
	# validate user session
	try:
		account = Account.objects.get(_account_name = request.session['account_name'])
	except Exception, e:
		return render(request , 'accounts/login.html' , {
			'is_login_success' : False,
			'is_register_success' : False,
			'is_first_time_to_this_page' : False,
			})

	return render(request , 'accounts/resume.html',{
		'is_login_success' : True,
		'user_session' : account,
		'request_user' : account,
		'user_skill_list' : account.skill_set.all().order_by('-_skill_proficiency'),
		'user_experience_list' : account.experience_set.all().order_by('-_start_date'),
		})

def showResumeWithID(request, account_id):
	# validate user session
	try:
		account = Account.objects.get(_account_name = request.session['account_name'])
	except Exception, e:
		return render(request , 'accounts/login.html' , {
			'is_login_success' : False,
			'is_register_success' : False,
			'is_first_time_to_this_page' : False,
			})

	try:
		request_account = Account.objects.get(id=account_id)
	except Exception, e:
		return HttpResponseRedirect('/accounts/resume')

	return render(request , 'accounts/resume.html',{
		'is_login_success' : True,
		'user_session' : account,
		'request_user' : request_account,
		'user_skill_list' : request_account.skill_set.all().order_by('-_skill_proficiency'),
		'user_experience_list' : request_account.experience_set.all().order_by('-_start_date'),
		})
	
