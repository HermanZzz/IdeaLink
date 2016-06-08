#-*- coding:utf-8 -*-

from django.shortcuts import render
from datetime import datetime
import hashlib
from datetime import timedelta
from accounts.models import Account
from django.http import HttpResponseRedirect, HttpResponseBadRequest, HttpResponse
from .models import Project, WechatQRCode

import sys
import os
reload(sys)
sys.setdefaultencoding('utf8')

from django.views.decorators.csrf import csrf_exempt
from wechat_sdk import WechatConf, WechatBasic
from wechat_sdk.exceptions import ParseError
from wechat_sdk.messages import ImageMessage, TextMessage

# Wechat configurations
conf = WechatConf(
	token = 'ILinkProjToken',
	appid = 'wx078801c8b39da1c2',
	appsecret = '579998602563a35b67d20ab6228e33b3',
	encrypt_mode = 'save',
	)


# Create your views here.
@csrf_exempt
def wechattest(request):

	signature = request.GET.get('signature')
	timestamp = request.GET.get('timestamp')
	nonce = request.GET.get('nonce')
	wechat_instance = WechatBasic(conf = conf)

	if not wechat_instance.check_signature(signature = signature, timestamp = timestamp, nonce = nonce) :
		return HttpResponseBadRequest('Verify Failed')
	else :
		if request.method == 'GET' :
			response = request.GET.get('echostr', 'err')
		else :
			try:
				wechat_instance.parse_data(request.body)
				message = wechat_instance.get_message()
				wechat_user_openid = wechat_instance.message.source

				# res = wechat_instance.create_qrcode({
				# 		    "expire_seconds": "QR_LIMIT_SCENE", 
				# 		    "action_name": "QR_SCENE", 
				# 		    "action_info": {
				# 		        "scene": {
				# 		            "scene_id": 123
				# 		        }
				# 		    }
				# 		})
				
				# response = wechat_instance.show_qrcode(res['ticket'])

				# with open('tmpfile', 'wb') as fd:
				#     for chunk in response.iter_content(1024):
				#         fd.write(chunk)
				

				if isinstance(message, ImageMessage) :
					try:
						link = WechatQRCode.objects.get(wechat_openid = wechat_user_openid)
						link.qrcode_url = message.picurl
						link.save()
						
						response = wechat_instance.download_media(message.media_id)
						# import pdb; pdb.set_trace()
						# filename = os.path.join(os.path.pardir,'/static/img/' + link.account.account_name + '.jpeg')

						with open('ILink/static/img/' + link.account.account_name + '.jpeg', 'wb') as fd :
							for chunk in response.iter_content(1024) :
								fd.write(chunk)


						reply_text = '二维码上传成功'

					except Exception, e:
						reply_text = '请先绑定帐号\n\n绑定ILink帐号，请使用 - 为分隔符输入帐号密码\n上传个人微信二维码，请直接发送图片'
					
				elif isinstance(message, TextMessage) :
					content = message.content

					if content.find("-") > -1 :
						# User varification
						account, passwd = content.split("-")

						# Encode account password
						md5 = hashlib.md5()
						md5.update(passwd.encode('utf-8'))
						passwd = md5.hexdigest()

						# Account validation
						try:
							account_for_validation = Account.objects.get(_account_name = account)
						except Exception, e:
							reply_text = '绑定ILink帐号，请使用 - 为分隔符输入帐号密码\n上传个人微信二维码，请直接发送图片'
							
						# import pdb; pdb.set_trace()
						if account_for_validation :
							if account_for_validation.account_passwd == passwd :
								try:
									link = WechatQRCode.objects.get(wechat_openid = wechat_user_openid)
									link.account = account_for_validation
									reply_text = '重新绑定ILink帐号成功'

								except Exception, e:
									newlink = WechatQRCode.create(account = account_for_validation, openid=wechat_user_openid)
									newlink.save()
									reply_text = '绑定ILink帐号成功'
								

							else :
								reply_text = '绑定ILink帐号验证失败'	


					else :
						reply_text = '绑定ILink帐号，请使用 - 为分隔符输入帐号密码\n上传个人微信二维码，请直接发送图片'

				else :
					reply_text = '绑定ILink帐号，请使用 - 为分隔符输入帐号密码\n上传个人微信二维码，请直接发送图片'

				response = wechat_instance.response_text(content = reply_text)
			except ParseError:
				return HttpResponseBadRequest('Invalid XML data.')
			
	return HttpResponse(response, content_type = 'application/xml')

@csrf_exempt
def wechatredirect(request):
	pass

def index(request) :
	return render(request , 'projects/myProjects.html')

def myProjects(request) :
	press_create = False
	create_project_succeed = False
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
		'press_create' : False,
		'create_project_succeed' : False,
		'target_projects' : account.project_set.all() | Project.objects.filter(project_members__id = account.id)
		})

