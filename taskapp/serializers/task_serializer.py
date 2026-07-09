from rest_framework import serializers
from taskapp.models import Task
from django.utils import timezone
from taskapp.models import Status,Priority


class TaskSerializer(serializers.ModelSerializer):
    project_name = serializers.ReadOnlyField(source='project.name')
    project_description = serializers.ReadOnlyField(source ='project.description')
    username = serializers.ReadOnlyField(source ='assigned_user.username')
    project_owner = serializers.ReadOnlyField(source='project.owner.username')


    class Meta:
        model = Task
        fields = ['id','title','description','status',
                  'priority','deadline','assigned_user','username',
                  'project','project_name','project_description',
                  'project_owner']
               
    def validate_title(self,value):
        if not value or not value.strip():
            raise serializers.ValidationError(
                {'title':'Title can not be empty.'}
            )
        
        return value
    
    def validate_deadline(self,value):
        if value < timezone.now():
            raise serializers.ValidationError(
                {'deadline':'Deadline cannot be in the past.'}
            )

        return value
    
    def validate_status(self,value):
        if value not in Status.values:
            raise serializers.ValidationError('Such a status does not exist.')
        
        return value
    
    def validate_priority(self,value):
        if value not in Priority.values:
            raise serializers.ValidationError('Such a priority does not exist.')
        
        return value