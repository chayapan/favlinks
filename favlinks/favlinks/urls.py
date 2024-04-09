"""
URL configuration for favlinks project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.models import User
from django.contrib.auth import views as auth_views
from rest_framework import routers
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
    path('signup/', views.signup, name="signup"),
    path('v1/manage-urls/', views.manage_favorite_url, name="fav"),
    path('accounts/', include('django.contrib.auth.urls')),
    # path("accounts/login/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path('change-password/', auth_views.PasswordChangeView.as_view(), name="password_reset"),
    path('api/v1/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path("admin/", admin.site.urls),
]
