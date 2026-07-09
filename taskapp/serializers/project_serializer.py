from taskapp.models import Project
from rest_framework import serializers

class ProjectSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    owner_name = serializers.ReadOnlyField(source = 'owner.username')

    class Meta:
        model = Project
        fields = ['id','name','description','owner','owner_name']



