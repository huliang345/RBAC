# Generated by Django 2.2.2 on 2019-09-07 03:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0002_auto_20190907_1117'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='action',
            options={'verbose_name_plural': '操作表'},
        ),
        migrations.AddField(
            model_name='action',
            name='code',
            field=models.CharField(default=1, max_length=32),
            preserve_default=False,
        ),
    ]
