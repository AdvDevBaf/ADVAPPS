# Generated by Django 2.1.1 on 2019-09-27 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BafosApp', '0007_auto_20190927_1216'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mtemplate',
            name='status',
            field=models.CharField(choices=[('n', 'No'), ('s', 'Send')], default='n', max_length=1),
        ),
    ]
