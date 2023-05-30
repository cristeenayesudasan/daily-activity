from django.contrib import admin
from django.db import models
from dailyapp.models import designation,department,employee_details,login,admin_login,enquiry
from dailyapp.models import appointment_detail,domestic_cust_add,business_cust_add,task_create,task_assigning,notes

# Register your models here.
class postlogin(admin.ModelAdmin):
    pass

class postadmin_login(admin.ModelAdmin):
    pass
class postdepartment(admin.ModelAdmin):
    pass

class postdesignation(admin.ModelAdmin):
    pass

class postemployee_details(admin.ModelAdmin):
    pass


class postenquiry(admin.ModelAdmin):
    pass

class postappointment_detail(admin.ModelAdmin):
    pass

class postdomestic_cust_add(admin.ModelAdmin):
    pass

class postbusiness_cust_add(admin.ModelAdmin):
    pass

class posttask_create(admin.ModelAdmin):
    pass


class posttask_assigning(admin.ModelAdmin):
    pass


class postnotes(admin.ModelAdmin):
    pass

# class postdaily_activity(admin.ModelAdmin):
#     pass


admin.site.register(login,postlogin)
admin.site.register(admin_login,postadmin_login)
admin.site.register(department,postdepartment)
admin.site.register(designation,postdesignation)
admin.site.register(employee_details,postemployee_details)
admin.site.register(enquiry,postenquiry)
admin.site.register(appointment_detail,postappointment_detail)
admin.site.register(domestic_cust_add,postdomestic_cust_add)
admin.site.register(business_cust_add,postbusiness_cust_add)
admin.site.register(task_create,posttask_create)
admin.site.register(task_assigning,posttask_assigning)
admin.site.register(notes,postnotes)
# admin.site.register(daily_activity,postdaily_activity)
