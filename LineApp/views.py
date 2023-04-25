from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt

# from django.contrib.auth import authenticate, login as auth_login, logout
# from django.contrib.auth.models import User

from LineApp.models import USER, Queue

import jwt
from LineApp.utils.auth import auth
########################################################################

#########################################################################

def home(request):
    return HttpResponse("<h1>Working</h1>")

@csrf_exempt
def login(request):
    if request.method == 'POST':
        userName = request.POST.get('userName')
        password = request.POST.get('password')
        print(userName)
        print(password)

        queryObj = USER.objects.filter(username=userName, password=password)

        if(queryObj.exists() == True):  
            payload = {
                'userName': userName
            }
            token = jwt.encode(payload, 'vivekkey', algorithm='HS256')
            print("token sent "+token)
            return JsonResponse({'token': token})
        else:
            return JsonResponse({'status': 'Invalid credentials'})
    return JsonResponse({'status': 'check your method'})

@csrf_exempt
def register(request):
    if request.method == "POST":
        try:
            userName = request.POST.get("userName")
            password = request.POST.get("password")          
        except:
            print("Username and pass not found")
            return JsonResponse({'status': 'Username and pass not found'})

        if USER.objects.filter(username=userName).exists() == True:
            return JsonResponse({'status': 'User exist'})
        else:
            newUSER = USER.objects.create(username=userName,password=password,data="[]")
            newUSER.save()
            return JsonResponse({'status': 'User created'})
    else:
        return JsonResponse({'status': 'check your method'})


def protected(request):
    status = auth(request)
    if(status == -1):
        return JsonResponse({'status': 'Invalid Authorization header'})
    elif(status == 0):
        return JsonResponse({'status': 'Invalid JWT token'})
    else:
        return JsonResponse({'status': "Authenticated !! your username is "+status})