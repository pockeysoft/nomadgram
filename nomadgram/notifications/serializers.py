from rest_framework import serializers
from . import models
from nomadgram.images import serializers as image_serializers

class NotificationsSerializer(serializers.ModelSerializer):

    creator = image_serializers.FeedUserSerializer()
    image = image_serializers.SmallImageSerializer()

    class Meta:
        model = models.Notifications
        fields = '__all__'
