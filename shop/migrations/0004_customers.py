# Generated by Django 3.2.7 on 2021-10-06 10:59

import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('shop', '0003_auto_20211002_1657'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customers',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='auth.user')),
                ('address', models.CharField(max_length=255, verbose_name='Адрес')),
                ('phone', models.CharField(max_length=30, verbose_name='Телефон')),
            ],
            options={
                'verbose_name': 'Покупатель',
                'verbose_name_plural': 'Покупатели',
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
