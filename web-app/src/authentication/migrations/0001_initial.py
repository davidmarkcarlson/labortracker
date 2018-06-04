# Generated by Django 2.0.3 on 2018-04-15 20:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(max_length=255, unique=True)),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, null=True)),
                ('gravida', models.IntegerField()),
                ('para', models.IntegerField()),
                ('date_of_admission', models.DateField(auto_now_add=True)),
                ('time_of_admission', models.TimeField(auto_now_add=True)),
                ('ruptured_membrane_time', models.TimeField(null=True)),
                ('vaginal_births', models.IntegerField()),
                ('age', models.PositiveIntegerField()),
                ('height', models.PositiveIntegerField()),
                ('weight', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Practitioner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='patient',
            name='practitioner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.Practitioner'),
        ),
        migrations.AddField(
            model_name='user',
            name='patient',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='authentication.Patient'),
        ),
        migrations.AddField(
            model_name='user',
            name='practitioner',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='authentication.Practitioner'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]