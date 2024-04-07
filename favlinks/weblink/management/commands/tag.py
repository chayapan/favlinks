"""
Admin command for Tag entities.

    python manage.py tag TEST FOOD

Command: 
    tag
Sub-command:
    list-all

"""

from django.core.management.base import BaseCommand, CommandError
from weblink.models import Tag

class Command(BaseCommand):
    help = "Manage link tags. List, add/create, remove."

    def add_arguments(self, parser):
        """Arguments for this command: --delete"""
        parser.add_argument("subcommand", nargs="+", type=str, choices=['list','add','delete'])
        parser.add_argument("--tags", nargs="+", type=str)
        parser.add_argument("--pk", nargs="?", type=str)

    def handle(self, *args, **options):
        cmd = options['subcommand'][0]
        if 'list' == cmd:
            self.stdout.write("=PK=" + "\t=TAG====")
            q = Tag.objects.all()
            for t in q:
                self.stdout.write("%04d" % t.pk + "\t%s" % t.value)
        elif 'add' == cmd:
            tags = options['tags']
            try:
                # two choices: either space-separate or comma separate. Comma separate would be better actually...
                # ex. "['FOOD', 'TRAVEL', 'BLOG']"
                tag_list = eval(str(tags))  # TODO: check security req.
            except Exception as e:
                raise CommandError(e +  "%s" % tags)
            for v in tag_list:
                t = Tag.objects.create(value=v)
                self.stdout.write("%04d" % t.pk + "\t%s" % t.value)
        elif 'delete' == cmd:
            if 'pk' in options:
                pk_list = options['pk'].split(',')
                q = Tag.objects.filter(pk__in=pk_list)
                if q.count() == 0:
                    raise CommandError('Tags with these PKs not found: %s' % pk_list)
                q.delete()
                self.stdout.write(self.style.SUCCESS('Deleted tags: pk=%s' % (pk_list,)))
            else:
                tags = list(options["tags"])
                for t in tags:
                    q = Tag.objects.filter(value=t)
                    q.delete()
                    self.stdout.write(self.style.SUCCESS('Deleted tag: "%s"' % t))