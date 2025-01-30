"""
Admin command for Link entities.

    manage.py link add  --url https://www.google.com
    manage.py link add  --url https://www.google.com --user test1

Command: 
    link
Sub-command:
    list  | --user  List for user / list all
    add   | --user Add new link:   EMAIL  URL
    fetch-preview   Get preview
    delete
"""

from django.core.management.base import BaseCommand, CommandError
from weblink.models import find_user, Link, Category, User

class Command(BaseCommand):
    help = "Manage web links category. List, add/create, remove."

    def list_all(self, options):
        self.stdout.write("=PK=" + "\t===URL===" + "\t\t=FAV-LINK====")
        try:    
            user = User.objects.get(id=options['user'])
            q = Link.objects.filter(user=user).all()
            print(options['user'])
        except User.DoesNotExist:
            q = Link.objects.all()
        for l in q:
            self.stdout.write("%04d" % l.pk + "\t%s" % l.url + "\t%s" % l)

    def add_arguments(self, parser):
        """Arguments for this command: --delete"""
        parser.add_argument(
            "subcommand",
            nargs="+",
            type=str,
            choices=["list", "add", "delete", "fetch-preview"],
        )
        parser.add_argument("--user", nargs="?", type=str)
        parser.add_argument("--email", nargs="?", type=str)
        parser.add_argument("--url", nargs="?", type=str)
        parser.add_argument("--ids", nargs="?", type=str)

    def handle(self, *args, **options):
        cmd = options["subcommand"][0]
        if "list" == cmd:
            self.list_all(options)
        if "delete" == cmd:
            link_ids = options["pks"].split(",")
            for id in link_ids:
                try:
                    link = Link.objects.get(pk=id)
                    link.delete()
                    self.stdout.write(
                        self.style.SUCCESS(
                            'Successfully delete link for id="%s" user="%s" url="%s"'
                            % (id, link.user.pk, link.url_text)
                        )
                    )
                except:
                    self.stdout.write(
                        self.style.ERROR('Fail to delete link id="%s" ' % (id,))
                    )
        if "add" == cmd:
            u = find_user(id=options['user'], name=options['user'], email=options['email'])
            the_url = options["url"]
            cat, created = Category.objects.get_or_create(
                name="-"
            )  # the default category for everyone
            if not options["url"]:
                the_url = input("URL: ")
            if not options['user']:
                u = User.objects.first()
            l = Link.set_favorite(user=u, category=cat, url=the_url)
            self.stdout.write(
                self.style.SUCCESS(
                    'Successfully add favorite link for user="%s" url="%s"'
                    % (u, the_url)
                )
            )
        if "fetch-preview" == cmd:
            link_ids = options["ids"].split(",")
            for id in link_ids:
                try:
                    link = Link.objects.get(pk=id)
                    link.fetch_preview()
                    self.stdout.write(
                        self.style.SUCCESS(
                            'Successfully fetch content preview for id="%s" user="%s" url="%s"'
                            % (id, link.user.pk, link.url_text)
                        )
                    )
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(
                            'Fail get preview for link id="%s" : %s' % (id, e)
                        )
                    )
