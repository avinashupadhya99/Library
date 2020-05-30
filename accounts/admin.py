from django.contrib import admin
from.models import UserProfile, OTP
from django.shortcuts import redirect
from django.http import HttpResponse

admin.site.site_header = 'Library Admin'

admin.site.index_template = "admin/my_index.html"

class OTPAdmin(admin.ModelAdmin):
    list_display = ('regno','otp')
    list_filter = ('regno',)



admin.site.register(UserProfile)
admin.site.register(OTP, OTPAdmin)