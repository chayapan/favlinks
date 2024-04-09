from django.contrib.auth.models import Group, User
from rest_framework import serializers
from weblink.models import Category, Tag, Link, URL

# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'favorite_links']

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class LinkSerializer(serializers.HyperlinkedModelSerializer):
    options = serializers.HyperlinkedRelatedField(
        view_name='url-detail',
        lookup_field = 'id',
        many=True,
        read_only=True)

    class Meta:
        model = Link
        fields = ['id', 'title', 'category', 'tags', 'updated_at', 'user', 'url_text', 'url_hash', 'options']
        lookup_field = 'id'
        extra_kwargs = {
            'url': {'lookup_field': 'id'}
        }

class URLSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = URL
        fields = ['id','raw_url','updated_at', 'last_preview_capture']

class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'url', 'links']

class TagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tag
        fields = ['value', 'url']
    
    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return Tag.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.value = validated_data.get('value', instance.value)
        instance.save()
        return instance