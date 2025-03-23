from django.db import models
from django_cleanup import cleanup


class Person(models.Model):
    GENDER_CHOICES = [
        ('M', 'Мужской'),
        ('F', 'Женский'),
        ('O', 'Другой'),
    ]

    first_name = models.CharField('Имя', max_length=100)
    last_name = models.CharField('Фамилия', max_length=100)
    middle_name = models.CharField('Отчество', max_length=100, blank=True, default='')
    gender = models.CharField('Пол', max_length=1, choices=GENDER_CHOICES, default='O')
    date_of_birth = models.DateField('Дата рождения')
    place_of_birth = models.CharField('Место рождения', max_length=200, blank=True, null=True)
    date_of_death = models.DateField('Дата смерти', null=True, blank=True)
    place_of_death = models.CharField('Место смерти', max_length=200, blank=True)
    biography = models.TextField('Биография', blank=True, default='')
    photo = models.ImageField('Фото', upload_to='persons/', blank=True, null=True)
    personal_page = models.URLField('Личная страница', max_length=200, blank=True)
    email = models.EmailField('Email', blank=True)
    phone = models.CharField('Телефон', max_length=20, blank=True)
    address = models.TextField('Адрес', blank=True)
    occupation = models.CharField('Род занятий', max_length=200, blank=True)
    education = models.TextField('Образование', blank=True)
    parents = models.ManyToManyField('self', related_name='children', symmetrical=False, blank=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

    class Meta:
        verbose_name = 'Человек'
        verbose_name_plural = 'Люди'
        ordering = ['last_name', 'first_name'] 