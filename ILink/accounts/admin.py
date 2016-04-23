from django.contrib import admin

from .models import Account , Skill, Experience

# Register your models here.
admin.site.register(Account)
admin.site.register(Skill)
admin.site.register(Experience)
