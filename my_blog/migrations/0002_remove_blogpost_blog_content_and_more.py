# Generated by Django 4.0.4 on 2022-07-04 21:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('my_blog', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogpost',
            name='blog_content',
        ),
        migrations.RemoveField(
            model_name='blogpost',
            name='blog_date',
        ),
        migrations.RemoveField(
            model_name='blogpost',
            name='blog_meta',
        ),
        migrations.RemoveField(
            model_name='blogpost',
            name='title',
        ),
        migrations.RemoveField(
            model_name='blogpost',
            name='topic_tag',
        ),
        migrations.RemoveField(
            model_name='blogpost',
            name='user_name',
        ),
    ]
