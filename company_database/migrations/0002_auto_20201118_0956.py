# Generated by Django 3.1.1 on 2020-11-18 01:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('company_database', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='companybasicinformation',
            options={'ordering': ('id', 'credit_code')},
        ),
    ]
