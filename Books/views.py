from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

@login_required
def index(request):
    return render(request,'index.html',{'UserName':request.user.first_name})
    