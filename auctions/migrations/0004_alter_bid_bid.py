# Generated by Django 4.1.3 on 2022-12-23 05:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_remove_comment_listing_comments_comment_listing'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bid',
            name='bid',
            field=models.FloatField(),
        ),
    ]
