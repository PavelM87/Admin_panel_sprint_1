# Generated by Django 3.2.8 on 2021-10-14 14:31

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Filmwork',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('description', models.TextField(blank=True, null=True, verbose_name='description')),
                ('creation_date', models.DateField(blank=True, null=True, verbose_name='creation date')),
                ('certificate', models.TextField(blank=True, null=True, verbose_name='certificate')),
                ('file_path', models.FileField(blank=True, null=True, upload_to='film_works/', verbose_name='file')),
                ('rating', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='rating')),
                ('type', models.CharField(choices=[('movie', 'movie'), ('tv_show', 'TV Show')], max_length=20, verbose_name='type')),
            ],
            options={
                'verbose_name': 'filmwork',
                'verbose_name_plural': 'filmworks',
                'db_table': '"content"."film_work"',
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, verbose_name='title')),
                ('description', models.TextField(blank=True, null=True, verbose_name='description')),
            ],
            options={
                'verbose_name': 'genre',
                'verbose_name_plural': 'genres',
                'db_table': '"content"."genre"',
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('full_name', models.CharField(max_length=255, verbose_name='full name')),
                ('birth_date', models.DateField(blank=True, null=True, verbose_name='birth date')),
            ],
            options={
                'verbose_name': 'person',
                'verbose_name_plural': 'persons',
                'db_table': '"content"."person"',
            },
        ),
        migrations.CreateModel(
            name='PersonFilmWork',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('role', models.CharField(max_length=255, verbose_name='role')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('film_work', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.filmwork')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.person')),
            ],
            options={
                'db_table': '"content"."person_film_work"',
            },
        ),
        migrations.CreateModel(
            name='FilmworkGenre',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('film_work', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.filmwork')),
                ('genre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.genre')),
            ],
            options={
                'db_table': '"content"."genre_film_work"',
            },
        ),
        migrations.AddField(
            model_name='filmwork',
            name='genres',
            field=models.ManyToManyField(through='movies.FilmworkGenre', to='movies.Genre'),
        ),
        migrations.AddIndex(
            model_name='personfilmwork',
            index=models.Index(fields=['film_work', 'person', 'role'], name='film_work_person_role'),
        ),
        migrations.AlterUniqueTogether(
            name='personfilmwork',
            unique_together={('film_work', 'person', 'role')},
        ),
        migrations.AddIndex(
            model_name='filmworkgenre',
            index=models.Index(fields=['film_work', 'genre'], name='film_work_genre'),
        ),
    ]
