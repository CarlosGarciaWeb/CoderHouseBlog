# Generated by Django 4.0.4 on 2022-07-04 19:17

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BlogPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=30, unique=True)),
                ('title', models.CharField(max_length=65, unique=True)),
                ('blog_date', models.DateField()),
                ('blog_meta', models.CharField(max_length=300)),
                ('blog_content', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('topic_tag', models.CharField(max_length=100)),
            ],
        ),
    ]
