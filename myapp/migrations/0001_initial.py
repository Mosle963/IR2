# Generated by Django 5.1.4 on 2024-12-05 11:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField()),
                ('answer', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Term',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('term', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='TermDocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight', models.DecimalField(decimal_places=3, max_digits=6)),
                ('document', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.document')),
                ('term', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.term')),
            ],
        ),
    ]
