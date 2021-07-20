from app.views import index, cadastro
from django.urls import path



urlpatterns = [
    path('',index),
    path('cadastro',cadastro, name='cadastro'),
]