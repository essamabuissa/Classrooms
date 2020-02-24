# Generated by Django 2.1.5 on 2020-02-22 13:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0003_classroom_teacher'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('dob', models.DateField()),
                ('gender', models.CharField(max_length=50)),
                ('exam_grade', models.DecimalField(decimal_places=2, max_digits=5)),
                ('classroom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='classes.Classroom')),
            ],
        ),
    ]