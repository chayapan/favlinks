"""
Admin command for account registration and management.

Command: 
    register
Sub-command:
    new-account
    list-all

See 
BaseCommand docs
https://docs.djangoproject.com/en/5.0/howto/custom-management-commands/#ref-basecommand-subclasses
ArgParser
https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser

    python manage.py register user1@example.com  Password1
    python manage.py register new-account --email test@example.com

"""

from django.core.management.base import BaseCommand, CommandError
from weblink.models import Category, User

class Command(BaseCommand):
    help = "Manage link tags. List, add/create, remove."

    def add_arguments(self, parser):
        """Arguments for this command: --delete"""
        parser.add_argument("subcommand", type=str, choices=['list', 'new', 'delete'])
        parser.add_argument("--email", help="email")
        parser.add_argument("--username", help="username")

    def handle(self, *args, **options):
        cmd = options["subcommand"]
        self.stdout.write(
            self.style.SUCCESS('Manage User Accounts\n%s:' % cmd)
        )
        if 'new-account' == cmd:
            self.stdout.write("Creating new account")
            email, username = options['email'], options.get('username', '-')
            try:
                u = User.objects.create(email=email, username=username)
                self.stdout.write("%02d" % u.pk + " "*6 + "%20s" % u.email)
            except Exception as e:
                self.stdout.write(self.style.ERROR(str(e) + "\nemail=%s, username=%s" % (email, username)))
        elif 'delete' == cmd:
            self.stdout.write("Deleting user account(s)")
            email, username = options['email'], options.get('username', '-')
            try:
                q = User.objects.filter(email=email)
                if q.count() == 0:
                    raise CommandError('User with email "%s" does not exist' % email)
                for u in q:
                    self.stdout.write("%02d" % u.pk + " "*6 + "%20s" % u.email)
                    u.delete()
            except Exception as e:
                self.stdout.write(self.style.ERROR(str(e) + "\nemail=%s, username=%s" % (email, username)))
        elif 'list' == cmd:
            self.stdout.write("Listing all accounts")
            self.stdout.write("=PK=" + "\t=EMAIL=\t" + "\t=USERNAME=")
            for u in User.objects.all():
                self.stdout.write(" %03d" % u.pk + "\t%20s" % u.email + "\t%10s" % u.username)

