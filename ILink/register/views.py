from django.shortcuts import render

import hashlib

from .models import Account

def index(request) :
	return render(request , 'register/register.html')

def register(request) :

	is_register_success = False

	# Fetch register information
	try :
		account_name = request.POST['account_name']
		account_password = request.POST['account_password']
		if '' == account_name or '' == account_password :
			raise KeyError('Invalid account')
	except (KeyError):
		return render(request , 'register/results.html' , {
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
		return render(request , 'register/results.html' , {
			'is_register_success' : is_register_success ,
			})

	# Success		
	is_register_success = True	

	return render(request , 'register/results.html' , {
		'account_name' : account_name , 
		'account_password' : account_password ,
		'is_register_success' : is_register_success ,
		})