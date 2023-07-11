# Generated by Django 4.2.2 on 2023-07-11 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stu_pannel', '0004_alter_product_product_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='extendeduser',
            old_name='WhatsApp',
            new_name='district',
        ),
        migrations.RenameField(
            model_name='extendeduser',
            old_name='user',
            new_name='user_id',
        ),
        migrations.RenameField(
            model_name='extendeduser',
            old_name='First_name',
            new_name='user_name',
        ),
        migrations.RemoveField(
            model_name='extendeduser',
            name='Gender',
        ),
        migrations.RemoveField(
            model_name='extendeduser',
            name='Last_name',
        ),
        migrations.AddField(
            model_name='extendeduser',
            name='photo_user',
            field=models.ImageField(default=2, upload_to='user_img'),
            preserve_default=False,
        ),
    ]
