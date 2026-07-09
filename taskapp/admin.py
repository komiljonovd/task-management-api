from django.contrib import admin
from .models import Project,Task

# Register your models here.

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['id','name','description','owner','created_at','updated_at']


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['id','title','description','status','priority','deadline','assigned_user','project','created_at','updated_at']


