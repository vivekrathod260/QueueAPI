from django.db import models

# Create your models here.
import json
from datetime import datetime

from django.contrib.auth.models import User
 
class USER(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    data = models.TextField(default='[]')

    def __str__(self):
        return self.username

class Queue(models.Model):
    queueName = models.CharField(max_length=20)
    creatorID = models.CharField(max_length=20)
    location = models.CharField(max_length=60)
    time = models.CharField(max_length=25)
    note = models.CharField(max_length=100)
    array = models.TextField(default='[]')
    speedData = models.CharField(max_length=50, default="3000#2023-04-25 23:13:33")

    def __str__(self):
        return self.queueName+"@"+self.creatorID

    def pop(self):
        if(self.array!="[]"):
            lst = json.loads(self.array)
            firstPerson = lst.pop(0)
            self.array = json.dumps(lst)
            ####
            speedData1 = self.speedData

            past_time_string = speedData.split("#")[1]
            stored_instance = datetime.strptime(past_time_string, '%Y-%m-%d %H:%M:%S')

            now_instance = datetime.now()
            now_time_string = now_instance.strftime('%Y-%m-%d %H:%M:%S')

            time_difference_seconds = (now_instance - stored_instance).total_seconds()

            self.speed = time_difference_seconds+"#"+now_time_string
            ####
            self.save()
            return firstPerson
        else:
            return None

    def push(self,userID):
        lst = json.loads(self.array)
        lst.append(userID)
        self.array = json.dumps(lst)
        self.save()
    
    def first(self):
        if(self.array!="[]"):
            lst = json.loads(self.array)
            firstPerson = lst[0]
            return firstPerson
        else:
            return None

    def len(self):
        return len(json.loads(self.array))

    def indexof(self,userID):
        if(self.array!="[]"):
            try:
                lst = json.loads(self.array)
                index = lst.index(userID)
                return index+1
            except:
                print("unable to get index of "+userID)
        else:
            return None

    def getSpeed(self):
        speedData1 = self.speedData
        return speedData1.split("#")[0]
