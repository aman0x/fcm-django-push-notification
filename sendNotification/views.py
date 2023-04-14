from rest_framework.views import APIView
from rest_framework.response import Response
from fcm_django.models import FCMDevice
from firebase_admin.messaging import Message, Notification
from django.conf import settings

# Create your views here.


class SendNotification(APIView):
    permission_classes = []
    def get(self, request):
        queryset = FCMDevice.objects.all()
        param_value = request.query_params.get('name', None)
        message_value = request.query_params.get('Test', None)
        fcm_key = settings.FCM_DJANGO_SETTINGS.get('FCM_SERVER_KEY')

        if param_value is not None:
            queryset = queryset.filter(name=param_value)
        devices = list(queryset)
        # print(devices)
        if devices:
            for device in devices:
                device.fcm_key = fcm_key
                # device.registration_id = registration_id
                device.token = device.registration_id
                xyz1 = FCMDevice.objects.send_message(Message(notification=Notification(title="title", body="body")))
                xyz = device.send_message(Message(notification=Notification(title="Info", body=message_value)))
                print(xyz)
            data = [{
                'id': device.id,
                'name': device.name,
                'registration_id': device.registration_id,
                'message': message_value
                # add any other fields you want to include in the response
            } for device in devices]
            # print(data)
            return Response(data, status=200)
        else:
            return Response({"error": "Device not found"}, status=404)
