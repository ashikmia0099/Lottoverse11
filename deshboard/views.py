from django.shortcuts import render
from django.contrib.auth.models import User

def Myprofile(request):
    data = User.objects.filter(username = request.user.username)
    
    return render(request,'Deshboard/myprofile.html'  , {'data': data})



