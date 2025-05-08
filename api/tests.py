from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from api.models import Conversation
import uuid

class ConversationDetailViewTest(APITestCase):
    def setUp(self):
        # Cria um usuário e faz login com ele
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.client = APIClient()
        self.client.login(username='testuser', password='testpass123')

        # Cria uma conversa
        self.conversation = Conversation.objects.create(id=uuid.uuid4())

    def test_authenticated_user_can_view_conversation_detail(self):
        url = f'/conversations/{self.conversation.id}/'
        response = self.client.get(url)
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('id', response.data)

    def test_unauthenticated_user_cannot_view_conversation_detail(self):
        self.client.logout()
        url = f'/conversations/{self.conversation.id}/'
        response = self.client.get(url)
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
