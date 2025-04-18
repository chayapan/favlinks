"""
Admin command for account registration and management.

Command:
    list
    delete
    register
Sub-command:
    new-account
    list-all

    python manage.py register user1@example.com  Password1
    python manage.py register new-account --email test@example.com

See
BaseCommand docs
https://docs.djangoproject.com/en/5.0/howto/custom-management-commands/#ref-basecommand-subclasses
ArgParser
https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser
    
"""

from django.core.management.base import BaseCommand, CommandError
from weblink.models import Category, User

class Command(BaseCommand):
    help = "Manage link tags. List, add/create, remove."

    def add_arguments(self, parser):
        """Arguments for this command: --delete"""
        parser.add_argument("subcommand", type=str, choices=['list', 'register', 'delete'])
        parser.add_argument("--email", help="email")
        parser.add_argument("--username", help="username")

    def list_users(self, options):
        table_data = []
        table_data.append(['ID','Username','email', 'link count'])
        q = User.objects.all()
        self.stdout.write("Listing all accounts")
        for u in q:
            row = [u.pk, u.username,  u.email, u.favorite_links.count()]
            table_data.append(row)
        for row in table_data:
            self.stdout.write("{: >4} {: >10} {: >20} {: >10}".format(*row))

    def add_user(self, options):
        self.stdout.write("Creating new account")
        email, username = options['email'], options.get('username', '-')
        if not username:
            username = input("username: ")
        if not email:
            email = input("email: ")
        try:
            u = User.objects.create(email=email, username=username)
            u.set_password(u.id) # generate password
            self.stdout.write("%02d" % u.pk + " "*6 + "%20s" % u.email)
        except Exception as e:
            self.stdout.write(self.style.ERROR(str(e) + "\nemail=%s, username=%s" % (email, username)))

    def delete_user(self, options):
        self.stdout.write("Deleting user account(s)")
        username = options.get('username', None)
        try:
            q = User.objects.filter(username=username)
            if q.count() == 0:
                raise CommandError('User with username "%s" does not exist' % (username, ))
            for u in q:
                self.stdout.write("%02d" % u.pk + " "*6 + "%20s" % u.username + "... DELETED")
                u.delete()
        except Exception as e:
            self.stdout.write(self.style.ERROR(str(e) + "\nusername=%s" % (username,)))

    def handle(self, *args, **options):
        cmd = options["subcommand"]
        self.stdout.write(
            self.style.SUCCESS('Manage User Accounts: %s' % cmd)
        )
        if 'register' == cmd:
            self.add_user(options)
        elif 'delete' == cmd:
            self.delete_user(options)
        elif 'list' == cmd:
            self.list_users(options)
