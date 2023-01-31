# Generated by Django 4.1.3 on 2022-12-23 05:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_alter_bid_bid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='listing_comments',
        ),
        migrations.AddField(
            model_name='comment',
            name='listing',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='listing_comments', to='auctions.listing'),
        ),
    ]
