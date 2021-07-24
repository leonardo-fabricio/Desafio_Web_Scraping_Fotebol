from os import system
from django import forms
from django.forms.widgets import Select
from django.shortcuts import get_object_or_404, redirect, render
from .models import Time
from .forms import TimeForm, TimesModel
from django.contrib import messages
import sqlite3
from sqlite3 import Error
from selenium import webdriver
from time import sleep
from datetime import datetime
from selenium.webdriver.chrome.options import Options

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

def webscraping(request):
    def conexao():
        caminho = r"C:\Users\leonn\OneDrive\Área de Trabalho\Documents\Django\Projeto2\db.sqlite3"
        con = None
        try:
            con = sqlite3.connect(caminho)
        except Error as ex:
            print(ex)
        return con
    vcon = conexao()
    def inserir(timeA,timeB,placar, rodada):
        conexao = vcon
        sql = r"INSERT INTO jogos (timeA,timeB,placar,rodada) VALUES('"+str(timeA)+"','"+str(timeB)+"','"+str(placar)+"','"+str(rodada)+"')"
        try:
            c = conexao.cursor()
            c.execute(sql)
            conexao.commit()
        except Error as ex:
            print(ex)
    
    # system.setProperty("webdriver.chrome.driver", r"C:\Users\leonn\OneDrive\Área de Trabalho\Documents\Django\Projeto2\app\chromedriver.exe")
    def scraping():
        options = Options()
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('-enable-webgl')
        options.add_argument('--no-sandbox')
        url = "https://ge.globo.com/futebol/brasileirao-serie-a/"
        driver = webdriver.Chrome(chrome_options= options, executable_path= r'C:\Users\leonn\OneDrive\Área de Trabalho\Documents\Django\Projeto2\app\chromedriver.exe')
        driver.get(url)
        driver.refresh()
        sleep(10)
        lista1 = ['1','2','3','4','5','6','7','8','9','10']

        for x in lista1:
            rodada = driver.find_element_by_xpath('//*[@id="classificacao__wrapper"]/section/nav/span[2]')
            timeA = driver.find_element_by_xpath('//*[@id="classificacao__wrapper"]/section/ul/li['+x+']/div/div/div/div[2]/div[1]/span[1]')
            timeB = driver.find_element_by_xpath('//*[@id="classificacao__wrapper"]/section/ul/li['+x+']/div/div/div/div[2]/div[3]/span[1]')
            placar = driver.find_element_by_xpath('//*[@id="classificacao__wrapper"]/section/ul/li['+x+']/div/div/div/div[2]/div[2]')
            #inserir(timeA.text,timeB.text,placar.text,rodada.text)
        driver.find_element_by_xpath('//*[@id="classificacao__wrapper"]/section/nav/span[1]').click()
        for x in range(12):
            sleep(30)
            for x in lista1:
                rodada = driver.find_element_by_xpath('//*[@id="classificacao__wrapper"]/section/nav/span[2]')
                timeA = driver.find_element_by_xpath('//*[@id="classificacao__wrapper"]/section/ul/li['+x+']/div/a/div[1]/div[2]/div[1]/span[1]')
                timeB = driver.find_element_by_xpath('//*[@id="classificacao__wrapper"]/section/ul/li['+x+']/div/a/div[1]/div[2]/div[3]/span[1]')
                placar = driver.find_element_by_xpath('//*[@id="classificacao__wrapper"]/section/ul/li['+x+']/div/a/div[1]/div[2]/div[2]')
                #inserir(timeA.text,timeB.text,placar.text,rodada.text)
            driver.find_element_by_xpath('//*[@id="classificacao__wrapper"]/section/nav/span[1]').click()
            
        driver.close()
        return redirect('/')

    scraping()
    return render(request,'index.html')
    