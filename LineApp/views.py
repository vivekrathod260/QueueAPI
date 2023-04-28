from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt

# from django.contrib.auth import authenticate, login as auth_login, logout
# from django.contrib.auth.models import User

from LineApp.models import USER, Queue

import jwt
import json
from LineApp.utils.auth import auth
########################################################################

#########################################################################

def home(request):
    return HttpResponse("<h1>Working</h1>")

@csrf_exempt
def login(request):
    if request.method == 'POST':
        try:
            userName = request.POST.get('userName')
            password = request.POST.get('password')
        except:
            return JsonResponse({'status': 'no data in post req'})

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

@csrf_exempt
def protected(request):
    status = auth(request)
    if(status == -1):
        return JsonResponse({'status': 'Invalid Authorization header'})
    elif(status == 0):
        return JsonResponse({'status': 'Invalid JWT token'})
    else:
        return JsonResponse({'status': "Authenticated !! your username is "+status})

@csrf_exempt
def joinqueue(request):
    if request.method == 'POST':
        try:
            creatorid = request.POST.get('creatorID')
            queuename = request.POST.get('queueName')
        except:
            return JsonResponse({'status': 'no data in post req'})
        
        status = auth(request)
        if(status == -1):
            return JsonResponse({'status': 'Invalid Authorization header'})
        elif(status == 0):
            return JsonResponse({'status': 'Invalid JWT token'})
        else:
            USER.objects.filter(username=status)[0].joinQueue(creatorid,queuename)
            return JsonResponse({'status': 'joined !'})

@csrf_exempt
def exitqueue(request):
    if request.method == 'POST':
        try:
            creatorid = request.POST.get('creatorID')
            queuename = request.POST.get('queueName')
        except:
            return JsonResponse({'status': 'no data in post req'})
        
        status = auth(request)
        if(status == -1):
            return JsonResponse({'status': 'Invalid Authorization header'})
        elif(status == 0):
            return JsonResponse({'status': 'Invalid JWT token'})
        else:
            try:
                USER.objects.filter(username=status)[0].exitQueue(creatorid, queuename)
                return JsonResponse({'status': 'exited from queue !'})
            except:
                return JsonResponse({'status': 'unable to exit queue'})

@csrf_exempt
def myjoinedqueue(request):
    status = auth(request)
    if(status == -1):
        return JsonResponse({'status': 'Invalid Authorization header'})
    elif(status == 0):
        return JsonResponse({'status': 'Invalid JWT token'})
    else:
        me = USER.objects.filter(username=status)[0]
        joinedQueuesList = me.getJoinedQueues()
        return JsonResponse({'status': joinedQueuesList})

@csrf_exempt
def createqueue(request):
    if request.method == 'POST':
        try:
            queueName = request.POST.get('queueName')
            location = request.POST.get('location')
            time = request.POST.get('time')
            note = request.POST.get('note')
        except:
            return JsonResponse({'status': 'no data in post req'})

        status = auth(request)
        if(status == -1):
            return JsonResponse({'status': 'Invalid Authorization header'})
        elif(status == 0):
            return JsonResponse({'status': 'Invalid JWT token'})
        else:
            USER.objects.filter(username=status)[0].createQueue(queueName, location, time, note)
            return JsonResponse({'status': 'created !'})

@csrf_exempt
def myqueue(request):
    status = auth(request)
    if(status == -1):
        return JsonResponse({'status': 'Invalid Authorization header'})
    elif(status == 0):
        return JsonResponse({'status': 'Invalid JWT token'})
    else:
        me = USER.objects.filter(username=status)[0]
        myQueueList = me.getMyQueues()
        return JsonResponse({'status': myQueueList})

