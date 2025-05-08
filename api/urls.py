from django.urls import path
from .views import ConversationDetailView, WebhookCreateView

urlpatterns = [
    path('webhook/', WebhookCreateView.as_view(), name='webhook'),
    path('conversations/<uuid:id>/', ConversationDetailView.as_view(), name='conversation_detail'),
]