def myApplications(request):
	# validate user session
	try:
		account = Account.objects.get(_account_name = request.session['account_name'])
	
	except Exception, e:
		return render(request , 'accounts/login.html' , {	
			'is_login_success' : False,
			'is_register_success' : False,
			'is_first_time_to_this_page' : False,
			})


	# import pdb; pdb.set_trace()
	result = Project.objects.filter(project_applicants__id = account.id)
	find_project_success = True
	return render(request , 'projects/findProject.html',{
		'is_login_success' : True,
		'find_project_success' : find_project_success,
		'user_session' : account,
		'results' : result
		})


def projectsByType(request, type):
	press_create = False
	create_project_succeed = False
	# validate user session
	try:
		account = Account.objects.get(_account_name = request.session['account_name'])
	except Exception, e:
		return render(request , 'accounts/login.html' , {	
			'is_login_success' : False,
			'is_register_success' : False,
			'is_first_time_to_this_page' : False,
			})

	if type == 'All' :
		target_projects = account.project_set.all() | Project.objects.filter(project_members__id = account.id)
	elif type == 'Own' :
		target_projects = account.project_set.all()
	elif type == 'Member' :
		target_projects = Project.objects.filter(project_members__id = account.id)	
	else :
		target_projects = account.project_set.all() | Project.objects.filter(project_members__id = account.id)

	return render(request , 'projects/myProjects.html',{
		'is_login_success' : True,
		'user_session' : account,
		'press_create' : False,
		'create_project_succeed' : False,
		'target_projects' : target_projects
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

def project_details(request , project_id):
	# validate user session
	try:
		account = Account.objects.get(_account_name = request.session['account_name'])
	except Exception, e:
		return render(request , 'accounts/login.html' , {
			'is_login_success' : False,
			'is_register_success' : False,
			'is_first_time_to_this_page' : False,
			})

	# Fetch project info
	import pdb; pdb.set_trace()
	current_project = Project.objects.get(id=project_id)
	pending_tasks = current_project.task_set.filter(task_status = 'Pending')
	underway_tasks = current_project.task_set.filter(task_status = 'Underway')
	finished_tasks = current_project.task_set.filter(task_status = 'Finished')
	


	return render(request , 'projects/projectDetail.html', {
		'is_login_success' : True,
		'user_session' : account,
		'current_project' : current_project,
		'pending_tasks' : pending_tasks,
		'underway_tasks' : underway_tasks,
		'finished_tasks' : finished_tasks,
		'appid' : conf.appid
		})

def create_task(request, project_id):
	# validate user session
	try:
		account = Account.objects.get(_account_name = request.session['account_name'])
	except Exception, e:
		return render(request , 'accounts/login.html' , {
			'is_login_success' : False,
			'is_register_success' : False,
			'is_first_time_to_this_page' : False,
			})
	# Fetch project info and create new task
	try:
		current_project = Project.objects.get(id=project_id)

		task_name = request.POST['task_name']
		task_description = request.POST['task_description']

		current_project.task_set.create(task_name = task_name, task_description= task_description, task_start_date = datetime.now(),
			task_expire_time = (datetime.now() + timedelta(days=30)), task_status = 'Pending')
	except Exception, e:
		return HttpResponseRedirect('/projects/projectDetail/' + project_id)
	return HttpResponseRedirect('/projects/projectDetail/' + project_id)

def delete_task(request, project_id, task_id):
	# validate user session
	try:
		account = Account.objects.get(_account_name = request.session['account_name'])
	except Exception, e:
		return render(request , 'accounts/login.html' , {
			'is_login_success' : False,
			'is_register_success' : False,
			'is_first_time_to_this_page' : False,
			})
	# Fetch project info and create new task
	try:
		
		current_project = Project.objects.get(id=project_id)
		current_task = current_project.task_set.filter(id=task_id)
		for task in current_task :
			task.delete()
	except Exception, e:
		return HttpResponseRedirect('/projects/projectDetail/' + project_id)
	return HttpResponseRedirect('/projects/projectDetail/' + project_id)
	
def projectQuickCreate(request):
	press_create = True
	create_project_succeed = False
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
		
		account.project_set.create(project_name = proj_name , project_description = proj_description , 
			project_owner = account,project_start_date = datetime.now().strftime('%Y-%m-%d'), project_expire_date = datetime.now().strftime('%Y-%m-%d'))

	except Exception, e:
		return HttpResponseRedirect('/projects/myProjects')
	else :
		proj = account.project_set.get(project_name = proj_name)
		return HttpResponseRedirect('/projects/projectDetail/' + str(proj.id))

def add_member(request, project_id):
	# validate user session
	try:
		account = Account.objects.get(_account_name = request.session['account_name'])
	except Exception, e:
		return render(request , 'accounts/login.html' , {
			'is_login_success' : False,
			'is_register_success' : False,
			'is_first_time_to_this_page' : False,
			})

	# Fetch project info
	try:
		current_project = account.project_set.get(id=project_id)
		member = Account.objects.get(_account_name = request.POST['member_name'])
		current_project.project_members.add(member)
	except Exception, e:
		return HttpResponseRedirect('/projects/projectDetail/' + project_id)
	return HttpResponseRedirect('/projects/projectDetail/' + project_id)

def delete_member(request, project_id, member_id):
	# validate user session
	try:
		account = Account.objects.get(_account_name = request.session['account_name'])
	except Exception, e:
		return render(request , 'accounts/login.html' , {
			'is_login_success' : False,
			'is_register_success' : False,
			'is_first_time_to_this_page' : False,
			})

	# Fetch project info
	try:
		current_project = account.project_set.get(id=project_id)
		member = Account.objects.get(id=member_id)

		current_project.project_members.remove(member)
	except Exception, e:
		return HttpResponseRedirect('/projects/projectDetail/' + project_id)
	return HttpResponseRedirect('/projects/projectDetail/' + project_id)

def findProject(request):
	find_project_success=False
	# validate user session
	try:
		account = Account.objects.get(_account_name = request.session['account_name'])
	except Exception, e:
		return render(request , 'accounts/login.html' , {
			'is_login_success' : False,
			'is_register_success' : False,
			'is_first_time_to_this_page' : False,
			})

	# Fetch user input
	try:
		# import pdb; pdb.set_trace()
		search_key = request.POST['search_key']

		# import pdb; pdb.set_trace()
		result_by_name = Project.objects.filter(project_name__contains = search_key)
		result = result_by_name.filter(project_status = 'Open')
		if result :
			find_project_success=True
		# result_by_tag =
	except Exception, e:
		return HttpResponseRedirect('/projects/projectsByType/1')

	return render(request , 'projects/findProject.html',{
		'is_login_success' : True,
		'find_project_success' : find_project_success,
		'user_session' : account,
		'results' : result
		})

def applyProject(request, project_id):
	# validate user session
	try:
		account = Account.objects.get(_account_name = request.session['account_name'])
	except Exception, e:
		return render(request , 'accounts/login.html' , {
			'is_login_success' : False,
			'is_register_success' : False,
			'is_first_time_to_this_page' : False,
			})
	# Fetch project info
	try:
		
		new_name = request.POST['proj_name']
		expire_time = request.POST['deadline']
		option = request.POST['option']
		if option == 'option_1' :
			status = 'Open'
		elif option == 'option_2':
			status = 'Undergoing'
		elif option == 'option_3' :
			status = 'Closed'
		else :
			status = 'Open'

		description = request.POST['description']

		current_project = Project.objects.get(id=project_id)

		# Update
		current_project.update_project(new_name,description,expire_time,status)
		
		# import pdb; pdb.set_trace()
		current_project.save()

	except Exception, e:
		return HttpResponseRedirect('/projects/projectDetail/' + project_id)
	return HttpResponseRedirect('/projects/projectDetail/' + project_id)

def reviewProject(request, project_id):
	# validate user session
	try:
		account = Account.objects.get(_account_name = request.session['account_name'])
	except Exception, e:
		return render(request , 'accounts/login.html' , {
			'is_login_success' : False,
			'is_register_success' : False,
			'is_first_time_to_this_page' : False,
			})

	# Fetch project info
	current_project = Project.objects.get(id=project_id)

	return render(request , 'projects/applyProject.html', {
		'is_login_success' : True,
		'user_session' : account,
		'current_project' : current_project,
		})	

def change_task(request, project_id, task_id):
	# validate user session
	try:
		account = Account.objects.get(_account_name = request.session['account_name'])
	except Exception, e:
		return render(request , 'accounts/login.html' , {
			'is_login_success' : False,
			'is_register_success' : False,
			'is_first_time_to_this_page' : False,
			})
	# Fetch project info and create new task
	try:
		current_project = Project.objects.get(id=project_id)
		current_task = current_project.task_set.get(id=task_id)
		
		if current_task.task_status == 'Pending':
			current_task.change_status('Underway')
		elif current_task.task_status == 'Underway':
			current_task.change_status('Finished')

		current_task.save()

	except Exception, e:
		return HttpResponseRedirect('/projects/projectDetail/' + project_id)
	return HttpResponseRedirect('/projects/projectDetail/' + project_id)

def applyForProject(request, project_id):
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
		project_for_apply = Project.objects.get(id=project_id)

		# import pdb; pdb.set_trace()
		project_for_apply.project_applicants.add(account)
		project_for_apply.save()

	except Exception, e:
		return HttpResponseRedirect('/projects/projectsByType/3')
	
	return HttpResponseRedirect('/projects/projectsByType/1')

def addApplicant(request, project_id, member_id):
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
		# import pdb; pdb.set_trace()
		project_for_add = Project.objects.get(id=project_id)
		member_for_add = Account.objects.get(id=member_id)
		project_for_add.project_members.add(member_for_add)
		project_for_add.project_applicants.remove(member_for_add)

	except Exception, e:
		return HttpResponseRedirect('/projects/projectDetail/' + project_id)
	return HttpResponseRedirect('/projects/projectDetail/' + project_id)
	

def deleteApplicant(request, project_id, member_id):
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
		project_for_delete = Project.objects.get(id=project_id)
		member_for_delete = Account.objects.get(id=member_id)
		project_for_delete.project_applicants.remove(member_for_delete)

	except Exception, e:
		return HttpResponseRedirect('/projects/projectDetail/' + project_id)
	return HttpResponseRedirect('/projects/projectDetail/' + project_id)
