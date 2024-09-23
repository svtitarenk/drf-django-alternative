from django.db import models

NULLABLE = {"null": True, "blank": True}


class Breed(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название породы", help_text='Укажите название породы',
                            **NULLABLE)
    description = models.TextField(**NULLABLE, verbose_name="Описание породы", help_text='Укажите описание породы')

    class Meta:
        verbose_name = "Порода"
        verbose_name_plural = "Породы"


class Dog(models.Model):
    name = models.CharField(max_length=100, verbose_name="Кличка", help_text='Укажите кличку собаки', **NULLABLE)
    breed = models.ForeignKey(
        Breed,
        verbose_name="Порода",
        help_text='Выберите породу',
        on_delete=models.SET_NULL,
        **NULLABLE
    )
    photo = models.ImageField(upload_to='dogs/photo', verbose_name="Фото", help_text='Загрузите фото собаки',
                              **NULLABLE)
    date_born = models.DateField(verbose_name='Дата рождения', help_text='Укажите дату рождения', **NULLABLE)

    class Meta:
        verbose_name = "Собака"
        verbose_name_plural = "Собаки"
