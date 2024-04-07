"""
See
https://docs.djangoproject.com/en/5.0/ref/contrib/admin/#module-django.contrib.admin

For inline admin see
https://stackoverflow.com/questions/73931689/django-admin-and-inline-related-models-filtering
"""

from django.contrib import admin
from .models import Category, Tag, Link, URL

admin.site.register(URL)
admin.site.register(Tag)
admin.site.register(Category)

admin.site.register(Link)