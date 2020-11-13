# Generated by Django 3.1.2 on 2020-11-06 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rule',
            name='r_starttime',
        ),
        migrations.AlterField(
            model_name='rule',
            name='dst_ip',
            field=models.CharField(default=None, max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='rule',
            name='feature',
            field=models.CharField(default=None, max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='rule',
            name='max_dst_port',
            field=models.CharField(default=None, max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='rule',
            name='max_src_port',
            field=models.CharField(default=None, max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='rule',
            name='min_dst_port',
            field=models.CharField(default=None, max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='rule',
            name='min_src_port',
            field=models.CharField(default=None, max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='rule',
            name='package_type',
            field=models.IntegerField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='rule',
            name='r_description',
            field=models.TextField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='rule',
            name='r_type',
            field=models.IntegerField(choices=[(0, 'default'), (1, 'ip'), (2, 'protocal'), (3, 'feature')], default=None, null=True),
        ),
        migrations.AlterField(
            model_name='rule',
            name='src_ip',
            field=models.CharField(default=None, max_length=64, null=True),
        ),
    ]