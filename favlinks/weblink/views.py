from django.shortcuts import render, redirect
from django.contrib.auth.models import Group, User
from django.contrib.auth import forms as auth_forms
from rest_framework import permissions, viewsets
from weblink import serializers
from weblink import forms as app_forms
from weblink import models as app_models

def signup(request):
    signup_form = auth_forms.UserCreationForm()
    if request.POST:
        signup_form = auth_forms.UserCreationForm(request.POST)
        if signup_form.is_valid():
            signup_form.save()
            print("Saved. User created.")
            return redirect('login') # after account successfully create redirect to login page
        else:
            print(signup_form.error_messages)
    context = {
        'signup_form': signup_form,
        'login_form': auth_forms.AuthenticationForm()
    }
    return render(request, template_name="registration/signup.html", context=context)

def home(request):
    if not request.user.is_authenticated:
        return redirect('signup')
    
    context = {
        'user_profile_form': app_forms.ProfileUpdateForm(instance=request.user),
        'add_link_form': app_forms.FavoriteLinkForm(),
        'favorite_urls': app_models.Link.objects.filter(user=request.user).all()
    }
    return render(request, template_name="home.html", context=context)

def manage_favorite_url(request):
    if request.POST:
        print(request)
        form = app_forms.FavoriteLinkForm(request.POST)
        form.is_valid()
        print(form.cleaned_data)
        url_text = form.cleaned_data['url_text']
        category = form.cleaned_data['category']
        tags_selected = form.cleaned_data['tag_select']
        my_link = app_models.make_favorite_link(url_text, request.user, category, tags_selected)
        print(my_link)
        return redirect('home')
    else:
        return redirect('home')

# ViewSets define the view behavior for REST framework.
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = serializers.Category.objects.all()
    serializer_class = serializers.CategorySerializer

class TagViewSet(viewsets.ModelViewSet):
    queryset = serializers.Tag.objects.all()
    serializer_class = serializers.TagSerializer

class URLViewSet(viewsets.ModelViewSet):
    queryset = serializers.URL.objects.all()
    serializer_class = serializers.URLSerializer

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