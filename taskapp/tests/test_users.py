from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class AuthAPITestCase(APITestCase):
    def setUp(self) -> None:
        self.username = "testuser"
        self.password = "password123"
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.login_url = reverse("token_obtain_pair")
        self.refresh_url = reverse("token_refresh")

    def test_login_success(self) -> None:
        """Тест: получение токенов при правильном логине."""
        data = {"username": self.username, "password": self.password}
        response = self.client.post(self.login_url, data, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_login_failure(self) -> None:
        """Тест: ошибка при неправильном пароле."""
        data = {"username": self.username, "password": "wrongpassword"}
        response = self.client.post(self.login_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_token_refresh(self) -> None:
        """Тест: обновление access токена через refresh токен."""
        # Сначала получаем токены
        login_response = self.client.post(self.login_url, {"username": self.username, "password": self.password})
        refresh_token = login_response.data["refresh"]
        
        # Обновляем
        response = self.client.post(self.refresh_url, {"refresh": refresh_token}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)