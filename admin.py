from django.contrib import admin
from models import *

class GovtAdmin(admin.ModelAdmin):
    search_fields = ['name',]
	
class SalaryAdmin(admin.ModelAdmin):
    search_fields = ['fullname',]
    list_display = ('fullname', 'dept', 'salary', 'total_gross', 'govt',)
    list_filter = ('govt',)

admin.site.register(Govt, GovtAdmin)
admin.site.register(Salary, SalaryAdmin)
