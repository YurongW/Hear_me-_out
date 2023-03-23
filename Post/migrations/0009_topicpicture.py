# Generated by Django 4.1.7 on 2023-03-03 23:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Post', '0008_topic_num_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='TopicPicture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField()),
                ('topic_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Post.topic')),
            ],
        ),
    ]
