from django.db import models
from django.db.models import signals
from django.template.defaultfilters import slugify

# Create your models here.

class Time(models.Model):
    sigla = models.CharField('Sigla', max_length=5)
    nome = models.CharField('Nome', max_length=100)
    serie = models.CharField('Serie',max_length=1)
    slug = models.SlugField('Slug',max_length=100, blank=True, editable=False)

    def __str__(self):
        return self.nome
    
def Time_pre_save(signal, instance, sender, **kwargs):
    instance.slug = slugify(instance.nome)

    class Meta:
        model = Time
signals.pre_save.connect(Time_pre_save, sender = Time)
