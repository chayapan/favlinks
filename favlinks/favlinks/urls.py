"""
URL configuration for favlinks project.
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from rest_framework import routers
from rest_framework.authtoken import views as drf_views
from weblink import views 
# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'categories', views.CategoryViewSet)
router.register(r'tags', views.TagViewSet)
router.register(r'links', views.LinkViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'favorited-urls', views.URLViewSet)
# router.register(r'groups', views.GroupViewSet)


urlpatterns = [
    path('', views.home, name="home"),
    path('profile/', views.profile, name="profile"),
    path('signup/', views.signup, name="signup"),
    path('v1/signup/', views.create_user, name="signup_api"),
    path('v1/manage-urls/', views.manage_favorite_url, name="fav"),
    path('accounts/', include('django.contrib.auth.urls')),
    path('change-password/', auth_views.PasswordChangeView.as_view(), name="password_reset"),
    path('api/v1/', include(router.urls)),
    path('api-token-auth/', drf_views.obtain_auth_token),
    path('api-auth/', include('rest_framework.urls')),
    path("admin/", admin.site.urls),
]
