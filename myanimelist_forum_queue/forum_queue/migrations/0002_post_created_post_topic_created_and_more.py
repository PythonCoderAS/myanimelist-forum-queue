# Generated by Django 4.0 on 2022-01-02 03:59

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('forum_queue', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='post',
            name='topic_created',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddConstraint(
            model_name='post',
            constraint=models.CheckConstraint(check=models.Q(models.Q(('topic_created__isnull', True), ('topic_id__isnull', True)), models.Q(('topic_created__isnull', False), ('topic_id__isnull', False)), _connector='OR'), name='topic_created_must_exist_if_topic_id_exists'),
        ),
    ]
