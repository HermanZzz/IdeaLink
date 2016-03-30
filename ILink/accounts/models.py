from __future__ import unicode_literals
from datetime import datetime

from django.db import models

class Account(models.Model):
	"""
	Account informations for users

	"""
	_account_name = models.CharField(max_length = 30 , unique = True )
	_account_passwd = models.CharField(max_length = 50)
	_account_register_date = models.DateField()

	@property
	def account_name(self):
	    return self._account_name
	
	@property
	def account_passwd(self):
	    return self._account_passwd
	@account_passwd.setter
	def account_passwd(self , new_password) :
		self._account_passwd = new_password
	
	@property
	def account_register_date(self):
	    return self._account_register_date
	
	@classmethod
	def create(cls , name , password) :
		account = cls(_account_name = name , _account_passwd = password)
		account._account_register_date = datetime.now()
		return account


	# Representations
	def __str__(self) :
		account_info = 'Account: ' + self._account_name
		return account_info
	__repr__ = __str__
