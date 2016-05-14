from django.shortcuts import render

# Create your views here.
def index(request) :
	return render(request , 'projects/myProjects.html')

def myProjects(request) :
	return render(request , 'projects/myProjects.html')	

def projectDetail(request) :
	return render(request , 'projects/projectDetail.html')	