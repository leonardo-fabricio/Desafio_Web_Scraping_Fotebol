from django.db import models

# Create your models here.

class Time(models.Model):
    sigla = models.CharField('Sigla', max_length=5)
    nome = models.CharField('Nome', max_length=100)
    escudo = models.BinaryField('escudo')
    serie = models.CharField('Serie',max_length=1)

    def __str__(self):
        return self.sigla