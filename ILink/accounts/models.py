from __future__ import unicode_literals
from datetime import datetime

from django.db import models

# Account for user login
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

	_contactinfo_name = models.CharField(max_length=30)
	_contactinfo_cellphone = models.CharField(max_length=20)
	_contactinfo_email = models.CharField(max_length=30)
	_contactinfo_birthdate = models.DateField()

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
	def contactinfo_email(self):
	    return self._contactinfo_email
	@contactinfo_email.setter
	def contactinfo_email(self , email) :
		self._contactinfo_email = email
	@property
	def contactinfo_birthdate(self):
	    return self._contactinfo_birthdate
	@contactinfo_birthdate.setter
	def contactinfo_birthdate(self , birthdate) :
		self._contactinfo_birthdate = birthdate

	@classmethod
	def create(cls , account, name , phonenum , email , birthdate) :
		contact_info = cls(account = account , _contactinfo_name = name , _contactinfo_cellphone = phonenum , 
			_contactinfo_email = email , _contactinfo_birthdate = birthdate)
		return contact_info

	# properties update
	def update_contact_info(name , phonenum , email , birthdate) :
		self._contactinfo_name = name
		self._contactinfo_cellphone = phonenum
		self._contactinfo_email = email
		self._contactinfo_birthdate = birthdate

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

	_job_title = models.CharField(max_length=30)
	_description = models.TextField()
	_start_date = models.DateField()
	_end_date = models.DateField()

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

	_skill_type = models.CharField(max_length=30)
	_skill_proficiency = models.IntegerField()
	_skill_description = models.TextField()

	# Properties & setter
	@property
	def skill_type(self):
	    return self._skill_type
	@skill_type.setter
	def skill_type(self , skill) :
		self._skill_type = skill
	@property
	def _skill_proficiency(self):
	    return self._skill_proficiency
	@_skill_proficiency.setter
	def _skill_proficiency(self , proficiency) :
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

# Projects info , many to one relation to Account
class Project(models.Model) :
	account = models.ForeignKey(
		Account,
		on_delete = models.CASCADE
	)

	_project_name = models.CharField(max_length=30)
	_project_description = models.TextField()
	_project_job_title = models.CharField(max_length=50)
	_project_contribution = models.FloatField()

	# Properties & setter
	@property
	def project_name(self):
	    return self._project_name
	@project_name.setter
	def project_name(self , name):
		self._project_name = name
	@property
	def project_description(self):
	    return self._project_description
	@project_description.setter
	def project_description(self , description):
		self._project_description = description
	@property
	def project_job_title(self):
	    return self._project_job_title
	@project_job_title.setter
	def project_job_title(self , job_title):
		self._project_job_title = job_title
	@property
	def project_contribution(self):
	    return self._project_contribution
	@project_contribution.setter
	def project_contribution(self , contribution):
		self._project_contribution = contribution

	@classmethod
	def cleate(cls , account , proj_name , proj_description , proj_job_title , proj_contribution):
		project = cls(account = account , _project_name = proj_name , _project_description = proj_description,
			_project_job_title = proj_job_title , _project_contribution = proj_contribution)
		return project

	# Representations
	def __str__(self):
		return 'Project:' + self._project_name + ' of account:' + self.account.account_name
	__repr__ = __str__
