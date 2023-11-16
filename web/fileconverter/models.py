from django.db import models

from users.models import User


class ConvertedModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    original_file = models.FileField(upload_to='original_files', verbose_name='Исходный файл')
    converted_file = models.FileField(upload_to='converted_files',verbose_name='Сконвертированный файл', blank=True, null=True)
    converted_filename = models.CharField(max_length=255, verbose_name='Имя сконвертированного файла', blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return f'{self.user.name} - {self.converted_filename}'

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Сконвертированные файлы'
        verbose_name_plural = 'Сконвертированный файл'
