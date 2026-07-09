from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from taskapp.models import Task,Project
from django.utils import timezone
from datetime import timedelta

User = get_user_model()

class TaskAPITestCase(APITestCase):
    def setUp(self) -> None:
        self.owner = User.objects.create_user(username="owner", password="password123")
        self.worker = User.objects.create_user(username="worker", password="password123")
        
        self.project = Project.objects.create(name="Project", owner=self.owner)
        
        self.task = Task.objects.create(
            title="Task 1", 
            description="Initial description", # Обязательно
            project=self.project, 
            deadline=timezone.now() + timedelta(days=1),
            assigned_user=self.worker,
            status="todo" # Важно: строго по choices модели
        )
        
        self.list_create_url = reverse("task-list-create")
        self.detail_url = reverse("task-detail", kwargs={"pk": self.task.pk})
        
        self.client.force_authenticate(user=self.owner)

    def test_create_task(self) -> None:
        data = {
            "title": "New Task", 
            "description": "Test",
            "project": self.project.pk,
            "deadline": (timezone.now() + timedelta(days=2)).isoformat(),
            "assigned_user": self.worker.pk,
            "status": "todo" 
        }
        response = self.client.post(self.list_create_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_task(self) -> None:
        data = {
            "title": "Updated Task",
            "description": "Updated",
            "project": self.project.pk, 
            "deadline": self.task.deadline.isoformat(),
            "assigned_user": self.worker.pk,
            "status": "todo"
        }
        response = self.client.put(self.detail_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, "Updated Task")

    def test_delete_task(self) -> None:
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_list_tasks(self) -> None:
        response = self.client.get(self.list_create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_task_validation(self) -> None:
        data = {
            "title": "", 
            "description": "Test",
            "project": self.project.pk,
            "deadline": (timezone.now() - timedelta(days=2)).isoformat(),
            "assigned_user": self.worker.pk,
            "status": "todo" 
        }
        response = self.client.post(self.list_create_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    