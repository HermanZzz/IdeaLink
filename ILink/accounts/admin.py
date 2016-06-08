from django.contrib import admin

from django.forms import ModelForm, TextInput
from django.contrib.admin import ModelAdmin
from suit.widgets import HTML5Input
from suit.widgets import EnclosedInput
from suit.widgets import SuitDateWidget
from suit.admin import SortableModelAdmin


from .models import Account , Skill, Experience, ContactInfo



class AccountForm(ModelForm):
    class Meta:
        widgets = {
             '_account_name': HTML5Input(input_type='email'),
             
            '_account_passwd': EnclosedInput(prepend='icon-pencil', append=''),

 			'_account_register_date': EnclosedInput(prepend='icon-calendar', append=''),

 			'_account_register_date': SuitDateWidget,
            
        }

class ContactInline(admin.TabularInline):
    model = ContactInfo
    suit_classes = 'suit-tab suit-tab-contact'

class AccountAdmin(SortableModelAdmin):
    form = AccountForm
    sortable = 'order'
    list_display = ('_account_name', 'account_register_date') # list

    inlines = (ContactInline,)

    fieldsets = [
        ('Account Name', {
            'classes': ('suit-tab', 'suit-tab-general',),
            'fields': ['_account_name']
        }),
        ('Account Info', {
            'classes': ('suit-tab', 'suit-tab-general',),
            'fields': ['_account_passwd', '_account_register_date']}),
    ]

    suit_form_tabs = (('general', 'General'), ('contact', 'Contact'),
                )

    def suit_cell_attributes(self, obj, column):
        if column == '_account_name':
            return {'class': 'text-center'}
        


# Register your models here.
admin.site.register(Account,AccountAdmin)
admin.site.register(ContactInfo)
admin.site.register(Skill)
admin.site.register(Experience)