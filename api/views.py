from rest_framework.generics import RetrieveAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework import status, mixins
from .models import Conversation
from django.utils.dateparse import parse_datetime
from .serializers import ConversationSerializer, MessageSerializer


class WebhookCreateView(mixins.CreateModelMixin, GenericAPIView):
    """
    View que processa eventos de webhook via POST.
    """
    serializer_class = MessageSerializer

    def post(self, request, *args, **kwargs):
        try:
            event_type = request.data.get('type')
            timestamp = parse_datetime(request.data.get('timestamp'))
            data = request.data.get('data', {})

            if event_type == "NEW_CONVERSATION":
                Conversation.objects.get_or_create(id=data['id'])

            elif event_type == "NEW_MESSAGE":
                conversation = Conversation.objects.filter(id=data['conversation_id']).first()
                if not conversation:
                    return Response({"error": "Conversa não encontrada"}, status=status.HTTP_404_NOT_FOUND)
                if conversation.status == 'CLOSED':
                    return Response({"error": "Conversa foi encerrada"}, status=status.HTTP_400_BAD_REQUEST)

                # Usa o serializer para criar a mensagem
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
    lookup_field = 'id'