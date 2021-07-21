from django import forms
from django.shortcuts import get_object_or_404, redirect, render
from .models import Time
from .forms import TimeForm, TimesModel
from django.contrib import messages
import sqlite3
from sqlite3 import Error

# Create your views here.
def index(request):
    serieA = Time.objects.filter(serie='A')
    serieB = Time.objects.filter(serie='B')

    context = {
        'serieA': serieA,
        'serieB': serieB
    }
    return render(request,'index.html', context)

def confirm_delete(request,id):
    # def conexao():
    #     caminho = r"C:\Users\leonn\OneDrive\Área de Trabalho\Documents\Django\Projeto2\db.sqlite3"
    #     con = None
    #     try:
    #         con = sqlite3.connect(caminho)
    #     except Error as ex:
    #         print(ex)
    #     return con
    # vcon = conexao()
    

    # def deletar(id):
    #     conexao = vcon
    #     sql = "delete from app_time where nome = '"+ str(rem)+ "'"
    #     try:
    #         c = conexao.cursor()
    #         c.execute(sql)
    #         conexao.commit()
    #     except Error as ex:
    #         print(ex)

    timeDelete = get_object_or_404(Time, pk=id)
    if str(request.method) == 'POST':
        timeDelete.delete()
        return redirect('/')
        
    #deletar("Flamengo")
    
    return render(request,'confirm_delete.html')
    

def cadastro(request):
    form = TimesModel(request.POST or None)
    if str(request.method) == 'POST' :
        if form.is_valid():
            form.save()
            messages.success(request, 'Cadastro feito')
            form = TimeForm()
  

    context = {
        'form' : form
    }
    return render(request,'cadastro.html', context)
