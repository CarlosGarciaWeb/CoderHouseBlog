# Generated by Django 4.0.4 on 2022-07-20 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_blog', '0020_alter_comments_post_alter_comments_user_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='comment',
            field=models.TextField(null=True),
        ),
    ]
