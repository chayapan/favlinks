"""
python manage.py category add --name CAT1
python manage.py category delete --name CAT1
python manage.py category list

"""

from django.core.management.base import BaseCommand, CommandError
from weblink.models import Category

class Command(BaseCommand):
    help = "Manage web links category. List, add/create, remove."

    def add_arguments(self, parser):
        """Arguments for this command: --delete"""
        parser.add_argument("subcommand", nargs="+", type=str, choices=['list','add','delete'])
        parser.add_argument(
                    "--delete",
                    action="store_true",
                    help="Delete poll instead of closing it",
                )
        parser.add_argument(
                    "--name",
                    help="String value of the category",
                )
        parser.add_argument(
                    "--pk",
                    help="Categoriy ID  in the system",
                )

        parser.add_argument("categories", nargs="?", type=str)
    
    def handle(self, *args, **options):
        if options['delete']:
            self.stdout.write(self.style.SUCCESS('Delete'))
        cmd = options['subcommand'][0]
        if 'add' == cmd:
            category = options['name']
            c = Category.objects.create(name=category)
            self.stdout.write("%04d" % c.pk + "\t%s" % c.name)
        if 'delete' == cmd:
            category, pk = options.get('name','-'), options.get('pk',0)
            if pk:
                q = Category.objects.filter(pk=pk)
                for c in q:
                    self.stdout.write("%04d" % c.pk + "\t%s" % c.name)
                    c.delete()
            elif category:
                self.stdout.write("Deleting %s" % category)
                q = Category.objects.filter(name=category)
                for c in q:
                    self.stdout.write("%04d" % c.pk + "\t%s" % c.name)
                    c.delete()
        elif 'list' == cmd:
            q = Category.objects.all()
            for c in q:
                self.stdout.write("%04d" % c.pk + "\t%s" % c.name)
        elif 'describe' == cmd:
            for cat in options["categories"]:
                try:
                    cat = Category.objects.get(name=cat)
                except Category.DoesNotExist:
                    raise CommandError('Category "%s" does not exist' % cat)
                poll.opened = False
                poll.save()

                self.stdout.write(
                    self.style.SUCCESS('Successfully closed poll "%s"' % poll_id)
                )