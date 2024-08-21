# Generated by Django 5.1 on 2024-08-21 05:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FinancialData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('step', models.IntegerField()),
                ('customer', models.CharField(max_length=255)),
                ('age', models.IntegerField()),
                ('gender', models.CharField(max_length=10)),
                ('zipcodeOri', models.CharField(max_length=10)),
                ('merchant', models.CharField(max_length=255)),
                ('zipMerchant', models.CharField(max_length=10)),
                ('category', models.CharField(max_length=255)),
                ('amount', models.FloatField()),
                ('fraud', models.IntegerField()),
            ],
            options={
                'db_table': 'financial_data',
            },
        ),
    ]
