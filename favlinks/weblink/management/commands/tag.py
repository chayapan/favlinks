"""
Admin command for Tag entities.

    python manage.py tag TEST FOOD

Command: 
    tag
Sub-command:
    list
    add     --tags TAG1 TAG2 TAG3
    delete
"""

from django.core.management.base import BaseCommand, CommandError
from weblink.models import Tag, add_tag, remove_tag

class Command(BaseCommand):
    help = "Manage link tags. List, add/create, remove."

    def add_arguments(self, parser):
        parser.add_argument("subcommand", nargs="+", type=str, choices=['list','add','delete'])
        parser.add_argument("--tags", nargs="+", type=str)
        parser.add_argument("--pk", nargs="?", type=str)

    def list_tags(self, options):
        table_data = []
        table_data.append(['PK','Tag'])
        q = Tag.objects.all()
        for t in q:
            row = [t.pk, t.value]
            table_data.append(row)    
        for row in table_data:
            self.stdout.write("{: >8} {: >20}".format(*row))
   
    def handle(self, *args, **options):
        cmd = options['subcommand'][0]
        if 'list' == cmd:
            self.list_tags(options)
        elif 'add' == cmd:
            # two choices: either space-separate or comma separate. Comma separate would be better actually...
            # ex. "['FOOD', 'TRAVEL', 'BLOG']"
            tags = options['tags']
            try:
                tag_list = eval(str(tags))  # TODO: check security req.
                for v in tag_list:
                    t = Tag.objects.create(value=v)
                    self.stdout.write("%04d" % t.pk + "\t%s" % t.value)
            except Exception as e:
                raise CommandError(e +  "%s" % tags)
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