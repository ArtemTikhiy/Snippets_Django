# Generated by Django 4.1.1 on 2023-02-16 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MainApp', '0012_remove_snippet_voted_down_remove_snippet_voted_up'),
    ]

    operations = [
        migrations.AddField(
            model_name='snippet',
            name='voted',
            field=models.TextField(default='', max_length=5000),
        ),
    ]
