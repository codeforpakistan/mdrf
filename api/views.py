# Create your views here.
import json

from django.contrib.auth.models import User
from firebase_admin import messaging
from push_notifications.models import GCMDevice
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api.serializers import UserSerializer


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=True, methods=['GET'])
    def notify(self, request, pk=None):
        # Retrieve the user's registered FCM device(s)
        # Note: A user might have multiple devices (e.g., mobile + web, or multiple browsers)
        devices = GCMDevice.objects.filter(user_id=pk, active=True)
        message = messaging.Message(
            notification=messaging.Notification(
                title="New Friend Request",
                body="Jane Doe wants to connect with you."
            ),
            webpush=messaging.WebpushConfig(
                notification=messaging.WebpushNotification(
                    icon="/static/images/notification-icon.png", # The small icon
                    image="/static/images/jane-profile.jpg",     # A larger preview image
                    require_interaction=True,                    # Keeps the notification on screen until dismissed
                ),
                # 'fcm_options' allows you to define where the user goes when they click the notification
                fcm_options=messaging.WebpushFCMOptions(
                    link="https://yoursite.com/profile/janedoe"
                )
            )
        )

        for device in devices:
            # Pass the messaging.Message object instead of a string
            device.send_message(message)

        return Response(data='Message sent', status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def save_token(self, request, pk=None):
        token = request.data.get('token')
        
        if not token:
            return Response({"error": "No token provided"}, status=400)

        device, created = GCMDevice.objects.get_or_create(
            registration_id=token,
            cloud_message_type='FCM',
            defaults={
                'user': request.user if request.user.is_authenticated else None,
                'name': 'Web Browser'
            }
        )
        
        if not created and request.user.is_authenticated and device.user != request.user:
            device.user = request.user
            device.save()

        return Response({"status": "success", "created": created})