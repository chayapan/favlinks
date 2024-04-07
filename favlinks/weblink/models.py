""" This module define entities used by the FavLinks app.
Models:
    1. Link  - user-favorite-link
    2. URL
    3. Category
    4. Tag
    5. User
"""
from django.db import models
from django.contrib.auth.models import User
from .preview import preview_url
import time

def find_user(id=None, email=None):
    """Returns user object by userId or registered email."""
    try:
        if id:
            u = User.objects.get(pk=id)
        elif email:
            q = User.objects.filter(email=email)
            u = q.first()
        return u
    except Exception as e:
        raise Exception("Lookup account error: %s id=%s email=%s" % (e, id, email))
    return None

class Category(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=250, unique=True)
    parent = models.ForeignKey("Category", null=True, on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = 'Link Category'
        verbose_name_plural = 'Link Categories'

    def __str__(self) -> str:
        return f'<Cat:{self.name}(pk={self.pk})>'

class Tag(models.Model):
    value = models.CharField(max_length=250, unique=True)
    url_count = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def __str__(self) -> str:
        return f'<Tag:{self.value}(pk={self.pk})>'

class URL(models.Model):
    """URL has many-to-many relationship with tag.
    https://docs.djangoproject.com/en/5.0/topics/db/examples/many_to_many/
    """
    tags = models.ManyToManyField(Tag)
    raw_url = models.CharField(max_length=2000, unique=True)
    last_preview_capture = models.DateTimeField("preview fetched", null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'URL'
        verbose_name_plural = 'URLs'

    @classmethod
    def add_to_crawler_queue(cls, url: str):
        print("Add URL to preview queue: %s" % url)
        the_url, create = cls.objects.get_or_create(raw_url=url)
        time.sleep(3) # simulate sleep
        print("Preview fetched.")

    def __str__(self) -> str:
        return f'<URL:{self.raw_url}(pk={self.pk})>'

class Link(models.Model):
    """When a user creates a link the app first checks if that link has already bookmarked or not by looking up the raw URL."""
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, related_name="links")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favorite_links")
    url_text = models.CharField(max_length=250)
    url = models.ForeignKey(URL, null=True, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=200, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Link'
        verbose_name_plural = 'Links'
    
    def add_tag(self, tag_kw) -> Tag:
        tag, create = Tag.objects.get_or_create(value=tag_kw)
        if not create:
            # increment count
            tag.url_count += 1
        self.url.tags.add(tag)
        tag.save()
        # Check transaction here..
        return tag
    def update_preview(self):
        """Get preview for the URL. 
        TODO: make proper functionality analysis for this. How do use job queue."""
        if not self.url.last_preview_capture:
            timestamp, title, status_code = preview_url(link=self)
            self.url.last_preview_capture = timestamp
            self.title = title
            # status_tag, created = Tag.objects.get_or_create(value=preview.status_code)
            # self.url.tags.set(status_tag)
            self.url.save()
            self.save()

    @classmethod 
    def set_favorite(cls, user: User, category: Category, url: str):
        the_url, created = URL.objects.get_or_create(raw_url=url)
        if created:
            # The field 'last_preview_capture' is null.
            # put in a queue to fetch a preview. 
            print("Created new URL instance")
            URL.add_to_crawler_queue(the_url)
        link_obj = cls(url_text=url, user=user, category=category, url=the_url)
        link_obj.save()
        # output some logs...
        return link_obj
    
    def __str__(self) -> str:
        return f'<Link:user={self.user.username}:url={self.url_text}>'
