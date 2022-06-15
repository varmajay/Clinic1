from django.contrib import admin

from .models import *

# Register your models here.


# admin.site.register(User)
@admin.register(User)
class AdminUser(admin.ModelAdmin):
    list_display=['id','name','email','roles','gender','address']

@admin.register(Doctor_availability)
class AdminDoctor_availability(admin.ModelAdmin):
    list_display=['id','week','start_time','end_time']
    # def doc_name(self, obj):
    #     return obj.doctor_id.name

@admin.register(Appoinment)
class AdminAppoinment(admin.ModelAdmin):
    list_display =['id','date','start_time','end_time','date','description','status']
    # def doc_name(self, obj):
    #     return obj.slot.doctor_id.name