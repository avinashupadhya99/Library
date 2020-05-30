from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from .models import UserProfile, OTP
import re
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required



def register(request):
    if request.method == 'POST':
        
        fullname = request.POST['fullname']
        regnumber = request.POST['regno']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        phnumber = request.POST['phnumber']
        otp = request.POST['otp']
        branch = request.POST['branch']
        sem = request.POST['semester']
        if re.match('\d\d[A-Z][A-Z][A-Z][A-Z]\d\d\d\d',regnumber):
            if password1==password2:
                if User.objects.filter(username=regnumber).exists():    
                    messages.error(request, 'Account exists with that register number')
                    return redirect('/accounts/register/')
                elif User.objects.filter(email=email).exists():
                    messages.error(request, 'An account exists with that email ID')
                    return redirect('/accounts/register/')
                elif UserProfile.objects.filter(phoneNumber=phnumber):
                    messages.error(request, 'An account exists with that phone number')
                    return redirect('/accounts/register/')
                else:
                    try:
                        otp_obj = OTP.objects.get(regno=regnumber)
                        try:
                            otp_obj = OTP.objects.get(regno=regnumber,otp=otp)
                            user = User.objects.create_user(username=regnumber, password=password1, email=email, first_name=fullname)
                            user.save()
                            user_profile = UserProfile.objects.create(user=user)
                            user_profile.phoneNumber = phnumber
                            user_profile.branch = branch
                            user_profile.semester = sem
                            user_profile.save()
                            return redirect('/accounts/login/')
                        except ObjectDoesNotExist:
                            messages.error(request, 'The unique number is incorrect')
                            return redirect('/accounts/register/')
                    except ObjectDoesNotExist:
                        messages.error(request, 'Register number does not exists. Please contact librarian')
                        return redirect('/accounts/register/')
            else:
                messages.error(request, 'Passwords do not match')
                return redirect('/accounts/register/')
        else:
            messages.error(request, 'Register number does not match format')
            return redirect('/accounts/register/')
    else:
        return render(request,'register.html')
        

def login(request):
    if request.method == 'POST':
        regnumber = request.POST['regNo']
        password = request.POST['password']

        user = auth.authenticate(username=regnumber,password=password)

        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            return redirect('/accounts/login/')
    else:
        return render(request,'login.html')

def logout(request):
    auth.logout(request)
    return redirect('/accounts/login/')

@staff_member_required
def getOTP(request):
    regNumber = request.GET.get('regNoSearch')
    context = {
        'regNo' : None,
        'otP' : None
    }
    print(regNumber)
    if regNumber:
        try:
            otp = OTP.objects.get(regno=regNumber)
            context = {
                'regNo' : regNumber,
                'otP': otp
            }
        except ObjectDoesNotExist:
            messages.error(request, 'No OTP for the user, add OTP in the database')
            return redirect('/accounts/getOTP/')

    return render(request,'admin/getotp.html',context)

@login_required
def dashboard(request):
    p = UserProfile.objects.get(user_id=request.user.id)
    context = {'FirstName':request.user.first_name,
            'UserName':request.user.username,
            'EmailID' :request.user.email,
            'PhoneNo' :p.phoneNumber,
            'Semester' :p.semester,
            'Branch': p.branch,
    }
    return render(request,'dashboard.html',context)

@login_required
def edit_email(request):
    if request.method == 'POST':
        email = request.POST['newemail']
        user_id = request.user.id
        user1 = User.objects.get(id=user_id)
        user1.email = email
        user1.save()
        messages.success(request, 'Email ID updated')
        return redirect('/accounts/dashboard/')
    else:
        return redirect('/accounts/dashboard/')

@login_required
def edit_phone(request):
    if request.method == 'POST':
        phone = request.POST['newphone']
        user_id = request.user.id
        user2 = UserProfile.objects.get(user_id=user_id)
        user2.phoneNumber = phone
        user2.save()
        messages.success(request, 'Phone Number updated')
        return redirect('/accounts/dashboard/')
    else:
        return redirect('/accounts/dashboard/')

@login_required
def change_password(request):
    if request.method == 'POST':
        oldpass = request.POST['currentPassword']
        current_user = request.user
        if current_user.check_password(oldpass):
            nPassword = request.POST['newPassword']
            nPassword1 = request.POST['newPassword1']
            if nPassword == nPassword1:
                if nPassword == oldpass:
                    messages.error(request, 'New password cannot be same as old password')
                    return redirect('/accounts/dashboard/')
                else:
                    current_user.set_password(nPassword)
                    current_user.save()
                    regnumber = current_user.username
                    user = auth.authenticate(username=regnumber,password=nPassword)
                    auth.login(request,user)
                    messages.success(request, 'Password changed sucessfully!')
                    return redirect('/accounts/dashboard/')
            else:
                messages.error(request, 'Password dont match')
                return redirect('/accounts/dashboard/')
        else:
            messages.error(request, 'Please check the current password')
            return redirect('/accounts/dashboard/')
        return redirect('/accounts/dashboard/')
    else:
        return redirect('/accounts/dashboard/')

def forgot_password(request):
    return render(request,'forgot_password.html')

def addreg(request):
    if 'regNo1' in request.GET and 'regNo2' in request.GET:
        reg1 = request.GET.get('regNo1')
        reg2 = request.GET.get('regNo2')
        if re.match('\d\d[A-Z][A-Z][A-Z][A-Z]\d\d\d\d',reg1) and re.match('\d\d[A-Z][A-Z][A-Z][A-Z]\d\d\d\d',reg2):
            pass
        else:
            messages.error(request, 'Register numbers dont match format')
            return redirect('/accounts/generateOTP/')
    elif 'reg0' in request.GET:
        reg0 = request.GET.get('regNo0')
        if re.match('\d\d[A-Z][A-Z][A-Z][A-Z]\d\d\d\d',reg0):
            try:
                otp = OTP.objects.get(regno=reg0)
            except ObjectDoesNotExist:
                messages.error(request, 'OTP already exists for the register number')

            

        else:
            messages.error(request, 'Register number doesnt match format')
            return redirect('/accounts/generateOTP/')
    else:
        pass


    return render(request,'admin/generateOTP.html')