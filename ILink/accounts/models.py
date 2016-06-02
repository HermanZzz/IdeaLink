from __future__ import unicode_literals
from datetime import datetime

from django.db import models

# Account for user login
class Account(models.Model):
	"""
	Account informations for users

	"""
	# Account info for register & login
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

# Contact info , one to one relation to user account
class ContactInfo(models.Model) :
	'''
	Contact information for users...
	One to one relationship to Account

	'''

	account = models.OneToOneField(
		Account,
		on_delete = models.CASCADE,
		primary_key=True,
	)

	_contactinfo_name = models.CharField(max_length=30, blank=True)
	_contactinfo_cellphone = models.CharField(max_length=20 , blank=True)
	_contactinfo_birthdate = models.CharField(max_length=50,blank=True)
	_contactinfo_gender = models.CharField(max_length=30 , blank=True)
	_contactinfo_address = models.CharField(max_length=50 , blank=True)
	_contactinfo_description = models.CharField(max_length = 140 ,blank=True)

	# Properties & setter
	@property
	def contactinfo_name(self):
	    return self._contactinfo_name
	@contactinfo_name.setter
	def contactinfo_name(self , name) :
		self._contactinfo_name = name
	@property
	def contactinfo_cellphone(self):
	    return self._contactinfo_cellphone
	@contactinfo_cellphone.setter
	def contactinfo_cellphone(self , phonenum) :
		self._contactinfo_cellphone = phonenum
	@property
	def contactinfo_birthdate(self):
	    return self._contactinfo_birthdate
	@contactinfo_birthdate.setter
	def contactinfo_birthdate(self , birthdate) :
		self._contactinfo_birthdate = birthdate
	@property
	def contactinfo_gender(self):
	    return self._contactinfo_gender
	@contactinfo_gender.setter
	def contactinfo_gender(self , gender):
		self._contactinfo_gender = gender
	@property
	def contactinfo_address(self):
	    return self._contactinfo_address
	@contactinfo_address.setter
	def contactinfo_address(self,  addr):
		self._contactinfo_address = addr
	@property
	def contactinfo_description(self):
	    return self._contactinfo_description
	@contactinfo_description.setter
	def contactinfo_description(self , description):
		self._contactinfo_description = description

	@classmethod
	def create(cls , account, name , phonenum  , birthdate,
		gender , address , description) :
		contact_info = cls(account = account , _contactinfo_name = name , _contactinfo_cellphone = phonenum , 
			_contactinfo_birthdate = birthdate , _contactinfo_gender = gender ,
			_contactinfo_address = address , _contactinfo_description = description)
		return contact_info

	# properties update
	def update_contact_info(self , name , phonenum ,  birthdate ,
		gender , address , description) :
		self._contactinfo_name = name
		self._contactinfo_cellphone = phonenum
		self._contactinfo_birthdate = birthdate
		self._contactinfo_gender = gender
		self._contactinfo_address = address
		self._contactinfo_description = description

	# Representations
	def __str__(self) :
		return 'Contact Info of:' + self._contactinfo_name + ' from account : ' + account.account_name
	__repr__ = __str__

# Experience info , many to one relation to user account
class Experience(models.Model) :
	'''
	Experience info for users...
	Many to one relationship to Account

	'''
	account = models.ForeignKey(
		Account,
		on_delete = models.CASCADE
	)

	_job_title = models.CharField(max_length=30 , default='Null')
	_description = models.TextField(default='Null')
	_start_date = models.DateField(blank=True)
	_end_date = models.DateField(blank=True)

	# Properties & setter
	@property
	def job_title(self):
	    return self._job_title
	@job_title.setter
	def job_title(self , title) :
		self._job_title = title
	@property
	def description(self):
	    return self._description
	@description.setter
	def description(self , description):
		self._description = description
	@property
	def start_date(self):
	    return self._start_date
	@start_date.setter
	def start_date(self , date):
		self._start_date = date
	@property
	def end_date(self):
	    return self._end_date
	@end_date.setter
	def end_date(self , date):
		self._end_date = date

	@classmethod
	def create(cls , account , job_title , description , start_date , end_date) :
		experience = cls(account = account , _job_title = job_title , _description = description,
			_start_date = start_date , _end_date = end_date)
		return experience

	# properties update
	def update_experience(job_title , description , start_date , end_date) :
		self._job_title = job_title
		self._description = description
		self._start_date = start_date
		self._end_date = end_date

	# Representations
	def __str__(self) :
		return 'Experience of :' + self._job_title + ' for account:' + account.account_name
	__repr__ = __str__
	
# Skills info , many to one relation to Account
class Skill(models.Model) :
	account = models.ForeignKey(
		Account,
		on_delete = models.CASCADE
	)

	_skill_type = models.CharField(max_length=30 , default='Null')
	_skill_proficiency = models.IntegerField(default=5)
	_skill_description = models.TextField(default='Null')

	# Properties & setter
	@property
	def skill_type(self):
	    return self._skill_type
	@skill_type.setter
	def skill_type(self , skill) :
		self._skill_type = skill
	@property
	def skill_proficiency(self):
	    return self._skill_proficiency
	@skill_proficiency.setter
	def skill_proficiency(self , proficiency) :
		self._skill_proficiency = proficiency
	@property
	def skill_description(self):
	    return self._skill_description
	@skill_description.setter
	def skill_description(self , description):
		self._skill_description = description

	@classmethod
	def create(cls , account , skill_type , skill_proficiency , skill_description):
		skill = cls(account = account_name , _skill_type = skill_type ,
			_skill_proficiency = skill_proficiency, _skill_description = skill_description)
		return skill

	# properties update
	def update_skill(skill_type , skill_proficiency , skill_description) :
		self._skill_type = skill_type
		self._skill_proficiency = skill_proficiency
		self._skill_description = skill_description

	# Representations
	def __str__(self) :
		return 'Skill:' + self._skill_type + ' of account :' + self.account.account_name
	__repr__ = __str__
