# Generated by Django 4.1.1 on 2023-02-16 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MainApp', '0009_alter_snippet_creation_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='snippet',
            name='voted',
            field=models.TextField(default='', max_length=5000),
        ),
    ]