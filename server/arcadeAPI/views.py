from .models import User, Game, Action
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from .serializers import UserSerializer, ActionSerializer
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os, shutil

import face_recognition
import numpy as np

@method_decorator(csrf_exempt, name='dispatch')
class UserViewSet(APIView): # API endpoint that allows users to be viewed or created.
    def get(self, request):
        users = User.objects.all().order_by('date_joined')
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class ActionViewSet(APIView): # API endpoint that allows actions to be viewed or created.
    def get(self, request):
        actions = Action.objects.all().order_by('date_time')
        serializer = ActionSerializer(actions, many=True)
        return Response(serializer.data)

    def post(self, request):
        # clears current_user folder
        current_user_folder = 'current_user'
        for filename in os.listdir(current_user_folder):
            file_path = os.path.join(current_user_folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))

        # saves image in current_user folder with current_user_photo.jpg as name
        image_file = request.FILES['photo']
        path = default_storage.save(os.path.join('current_user', 'current_user_photo.jpg'), ContentFile(image_file.read()))

        # face recognition
        unknown_image = face_recognition.load_image_file(path)
        recognized_a_face_in_webcam_photo = True
        try:
          unknown_encoding = face_recognition.face_encodings(unknown_image)[0]
        except IndexError:
          print('Can\'t recognize a face in the webcam photo')
          recognized_a_face_in_webcam_photo = False

        username = '<unknown>'
        if recognized_a_face_in_webcam_photo:
          users_photos_folder = 'users_photos'
          for filename in os.listdir(users_photos_folder):
              known_image = face_recognition.load_image_file(os.path.join(users_photos_folder, filename))
              known_encoding = face_recognition.face_encodings(known_image)[0]
              results = face_recognition.compare_faces([known_encoding], unknown_encoding)
              userIsRecognized = np.asscalar(results[0])
              if userIsRecognized:
                username = filename.replace('.jpg', '')
                break

        # process request
        data = request.data.dict()
        data['user'] = username

        serializer = ActionSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)