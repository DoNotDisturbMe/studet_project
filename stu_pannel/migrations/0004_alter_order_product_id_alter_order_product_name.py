# Generated by Django 4.2.2 on 2023-07-25 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stu_pannel', '0003_order_product_id_order_product_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='product_id',
            field=models.CharField(max_length=600),
        ),
        migrations.AlterField(
            model_name='order',
            name='product_name',
            field=models.CharField(max_length=600),
        ),
    ]
