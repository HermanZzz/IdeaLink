from django.shortcuts import render

import hashlib

from .models import Account

def index(request) :
	return render(request , 'home.html')

def setting(request) :
	return render(request , 'accounts/setting.html',{
		'is_login_success' : True,
		'user_session' : Account.objects.get(_account_name = request.session['account_name'])
		})

def settingContact(request) :
	return render(request , 'accounts/setting/contact.html',{
		'is_login_success' : True,
		'user_session' : Account.objects.get(_account_name = request.session['account_name'])
		})

def settingExperience(request) :
	return render(request , 'accounts/setting/experience.html',{
		'is_login_success' : True,
		'user_session' : Account.objects.get(_account_name = request.session['account_name'])
		})
	

def home(request) :
	return render(request , 'home.html' , {
			'is_login_success' : True,
			'user_session' : Account.objects.get(_account_name = request.session['account_name']),
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
