from django.shortcuts import render
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.response import Response
import jwt
from testproject.settings import api_settings

jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
jwt_get_username_from_payload = api_settings.JWT_PAYLOAD_GET_USERNAME_HANDLER
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    if user:
            payload = jwt_payload_handler(user)
            jwt_token = {'token': jwt.encode(payload, "mysecret")}
    #token = jwt.encode(payload, "myscert")
    #token, _ = Token.objects.get_or_create(user=user)
            return Response(jwt_token,
                    status=HTTP_200_OK)
@csrf_exempt
@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def sample_api(request):
    data = {'sample_data': 123}
    return Response(data, status=HTTP_200_OK)