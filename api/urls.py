from django.urls import path
from .views import ConversationDetailView, WebhookCreateView, conversation_list_view, conversation_detail_view

urlpatterns = [
    path('conversations/', conversation_list_view, name='conversation_list'),
    path('conversations/<uuid:id>/', conversation_detail_view, name='conversation_detail'),
    path('webhook/', WebhookCreateView.as_view(), name='webhook'),
    path('conversations/<uuid:id>/', ConversationDetailView.as_view(), name='conversation_detail'),
]