from django.contrib import admin

# Register your models here.
from .models import Time

class TimeAdmin(admin.ModelAdmin):
    list_display = ('nome','sigla','serie','escudo')

admin.site.register(Time,TimeAdmin)