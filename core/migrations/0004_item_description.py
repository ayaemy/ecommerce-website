# Generated by Django 5.0.3 on 2024-04-02 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_item_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='description',
            field=models.TextField(default='this is a test description dhahufeu kjfwebh hfbherb'),
            preserve_default=False,
        ),
    ]