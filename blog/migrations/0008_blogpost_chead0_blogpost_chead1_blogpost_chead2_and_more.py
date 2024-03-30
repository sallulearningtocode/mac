# Generated by Django 5.0.2 on 2024-03-24 06:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='chead0',
            field=models.CharField(default='', max_length=5000),
        ),
        migrations.AddField(
            model_name='blogpost',
            name='chead1',
            field=models.CharField(default='', max_length=5000),
        ),
        migrations.AddField(
            model_name='blogpost',
            name='chead2',
            field=models.CharField(default='', max_length=5000),
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='thumbnail',
            field=models.ImageField(default='', upload_to='shop/images'),
        ),
    ]