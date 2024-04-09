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
from hashlib import sha256
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
        return self.name
    def __repr__(self) -> str:
        return f'<Cat:{self.name}(pk={self.pk})>'

class Tag(models.Model):
    value = models.CharField(max_length=250, unique=True)
    link_count = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
    def __str__(self) -> str:
        return f'{self.value}'
    def __repr__(self) -> str:
        return f'<Tag:{self.value}(pk={self.pk})>'

class URL(models.Model):
    """URL has many-to-many relationship with tag.
    https://docs.djangoproject.com/en/5.0/topics/db/examples/many_to_many/
    """
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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    state = models.CharField(max_length=10)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, related_name="links")
    tags = models.ManyToManyField(Tag, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favorite_links")
    url_text = models.CharField(max_length=250)
    url_hash = models.CharField(max_length=100, null=True)
    url = models.ForeignKey(URL, null=True, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=200, null=True)

    class Meta:
        verbose_name = 'Link'
        verbose_name_plural = 'Links'

    def save(self, *args, **kwargs):
        """Override model save. Compute hash of the URL value."""
        h = sha256()
        h.update(self.url_text.encode('utf-8'))
        self.url_hash =  h.hexdigest()
        super(Link, self).save(*args, **kwargs)

    def add_tag(self, tag_kw) -> Tag:
        tag, create = Tag.objects.get_or_create(value=tag_kw)
        if not create:
            tag.link_count += 1 # increment count
        self.tags.add(tag)
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


def make_favorite_link(url: str,  user:  User, category: str  = "", tags = []) -> Link:
    """Link is owned by User and belongs to Category
    1. The URL is hashed and look up in the URL table. 
    If there is existing, return 'url_already_exists' if not return 'new_url'.
    2. The URL hash is saved.
    3. Category is selected. Fetch from database.
    4. URL object retrieved.
    5. Tags are created and assigned to the Link object.
    6. Return the Link object.
    """
    q = URL.objects.filter(raw_url=url)
    if q.count() == 0: # 'new_url'
        url_obj = URL.objects.create(raw_url=url)
    else:
        url_obj = URL.objects.get(raw_url=url)
    c = Category.objects.get(name=category)
    # create Link object
    # check if link already favorited
    q = Link.objects.filter(user=user, url_text=url)
    if q.count() == 0:
        link = Link.objects.create(url=url_obj, url_text=url, user=user, category=c)
        for t  in tags:
            if isinstance(t, str):
                link.add_tag(t)
            else:
                link.add_tag(t.value)
        link.update_preview()
        return link
    # link already exists in user's bookmark
    return q.first()