from django.shortcuts import render

import hashlib
import pdb

from .models import Account

def index(request) :
	return render(request , 'accounts/register.html')
	#return render(request , 'accounts/login.html')

def register(request) :

	is_register_success = False

	# Fetch register information
	try :
		account_name = request.POST['account_name']
		account_password = request.POST['account_password']
		if '' == account_name or '' == account_password :
			raise KeyError('Invalid account')
	except (KeyError):
		return render(request , 'accounts/results.html' , {
			'is_register_success' : is_register_success ,
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
		return render(request , 'accounts/results.html' , {
			'is_register_success' : is_register_success ,
			})

	# Success		
	is_register_success = True	

	return render(request , 'accounts/results.html' , {
		'account_name' : account_name , 
		'account_password' : account_password ,
		'is_register_success' : is_register_success ,
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
		return render(request , 'accounts/loginresults.html' , {
			'is_login_success' : False,
			})

	# Encode account password
	md5 = hashlib.md5()
	md5.update(account_password.encode('UTF-8'))
	account_password = md5.hexdigest()

	# Account validation
	try:
		account_for_validation = Account.objects.get(_account_name = account_name)
	except Exception, e:
		return render(request , 'accounts/loginresults.html' , {
			'is_login_success' : False,
			})
		
	
	if account_for_validation :
		if account_for_validation.account_passwd == account_password :
			is_login_success = True

	return render(request , 'accounts/loginresults.html' , {
			'is_login_success' : is_login_success,
			})