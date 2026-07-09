from taskapp.serializers.task_serializer import TaskSerializer,Task
from rest_framework import generics,permissions,filters,serializers
from django.db import models
from taskapp.permissions.project_owner import IsProjectOwnerOrTaskAssignee
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page


class TaskListCreateAPI(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated,IsProjectOwnerOrTaskAssignee]
    filter_backends = [filters.SearchFilter,DjangoFilterBackend]
    search_fields = ['title']
    filterset_fields = ['status','priority','deadline']
      
    def get_queryset(self):
        return Task.objects.select_related('project').filter(
            models.Q(project__owner=self.request.user) | models.Q(assigned_user=self.request.user)
        ).distinct()
    
    def perform_create(self, serializer):
        project = serializer.validated_data.get('project')

        if project.owner!=self.request.user:
            raise serializers.ValidationError(
                {'project':'You do not have permission to perform this action.'})

        serializer.save()

class TaskDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated,IsProjectOwnerOrTaskAssignee]


    def get_queryset(self):
        return Task.objects.filter(
        models.Q(project__owner=self.request.user) | models.Q(assigned_user=self.request.user)
    ).distinct()
        