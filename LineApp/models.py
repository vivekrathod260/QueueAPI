from django.db import models
# Create your models here.
import json
from datetime import datetime
 
class USER(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    joinedQueue = models.TextField(default='[]')
    myQueue = models.TextField(default='[]')
    data = models.TextField(default='[]')

    def __str__(self):
        return self.username
    
    def getMyQueues(self):
        try:
            lst = json.loads(self.myQueue)
            return lst
        except:
            print("cannot load myQueue")

    def getJoinedQueues(self):
        try:
            lst = json.loads(self.joinedQueue)
            return lst
        except:
            print("cannot load joinedQueue")

    def joinQueue(self,creatorID1,queueName1):
        try:
            lst = json.loads(self.joinedQueue)
            if(str(creatorID1)+"#"+str(queueName1) not in lst):
                lst.append((str(creatorID1)+"#"+str(queueName1)))

                if(Queue.objects.filter(queueName =queueName1,creatorID = creatorID1).exists()== False):
                    print("queue doesn't exists")
                else:            
                    self.joinedQueue = json.dumps(lst)
                    self.save()
                    queryObj = Queue.objects.filter(queueName =queueName1,creatorID = creatorID1)
                    queue = queryObj[0]
                    queue.push(self.username)
            else:
                print("already joined queue")
        except:
            print("cannot join queue")

    def exitQueue(self,creatorID1,queueName1):
        try:
            lst = json.loads(self.joinedQueue)
            if(str(creatorID1)+"#"+str(queueName1) in lst):
                lst.remove(str(creatorID1)+"#"+str(queueName1))
                if(Queue.objects.filter(queueName =queueName1,creatorID = creatorID1).exists()== True):
                    self.joinedQueue = json.dumps(lst)
                    self.save()
                    q = Queue.objects.filter(queueName =queueName1,creatorID = creatorID1)[0]
                    q.removeByID(str(self.username))
                else:
                    print("queue does not exitst")
            else:
                print("cannto exit from queue as queue you specified does not exist")
        except:
            print("cannot exit from Queue")

    def createQueue(self,queueName,location,time,note):
        try:
            lst = json.loads(self.myQueue)
            if(str(self.username)+"#"+str(queueName) not in lst):
                lst.append((str(self.username)+"#"+str(queueName)))

                # creating new queue
                newQueue = Queue.objects.create(queueName=queueName,creatorID=self.username,location=location,time=time,note=note)

                self.myQueue = json.dumps(lst)
                self.save()
                newQueue.save()
            else:
                print("queue name already exists")
        except:
            print("cannot create queue")

    def deleteQueue(self,queueName1):
        try:
            lst = json.loads(self.myQueue)
            temp = str(self.username)+"#"+str(queueName1)

            if(temp in lst):
                lst.remove(temp)

                if(Queue.objects.filter(queueName =queueName1,creatorID = self.username).exists()== True):
                    q = Queue.objects.filter(queueName =queueName1,creatorID = self.username)[0]

                    #### removing all customers from list ########
                    customersList = json.loads(q.array)
                    for customerID in customersList:
                        thisUser = USER.objects.filter(username=customerID)[0]
                        joinedList = json.loads(thisUser.joinedQueue)
                        if temp in joinedList:
                            joinedList.remove(temp)
                            thisUser.joinedQueue = json.dumps(joinedList)
                            thisUser.save()
                    ##############################################
                    q.delete()
                    self.myQueue = json.dumps(lst)
                    self.save()
                    return 1
                else:
                    print("cannot delete as queue does not exitst")
                    return -2
            else:
                print("can not delete queue as queue you specified does not exist")
                return -1
        except:
            print("cannot delete Queue")
            return 0

    def pop(self, queueName1):
        if(Queue.objects.filter(queueName=queueName1, creatorID=self.username).exists() == True):
            q = Queue.objects.filter(queueName=queueName1, creatorID=self.username)[0]
            popedPerson = q.pop()
            return popedPerson
        else:
            print("cannot deletee queue as it is not in your created queue list")

    def deletePersonFromQueue(self, queueName1, userID1):
        if(Queue.objects.filter(queueName=queueName1, creatorID=self.username).exists() == True):
            q = Queue.objects.filter(queueName=queueName1, creatorID=self.username)[0]
            removedPerson = q.removeByID(userID1)
            return removedPerson
        else:
            print("cannot deletee queue as it is not in your created queue list")



class Queue(models.Model):
    queueName = models.CharField(max_length=20)
    creatorID = models.CharField(max_length=20)
    location = models.CharField(max_length=60)
    time = models.CharField(max_length=25)
    note = models.CharField(max_length=100)
    array = models.TextField(default='[]')
    speedData = models.CharField(max_length=50, default="300#2023-04-25 23:13:33")

    def __str__(self):
        return self.creatorID+"@"+self.queueName

    def pop(self):
        if(self.array!="[]"):
            lst = json.loads(self.array)
            firstPerson = lst.pop(0)
            self.array = json.dumps(lst)
            self.save()

            ##
            if(USER.objects.filter(username=firstPerson).exists()==True):
                u = USER.objects.filter(username=firstPerson)[0]
                lst = json.loads(u.joinedQueue)
                if(str(self.creatorID)+"#"+str(self.queueName) in lst):
                    lst.pop(lst.index(str(self.creatorID)+"#"+str(self.queueName)))
                    u.joinedQueue = json.dumps(lst)
                    u.save()
            ######### updating current speed #############
            speedData1 = self.speedData

            stored_instance = datetime.strptime(speedData1.split("#")[1], '%Y-%m-%d %H:%M:%S')         # loading sotred time in instance

            now_instance = datetime.now()
            now_time_string = now_instance.strftime('%Y-%m-%d %H:%M:%S')                             # loading now time in instance

            time_difference_seconds = (now_instance - stored_instance).total_seconds()                  # finding difference in sec

            self.speedData = str(time_difference_seconds)+"#"+now_time_string                           # updating speeddata
            ####

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
            return 0

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
            return 0

    def getSpeed(self):
        speedData1 = self.speedData
        return speedData1.split("#")[0]

    def removeByID(self,userID):
        if(self.array!="[]"):
            lst = json.loads(self.array)

            try:
                index = lst.index(userID)
            except:
                print("cannot delete as userID you specified does not exist in this qeueue")
            
            removedPerson = lst.pop(index)

            if(USER.objects.filter(username=userID).exists()==True):
                currentUser = USER.objects.filter(username=userID)[0]
                userList = currentUser.getJoinedQueues()
                if((str(self.creatorID)+"#"+str(self.queueName)) in userList):
                    userList.remove(str(self.creatorID)+"#"+str(self.queueName))
                    currentUser.joinedQueue = json.dumps(userList)
                    currentUser.save()
            
            self.array = json.dumps(lst)
            self.save()
            return removedPerson
        else:
            print("cannot delete as queue is empty")
            return 0