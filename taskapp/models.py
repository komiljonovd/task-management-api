from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


# Create your models here.

class Status(models.TextChoices):
    TODO = 'todo',_('To Do')
    IN_PROGRESS = 'in_progress',_('In Progress')
    DONE = 'done',_('Done')


class Priority(models.TextChoices):
    LOW = 'low',_('Low')
    MEDIUM = 'medium',_('Medium')
    HIGH = 'high',_('High')


class Project(models.Model):
    name = models.CharField(max_length=256,unique=True)
    description = models.CharField(max_length=256)
    owner = models.ForeignKey(User,on_delete=models.CASCADE,related_name='projects')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'projects'
        verbose_name ='project'
        verbose_name_plural ='projects'
        ordering = ['-created_at']  



class Task(models.Model):
    title = models.CharField(max_length=256)
    description = models.CharField(max_length=256)
    status = models.CharField(
        max_length=20, 
        choices=Status.choices, 
        default=Status.TODO,
        db_index=True
    )

    priority = models.CharField(
        max_length=20, 
        choices=Priority.choices, 
        default=Priority.MEDIUM,
        db_index=True
    )

    deadline = models.DateTimeField()
    assigned_user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='tasks')
    project = models.ForeignKey(Project,on_delete=models.CASCADE,related_name='tasks')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.project.name} | {self.title}"
    

    class Meta:
        db_table = 'tasks'
        verbose_name ='Task'
        verbose_name_plural ='tasks'
        ordering = ['-created_at']  
