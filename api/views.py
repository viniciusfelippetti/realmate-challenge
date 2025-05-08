from rest_framework.generics import RetrieveAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, mixins
from django.utils.dateparse import parse_datetime
from .serializers import ConversationSerializer, MessageSerializer
from django.shortcuts import render, get_object_or_404
from .models import Conversation

class WebhookCreateView(mixins.CreateModelMixin, GenericAPIView):
    """
    View que processa as mensagens
    """
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            event_type = request.data.get('type')
            timestamp = parse_datetime(request.data.get('timestamp'))
            data = request.data.get('data', {})

            if event_type == "NEW_CONVERSATION":
                Conversation.objects.create(id=data['id'])

            elif event_type == "NEW_MESSAGE":
                conversation = Conversation.objects.filter(id=data['conversation_id']).first()
                if not conversation:
                    return Response({"error": "Conversa não encontrada"}, status=status.HTTP_404_NOT_FOUND)
                if conversation.status == 'CLOSED':
                    return Response({"error": "Conversa foi encerrada"}, status=status.HTTP_400_BAD_REQUEST)

                serializer = self.get_serializer(data={
                    "id": data['id'],
                    "direction": data['direction'],
                    "content": data['content'],
                    "timestamp": timestamp
                })
                serializer.is_valid(raise_exception=True)
                serializer.save(conversation=conversation)

            elif event_type == "CLOSE_CONVERSATION":
                conv = Conversation.objects.filter(id=data['id']).first()
                if conv:
                    conv.status = 'CLOSED'
                    conv.save()

            else:
                return Response({"error": "event_type não reconhecido."}, status=status.HTTP_400_BAD_REQUEST)

            return Response({"status": "success"})

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ConversationDetailView(RetrieveAPIView):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'




def conversation_list_view(request):
    conversations = Conversation.objects.all()
    return render(request, 'conversations/list.html', {'conversations': conversations})

def conversation_detail_view(request, id):
    conversation = get_object_or_404(Conversation, id=id)
    messages = conversation.messages.all()
    return render(request, 'conversations/detail.html', {'conversation': conversation, 'messages': messages})
