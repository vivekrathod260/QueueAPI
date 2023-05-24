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
    return JsonResponse({'status': 'you got correct server for line'})

@csrf_exempt
def login(request):
    if request.method == 'POST':
        try:
            userName = json.loads(request.body).get('userName')
            password = json.loads(request.body).get('password')
            # userName = request.POST.get('userName')
            # password = request.POST.get('password')
        except:
            return JsonResponse({'status': 'no data in post req'})

        queryObj = USER.objects.filter(username=userName, password=password)
        print(userName)
        print(password)

        if(queryObj.exists() == True):  
            payload = {
                'userName': userName
            }
            token = jwt.encode(payload, 'vivekkey', algorithm='HS256')
            print("token sent "+token)
            return JsonResponse({'status':"ok",'token': token})
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
            creatorid = json.loads(request.body).get("creatorID")
            queuename = json.loads(request.body).get("queueName")
        except:
            return JsonResponse({'status': 'no data in post req'})
        
        status = auth(request)
        if(status == -1):
            return JsonResponse({'status': 'Invalid Authorization header'})
        elif(status == 0):
            return JsonResponse({'status': 'Invalid JWT token'})
        else:
            USER.objects.filter(username=status)[0].joinQueue(creatorID1=creatorid,queueName1=queuename)
            print(creatorid+" "+queuename)
            return JsonResponse({'status': 'joined !'})

@csrf_exempt
def exitqueue(request):
    if request.method == 'POST':
        try:
            creatorid = json.loads(request.body).get('creatorID')
            queuename = json.loads(request.body).get('queueName')
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
    print(status)
    if(status == -1):
        return JsonResponse({'status': 'Invalid Authorization header'})
    elif(status == 0):
        return JsonResponse({'status': 'Invalid JWT token'})
    else:
        me = USER.objects.filter(username=status)[0]
        joinedQueuesList = me.getJoinedQueues()
        return JsonResponse({'status': "ok", 'lst':joinedQueuesList})

@csrf_exempt
def createqueue(request):
    if request.method == 'POST':
        try:
            queueName = json.loads(request.body).get('queueName')
            location = json.loads(request.body).get('location')
            time = json.loads(request.body).get('time')
            note = json.loads(request.body).get('note')
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
        return JsonResponse({'status': 'ok', 'lst':myQueueList})

@csrf_exempt
def deletequeue(request):
    if request.method == 'POST':
        try:
            queuename = json.loads(request.body).get('queueName')
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
                    return JsonResponse({'status': 'cannot delete Queue'})
                elif res ==-1:
                    return JsonResponse({'status': 'can not delete queue as queue you specified does not exist'})
                elif res ==-2:
                    return JsonResponse({'status': 'cannot delete as queue does not exitst'})
                else:
                    return JsonResponse({'status': 'queue deleted !'})
            else:
                return JsonResponse({'status': 'user doesnt exist'})

@csrf_exempt
def customerpanel(request):
    if request.method == 'POST':
        try:
            creatorid = json.loads(request.body).get('creatorID')
            queuename = json.loads(request.body).get('queueName')
            if(creatorid==None or queuename==None):
                JsonResponse({'status': 'no data in post req'})
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
                print(data)
                return JsonResponse({'status': "ok", 'data':data})
            else:
                return JsonResponse({'status': "queue you specified does not exist"}) 

@csrf_exempt
def adminpanel(request):
    if request.method == 'POST':
        try:
            queuename = json.loads(request.body).get('queueName')
            
            if(queuename==None):
                JsonResponse({'status': 'no data in post req'})
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
                    "speed":str(float(q.getSpeed())/60.0)+" min/person",
                    "estTimeToEmpty": str(float(q.len())*float(q.getSpeed())/float(60))
                }
                return JsonResponse({'status': "ok", 'data':data})
            else:
                return JsonResponse({'status': "queue you specified does not exist"})

@csrf_exempt
def pop(request):
    if request.method == 'POST':
        try:
            queuename = json.loads(request.body).get('queueName')
            
            if(queuename==None):
                JsonResponse({'status': 'no data in post req'})
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
                return JsonResponse({'status': "work done"})
            else:
                return JsonResponse({'status': 'user doesnt exist'})

@csrf_exempt
def deletepersonfromqueue(request):
    if request.method == 'POST':
        try:
            queuename = json.loads(request.body).get('queueName')
            userid = json.loads(request.body).get("userID")
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