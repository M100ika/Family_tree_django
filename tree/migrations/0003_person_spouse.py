# Generated by Django 5.1.7 on 2025-03-24 07:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tree', '0002_alter_person_options_person_address_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='spouse',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='partner', to='tree.person'),
        ),
    ]
