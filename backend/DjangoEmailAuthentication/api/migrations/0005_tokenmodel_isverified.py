# Generated by Django 5.1b1 on 2024-07-14 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_alter_customuser_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='tokenmodel',
            name='isVerified',
            field=models.BooleanField(default=False),
        ),
    ]
