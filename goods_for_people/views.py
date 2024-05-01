from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import permission_classes, api_view, authentication_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_jwt.utils import jwt_decode_handler

from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly
from .serializers import UserSerializer, MessageSerializer, NotificationSerializer, CreateUserSerializer, \
    AdDepthSerializer, ChatDepthSerializer
from .serializers import AdSerializer
from .serializers import ChatSerializer
from .serializers import CategorySerializer
from .models import Profile, Message, Notification
from .models import Ad
from .models import Chat
from .models import Category


@api_view()
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def User(request):
    return Response({
        'data': UserSerializer(request.user).data
    })


class UserViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['get', 'post', 'put', 'delete']

    def get_queryset(self):
        queryset = Profile.objects.all()
        if self.request.method == 'GET':
            params = self.request.query_params.dict()
            try:
                queryset = queryset.filter(username=params['username'])
            except:
                pass
            try:
                queryset = queryset.filter(first_name__icontains=params['first_name'])
            except:
                pass
            try:
                queryset = queryset.filter(last_name__icontains=params['last_name'])
            except:
                pass
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = CreateUserSerializer(data=request.data)
        if serializer.is_valid():
            if Profile.objects.filter(username=request.data.get('username')).count() != 0:
                return Response(status=status.HTTP_409_CONFLICT, data='User with this username is already registered')
            new_user = serializer.save()
            new_user.set_password(new_user.password)
            new_user.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)

    def update(self, request, *args, **kwargs):
        queryset = Profile.objects.all()
        serializer = UserSerializer(data=request.data)
        if request.data.get('id'):
            if serializer.is_valid():
                updated_user = serializer.save()
                updated_user.set_password(updated_user.password)
                queryset.filter(id=request.data.get('id')).update(**updated_user.data)
                return Response(data=updated_user.data, status=status.HTTP_200_OK)
            return Response(serializer.errors)

    def destroy(self, request, *args, **kwargs):
        queryset = Profile.objects.all()
        if self.get_object().id:
            user = queryset.filter(id=self.get_object().id)
            if user.count() != 1:
                return Response(status=status.HTTP_204_NO_CONTENT)
            user.delete()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


