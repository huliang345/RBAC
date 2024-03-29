# Generated by Django 2.2.2 on 2019-09-07 06:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0003_auto_20190907_1126'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='permission2action',
            options={'verbose_name_plural': '权限表'},
        ),
        migrations.AlterModelOptions(
            name='permission2action2role',
            options={'verbose_name_plural': '角色分配权限'},
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.CharField(max_length=32)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='p', to='app01.Menu')),
            ],
        ),
    ]
