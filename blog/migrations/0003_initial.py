# Generated by Django 5.0.2 on 2024-03-24 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('blog', '0002_delete_product'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bogpost',
            fields=[
                ('post_id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=50)),
                ('head0', models.CharField(default='', max_length=500)),
                ('pub_date', models.DateField()),
                ('thumbnail', models.ImageField(default='', upload_to='shop/images')),
            ],
        ),
    ]
