# Generated by Django 4.1.7 on 2023-03-03 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Post', '0003_alter_topic_customer_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecordLike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(verbose_name='record uuid')),
                ('customer_id', models.IntegerField(verbose_name='record customer_id')),
            ],
        ),
    ]
