# Generated by Django 4.0.4 on 2022-07-18 02:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_blog', '0013_alter_post_user_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='header_image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
