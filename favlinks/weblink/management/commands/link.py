"""
Admin command for Link entities.

    manage.py link create URL --user

Command: 
    link
Sub-command:
    create
    list-user-  
List for user
Get preview
Add new link:   EMAIL  URL


"""

from django.core.management.base import BaseCommand, CommandError
from weblink.models import find_user, Link, Category

class Command(BaseCommand):
    help = "Manage web links category. List, add/create, remove."

    def add_arguments(self, parser):
        """Arguments for this command: --delete"""
        parser.add_argument("subcommand", nargs="+", type=str, choices=['list','add','delete','fetch-preview'])
        parser.add_argument("--userId", nargs="?", type=str)
        parser.add_argument("--email", nargs="?", type=str)
        parser.add_argument("--url", nargs="?", type=str)
        parser.add_argument("--ids", nargs="?", type=str)

    def handle(self, *args, **options):
        cmd = options['subcommand'][0]
        if 'list' == cmd:
            self.stdout.write("=PK=" + "\t=FAV-LINK====" + "\t\t===URL===")
            q = Link.objects.all()
            for l in q:
                self.stdout.write("%04d" % l.pk + "\t%s" % l + "\t%s" % l.url)
        if 'delete' == cmd:
            link_ids = options['pks'].split(',')
            for id in link_ids:
                try:
                    link = Link.objects.get(pk=id)
                    link.delete()
                    self.stdout.write(
                        self.style.SUCCESS('Successfully delete link for id="%s" user="%s" url="%s"' % (id, link.user.pk, link.url_text))
                    )
                except:
                    self.stdout.write(
                        self.style.ERROR('Fail to delete link id="%s" ' % (id, ))
                    )
        if 'add' == cmd:
            uid = options['userId'].split(',')[0] # TODO: better parser
            email = options.get('email', None)
            u = find_user(id=uid,email=email)
            the_url = options['url']
            cat, created = Category.objects.get_or_create(name='-') # the default category for everyone
            l = Link.set_favorite(user=u, category=cat, url=the_url)
            self.stdout.write(
                self.style.SUCCESS('Successfully add favorite link for user="%s" url="%s"' % (u, the_url))
            )
        if 'fetch-preview' == cmd:
            link_ids = options['ids'].split(',')
            for id in link_ids:
                try:
                    link = Link.objects.get(pk=id)
                    link.update_preview()
                    self.stdout.write(
                        self.style.SUCCESS('Successfully fetch content preview for id="%s" user="%s" url="%s"' % (id, link.user.pk, link.url_text))
                    )
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR('Fail get preview for link id="%s" : %s' % (id, e))
                    )

