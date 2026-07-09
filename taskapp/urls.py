from django.urls import path
from .views import project_views,task_views
from taskapp.views.user_views import RegisterView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
) 



urlpatterns = [
    path('user/register/',RegisterView.as_view(),name='register'),
    path('user/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('user/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('project/',project_views.ProjectListCreateAPI.as_view(),name='project-list-create'),
    path('project/<int:pk>',project_views.ProjectDetailAPI.as_view(),name ='project-detail'),
   
    path('task/',task_views.TaskListCreateAPI.as_view(),name='task-list-create'),
    path('task/<int:pk>',task_views.TaskDetailAPI.as_view(),name='task-detail'),

    
]