@authentication_classes([JWTAuthentication])
@permission_classes([IsAdminOrReadOnly])
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    http_method_names = ['get', 'post', 'delete']

    def create(self, request, *args, **kwargs):
        if not request.data.get('title'):
            return Response(status=status.HTTP_400_BAD_REQUEST, data='Title is missing')
        new_category = CategorySerializer(data=request.data)
        if new_category.is_valid():
            new_category.save()
            return Response(data=new_category.data, status=status.HTTP_201_CREATED)
        return Response(new_category.errors)

    def destroy(self, request, *args, **kwargs):
        queryset = Category.objects.all()
        if self.get_object().id:
            category = queryset.filter(id=self.get_object().id)
            if category.count() != 1:
                return Response(status=status.HTTP_204_NO_CONTENT)
            category.delete()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class AdDepthViewSet(viewsets.ModelViewSet):
    serializer_class = AdDepthSerializer
    http_method_names = ['get']

    def get_queryset(self):
        queryset = Ad.objects.all().order_by('publication_date')
        if self.request.method == 'GET':
            params = self.request.query_params.dict()
            try:
                queryset = queryset.filter(user_id=params['user_id'])
            except:
                pass
            try:
                queryset = queryset.filter(user_id__city__incontains=params['city'])
            except:
                pass
            try:
                queryset = queryset.filter(title__icontains=params['title'])
            except:
                pass
            try:
                queryset = queryset.filter(category=params['c_id'])
            except:
                pass
            try:
                queryset = queryset.filter(price__lte=params['max_p'])
            except:
                pass
            try:
                queryset = queryset.filter(price__gte=params['min_p'])
            except:
                pass
        return queryset


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticatedOrReadOnly])
class AdViewSet(viewsets.ModelViewSet):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    http_method_names = ['get', 'post', 'put', 'delete']

    def get_queryset(self):
        queryset = Ad.objects.all()
        if self.request.method == 'GET':
            params = self.request.query_params.dict()
            try:
                queryset = queryset.filter(user_id=params['user_id'])
            except:
                pass
            try:
                queryset = queryset.filter(user_id__city=params['city'])
            except:
                pass
            try:
                queryset = queryset.filter(title__icontains=params['title'])
            except:
                pass
            try:
                queryset = queryset.filter(category=params['c_id'])
            except:
                pass
            try:
                queryset = queryset.filter(price__lte=params['max_p'])
            except:
                pass
            try:
                queryset = queryset.filter(price__gte=params['min_p'])
            except:
                pass
        return queryset

    def create(self, request, *args, **kwargs):
        if not request.data.get('title') or not request.data.get('price') or not request.data.get('category'):
            return Response(status=status.HTTP_400_BAD_REQUEST, data='Some data is missing')
        data = request.data
        data['user_id'] = request.user.id
        new_ad = AdSerializer(data=data)
        if new_ad.is_valid():
            new_ad.save()
            return Response(data=new_ad.data, status=status.HTTP_201_CREATED)
        return Response(new_ad.errors)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data
        queryset = Ad.objects.all()
        if request.user.id != instance.user_id.id:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        decoded_payload = jwt_decode_handler(request.headers.get("Authorization")[7:])
        data['user_id'] = decoded_payload.get('user_id')
        updated_ad = AdSerializer(data=data)
        if instance.id:
            if updated_ad.is_valid():
                queryset.filter(id=instance.id).update(**updated_ad.data)
                return Response(data=updated_ad.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user.id != instance.user_id.id or not request.user.is_staff:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        if instance.status == 'S':
            return Response(data='already sold')
        instance.status = 'S'
        instance.save()
        return Response(status=status.HTTP_200_OK)


class ChatDepthViewSet(viewsets.ModelViewSet):
    serializer_class = ChatDepthSerializer
    http_method_names = ['get']

    def get_queryset(self):
        queryset = Chat.objects.all()
        if self.request.method == 'GET':
            params = self.request.query_params.dict()
            try:
                queryset = queryset.filter(user_1=params['u1_id'])
            except:
                pass
            try:
                queryset = queryset.filter(user_2=params['u2_id'])
            except:
                pass
        return queryset


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticatedOrReadOnly])
class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    http_method_names = ['get', 'post', 'delete']

    def get_queryset(self):
        queryset = Chat.objects.all()
        if self.request.method == 'GET':
            params = self.request.query_params.dict()
            try:
                queryset = queryset.filter(user_1=params['u1_id'])
            except:
                pass
            try:
                queryset = queryset.filter(user_2=params['u2_id'])
            except:
                pass
        return queryset

    def create(self, request, *args, **kwargs):
        if not request.data.get('user_1') or not request.data.get('user_2'):
            return Response(status=status.HTTP_400_BAD_REQUEST, data='Some data is missing')

        data = request.data

        if data['user_1'] == data['user_2']:
            return Response(status=status.HTTP_400_BAD_REQUEST, data='Same users id')

        decoded_payload = jwt_decode_handler(request.headers.get("Authorization")[7:])
        auth_user = decoded_payload.get('user_id')
        chat1_exists = Chat.objects.filter(user_1=data['user_1']).filter(user_2=data['user_2'])
        if chat1_exists.count() != 0:
            return Response(status=status.HTTP_200_OK, data=chat1_exists[0].id)

        chat2_exists = Chat.objects.filter(user_2=data['user_1']).filter(user_1=data['user_2'])
        if chat2_exists.count() != 0:
            return Response(status=status.HTTP_200_OK, data=chat2_exists[0].id)

        data['creator'] = auth_user
        new_chat = ChatSerializer(data=data)
        if new_chat.is_valid():
            new_chat.save()
            return Response(data=new_chat.data, status=status.HTTP_201_CREATED)
        return Response(new_chat.errors)

    def destroy(self, request, *args, **kwargs):
        queryset = Chat.objects.all()
        if self.get_object().id:
            chat = queryset.filter(id=self.get_object().id)
            if chat.count() != 1:
                return Response(status=status.HTTP_204_NO_CONTENT)
            chat.delete()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
