from django.conf.urls import url
from django.urls.conf import re_path
from app.views import index, cadastro, confirm_delete, webscraping, estatisticas
from django.urls import path
from django.views.generic.base import RedirectView
from django.contrib.staticfiles.storage import staticfiles_storage

favicon_view = RedirectView.as_view(url='/static/img/home.png', permanent=True)

urlpatterns = [
    path('',index),
    path('cadastro',cadastro, name='cadastro'),
    path('confirm_delete/<int:id>', confirm_delete, name="confirme"),
    path('webscraping', webscraping, name="webscraping"),
    path('estatisticas/<str:sigla>',estatisticas,name="estatisticas"),
    re_path(r'^favicon\.ico$', favicon_view),
]