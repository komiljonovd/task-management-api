from taskapp.serializers.project_serializer import ProjectSerializer,Project
from rest_framework import generics,permissions
from taskapp.permissions.project_owner import IsProjectOwnerOrTaskAssignee

class ProjectListCreateAPI(generics.ListCreateAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated] 

    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user)
    
    

class ProjectDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user)