# Generated by Django 4.1.1 on 2023-02-07 21:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MainApp', '0002_snippet_user_alter_snippet_lang'),
    ]

    operations = [
        migrations.AddField(
            model_name='snippet',
            name='privacy',
            field=models.CharField(choices=[('Публичный', 'Публичный'), ('Частный', 'Частный')], default='Публичный', max_length=10),
            preserve_default=False,
        ),
    ]