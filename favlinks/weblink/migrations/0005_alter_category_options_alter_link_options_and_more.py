# Generated by Django 5.0 on 2024-04-08 08:23

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("weblink", "0004_alter_category_name_alter_tag_value"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="category",
            options={
                "verbose_name": "Link Category",
                "verbose_name_plural": "Link Categories",
            },
        ),
        migrations.AlterModelOptions(
            name="link",
            options={"verbose_name": "Link", "verbose_name_plural": "Links"},
        ),
        migrations.AlterModelOptions(
            name="tag",
            options={"verbose_name": "Tag", "verbose_name_plural": "Tags"},
        ),
        migrations.AlterModelOptions(
            name="url",
            options={"verbose_name": "URL", "verbose_name_plural": "URLs"},
        ),
        migrations.AddField(
            model_name="link",
            name="tags",
            field=models.ManyToManyField(null=True, to="weblink.tag"),
        ),
        migrations.AlterField(
            model_name="link",
            name="category",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="links",
                to="weblink.category",
            ),
        ),
        migrations.AlterField(
            model_name="link",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="favorite_links",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="url",
            name="raw_url",
            field=models.CharField(max_length=2000, unique=True),
        ),
    ]