@csrf_exempt
def deletequeue(request):
    if request.method == 'POST':
        try:
            queuename = request.POST.get('queueName')
        except:
            return JsonResponse({'status': 'no data in post req'})
        
        status = auth(request)
        if(status == -1):
            return JsonResponse({'status': 'Invalid Authorization header'})
        elif(status == 0):
            return JsonResponse({'status': 'Invalid JWT token'})
        else:
            if(USER.objects.filter(username=status).exists()== True):

                res = USER.objects.filter(username=status)[0].deleteQueue(queuename)
                if res==0:
                    return JsonResponse({'cannot delete Queue'})
                elif res ==-1:
                    return JsonResponse({'can not delete queue as queue you specified does not exist'})
                elif res ==-2:
                    return JsonResponse({'cannot delete as queue does not exitst'})
                else:
                    return JsonResponse({'status': 'queue deleted !'})
            else:
                return JsonResponse({'status': 'user doesnt exist'})

@csrf_exempt
def customerpanel(request):
    if request.method == 'POST':
        try:
            creatorid = request.POST.get('creatorID')
            queuename = request.POST.get('queueName')
        except:
            return JsonResponse({'status': 'no data in post req'})
        
        status = auth(request)
        if(status == -1):
            return JsonResponse({'status': 'Invalid Authorization header'})
        elif(status == 0):
            return JsonResponse({'status': 'Invalid JWT token'})
        else:
            if(Queue.objects.filter(queueName=queuename, creatorID=creatorid).exists() == True):
                q = Queue.objects.filter(queueName=queuename, creatorID=creatorid)[0]
                index = q.indexof(status)

                if(index==0):
                    return JsonResponse({'status': "you cannot access as you are not in this queue"})
                
                speed = q.getSpeed()
                data = {
                    "length":q.len(),
                    "first":q.first(),
                    "myIndx":index,
                    "speed":str(float(speed)/60.0)+" min/person",
                    "estTime": str(((float(index)-1.0)*float(speed))/60.0)+" min"
                }
                return JsonResponse({'status': data})
            else:
                return JsonResponse({'status': "queue you specified does not exist"}) 

@csrf_exempt
def adminpanel(request):
    if request.method == 'POST':
        try:
            queuename = request.POST.get('queueName')
        except:
            return JsonResponse({'status': 'no data in post req'})
        
        status = auth(request)
        if(status == -1):
            return JsonResponse({'status': 'Invalid Authorization header'})
        elif(status == 0):
            return JsonResponse({'status': 'Invalid JWT token'})
        else:
            if(Queue.objects.filter(queueName=queuename, creatorID=status).exists() == True):
                q = Queue.objects.filter(queueName=queuename, creatorID=status)[0]

                if q.first()==0:
                    first = "Empty Queue"
                else:
                    first = q.first()
                
                data = {
                    "length":q.len(),
                    "first":first,
                    "speed":str(float(q.getSpeed())/60.0)+" min/person"
                }
                return JsonResponse({'status': data})
            else:
                return JsonResponse({'status': "queue you specified does not exist"})

@csrf_exempt
def pop(request):
    if request.method == 'POST':
        try:
            queuename = request.POST.get('queueName')
        except:
            return JsonResponse({'status': 'no data in post req'})
        
        status = auth(request)
        if(status == -1):
            return JsonResponse({'status': 'Invalid Authorization header'})
        elif(status == 0):
            return JsonResponse({'status': 'Invalid JWT token'})
        else:
            if(USER.objects.filter(username=status).exists() == True):
                u = USER.objects.filter(username=status)[0]
                poppedPerson = u.pop(queuename)
                return JsonResponse({'status': poppedPerson+" work done"})
            else:
                return JsonResponse({'status': 'user doesnt exist'})

@csrf_exempt
def deletepersonfromqueue(request):
    if request.method == 'POST':
        try:
            queuename = request.POST.get('queueName')
            userid = request.POST.get("userID")
        except:
            return JsonResponse({'status': 'no data in post req'})
        
        status = auth(request)
        if(status == -1):
            return JsonResponse({'status': 'Invalid Authorization header'})
        elif(status == 0):
            return JsonResponse({'status': 'Invalid JWT token'})
        else:
            if(USER.objects.filter(username=status).exists() == True):
                u = USER.objects.filter(username=status)[0]
                deletededPerson = u.deletePersonFromQueue(queuename, userid)
                return JsonResponse({'status': deletededPerson+" deleted from queue"})
            else:
                return JsonResponse({'status': 'user doesnt exist'})