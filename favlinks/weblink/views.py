from django.shortcuts import render
from django.contrib.auth.models import Group, User
from rest_framework import permissions, viewsets
from weblink import serializers

# ViewSets define the view behavior.
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = serializers.Category.objects.all()
    serializer_class = serializers.CategorySerializer

class TagViewSet(viewsets.ModelViewSet):
    queryset = serializers.Tag.objects.all()
    serializer_class = serializers.TagSerializer

class LinkViewSet(viewsets.ModelViewSet):
    queryset = serializers.Link.objects.all()
    serializer_class = serializers.LinkSerializer

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = serializers.UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all().order_by('name')
    serializer_class = serializers.GroupSerializer
    permission_classes = [permissions.IsAuthenticated]