from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import models, serializers

class Notifications(APIView):

    def get(self, request, format=None):

        user = request.user

        notifications = models.Notifications.objects.filter(to=user)

        serializer = serializers.NotificationsSerializer(notifications, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

def create_notification(creator, to, type, image=None, comment=None):

    notification = models.Notifications.objects.create(
        creator = creator,
        to=to,
        notification_type=type,
        image=image,
        comment=comment
    )

    notification.save()

