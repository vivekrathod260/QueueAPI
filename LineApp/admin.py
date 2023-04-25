from django.contrib import admin

# Register your models here.

from LineApp.models import USER
admin.site.register(USER)

from LineApp.models import Queue
admin.site.register(Queue)