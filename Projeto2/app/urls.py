from app.views import index, cadastro, confirm_delete
from django.urls import path



urlpatterns = [
    path('',index),
    path('cadastro',cadastro, name='cadastro'),
    path('confirm_delete/<int:id>', confirm_delete, name="confirme")
]