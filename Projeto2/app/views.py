from os import system
from django import forms
from django.forms.widgets import Select
from django.shortcuts import get_object_or_404, redirect, render
from .models import Time, jogos
from .forms import TimeForm, TimesModel
from django.contrib import messages
import sqlite3
from sqlite3 import Error
from selenium import webdriver
from time import sleep
from datetime import datetime
from selenium.webdriver.chrome.options import Options
import os

def conexao():
    caminho = r"C:\Users\leonn\OneDrive\Área de Trabalho\Desafio_Web_Scraping_Fotebol\Projeto2\db.sqlite3"
    con = None
    try:
        con = sqlite3.connect(caminho,check_same_thread=False)
    except Error as ex:
        print(ex)
    return con
vcon = conexao()

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

def estatisticas(request,sigla):
    # conexao = vcon
    # sql = r"SELECT * FROM jogos WHERE timeA = '"+str(sigla)+"' or timeB = '"+str(sigla)+"'"
    # lista = []
    # context = {}
    # for p in jogos.objects.raw ('SELECT * FROM jogos WHERE timeA = "'+str(sigla)+ '" or timeB = "'+str(sigla)+ '"'):
    #     lista.append(p)
        
    # for x in range(len(lista)):
    #     context["jogo"+str(x)] = lista[x]
    timea = jogos.objects.filter(timeA = sigla).exclude(timeB = sigla).order_by()
    context = {
        'timea':timea,
    }
    return render(request,'estatisticas.html',context)
    
def webscraping(request):
    def inserir(timeA,timeB,placar, rodada,serie):
        conexao = vcon
        sql = r"INSERT INTO app_jogos (timeA,timeB,placar,Serie,rodada) VALUES('"+str(timeA)+"','"+str(timeB)+"','"+str(placar)+"','"+str(serie)+"','"+str(rodada)+"')"
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
        driver = webdriver.Chrome(chrome_options= options, executable_path= r'C:\Users\leonn\OneDrive\Área de Trabalho\Desafio_Web_Scraping_Fotebol\Projeto2\app\chromedriver.exe')
        driver.get(url)
        #driver.refresh()
        sleep(5)
        #sleep(10)
        lista1 = ['1','2','3','4','5','6','7','8','9','10']
        totRodadas = 13
        for y in range(totRodadas):
            sleep(2)
            for x in lista1:
                rodada = driver.find_element_by_xpath('//*[@id="classificacao__wrapper"]/section/nav/span[2]')
                if(((rodada.text == '5ª RODADA') or (rodada.text == '4ª RODADA')  or (rodada.text == '2ª RODADA')) and x=='10'):
                    timeA = driver.find_element_by_xpath('//*[@id="classificacao__wrapper"]/section/ul/li['+x+']/div/div/div/div[2]/div[1]/span[1]')
                    timeB = driver.find_element_by_xpath('//*[@id="classificacao__wrapper"]/section/ul/li['+x+']/div/div/div/div[2]/div[3]/span[1]')
                    placar = driver.find_element_by_xpath('//*[@id="classificacao__wrapper"]/section/ul/li['+x+']/div/div/div/div[2]/div[2]')
                    inserir(timeA.text,timeB.text,placar.text,rodada.text,'A')
                else:
                    timeA = driver.find_element_by_xpath('//*[@id="classificacao__wrapper"]/section/ul/li['+x+']/div/a/div[1]/div[2]/div[1]/span[1]')
                    timeB = driver.find_element_by_xpath('//*[@id="classificacao__wrapper"]/section/ul/li['+x+']/div/a/div[1]/div[2]/div[3]/span[1]')
                    placar = driver.find_element_by_xpath('//*[@id="classificacao__wrapper"]/section/ul/li['+x+']/div/a/div[1]/div[2]/div[2]')
                    inserir(timeA.text,timeB.text,placar.text,rodada.text,'A')
            driver.find_element_by_xpath('//*[@id="classificacao__wrapper"]/section/nav/span[1]').click()
        driver.quit()
    
    def scrapingSerieB():
        
        options = Options()
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('-enable-webgl')
        options.add_argument('--no-sandbox')
        url = "https://ge.globo.com/futebol/brasileirao-serie-b/"
        driver = webdriver.Chrome(chrome_options= options, executable_path= r'C:\Users\leonn\OneDrive\Área de Trabalho\Desafio_Web_Scraping_Fotebol\Projeto2\app\chromedriver.exe')
        driver.get(url)
        driver.refresh()
        sleep(5)
        #sleep(10)
        lista1 = ['1','2','3','4','5','6','7','8','9','10']
        totRodadas = 14
        for y in range(totRodadas):
            sleep(2)
            for x in lista1:
                rodada = driver.find_element_by_xpath('//*[@id="classificacao__wrapper"]/section/nav/span[2]')
                if(((rodada.text == '6ª RODADA') or (rodada.text == '5ª RODADA') or (rodada.text == '4ª RODADA')) and x == '10'):
                    timeA = driver.find_element_by_xpath('//*[@id="classificacao__wrapper"]/section/ul/li['+x+']/div/div/div/div[2]/div[1]/span[1]')
                    timeB = driver.find_element_by_xpath('//*[@id="classificacao__wrapper"]/section/ul/li['+x+']/div/div/div/div[2]/div[3]/span[1]')
                    placar = driver.find_element_by_xpath('//*[@id="classificacao__wrapper"]/section/ul/li['+x+']/div/div/div/div[2]/div[2]')
                    inserir(timeA.text,timeB.text,placar.text,rodada.text,'B')
                else:
                    timeA = driver.find_element_by_xpath('//*[@id="classificacao__wrapper"]/section/ul/li['+x+']/div/a/div[1]/div[2]/div[1]/span[1]')
                    timeB = driver.find_element_by_xpath('//*[@id="classificacao__wrapper"]/section/ul/li['+x+']/div/a/div[1]/div[2]/div[3]/span[1]')
                    placar = driver.find_element_by_xpath('//*[@id="classificacao__wrapper"]/section/ul/li['+x+']/div/a/div[1]/div[2]/div[2]')
                    inserir(timeA.text,timeB.text,placar.text,rodada.text,'B')
            driver.find_element_by_xpath('//*[@id="classificacao__wrapper"]/section/nav/span[1]').click()
        driver.quit()
        
    def atualizar(url,serie):
        options = Options()
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('-enable-webgl')
        options.add_argument('--no-sandbox')
        
        driver = webdriver.Chrome(chrome_options= options, executable_path= r'C:\Users\leonn\OneDrive\Área de Trabalho\Desafio_Web_Scraping_Fotebol\Projeto2\app\chromedriver.exe')
        driver.get(url)
        driver.refresh()
        sleep(5)
        #sleep(10)
        lista1 = ['1','2','3','4','5','6','7','8','9','10']
        totRodadas = 13
        
        driver.find_element_by_xpath('//*[@id="classificacao__wrapper"]/section/nav/span[3]').click()
        
        for y in range(38-totRodadas):
            sleep(2)
            for x in lista1:
                rodada = driver.find_element_by_xpath('//*[@id="classificacao__wrapper"]/section/nav/span[2]')
                timeA = driver.find_element_by_xpath('//*[@id="classificacao__wrapper"]/section/ul/li['+x+']/div/div/div/div[2]/div[1]/span[1]')
                timeB = driver.find_element_by_xpath('//*[@id="classificacao__wrapper"]/section/ul/li['+x+']/div/div/div/div[2]/div[3]/span[1]')
                placar = driver.find_element_by_xpath('//*[@id="classificacao__wrapper"]/section/ul/li['+x+']/div/div/div/div[2]/div[2]')
                inserir(timeA.text,timeB.text,placar.text,rodada.text,serie)
            driver.find_element_by_xpath('//*[@id="classificacao__wrapper"]/section/nav/span[3]').click()
        driver.quit()
        
    scraping()
    # scrapingSerieB()
    # url = "https://ge.globo.com/futebol/brasileirao-serie-a/"
    # atualizar(url,"A")
    return render(request,'index.html')
    
    
     # rodada = driver.find_element_by_xpath('//*[@id="classificacao__wrapper"]/section/nav/span[2]')
            
            # timeA = driver.find_element_by_xpath('//*[@id="classificacao__wrapper"]/section/ul/li[1]/div/a/div[1]/div[2]/div[1]/span[1]')
            # timeB = driver.find_element_by_xpath('//*[@id="classificacao__wrapper"]/section/ul/li[1]/div/a/div[1]/div[2]/div[3]/span[1]')
            # placar = driver.find_element_by_xpath('//*[@id="classificacao__wrapper"]/section/ul/li[1]/div/a/div[1]/div[2]/div[2]')
            # # sleep(1)
            # timeA2 = driver.find_element_by_xpath('//*[@id="classificacao__wrapper"]/section/ul/li[2]/div/a/div[1]/div[2]/div[1]/span[1]')
            # timeB2 = driver.find_element_by_xpath('//*[@id="classificacao__wrapper"]/section/ul/li[2]/div/a/div[1]/div[2]/div[3]/span[1]')
            # placar2 = driver.find_element_by_xpath('//*[@id="classificacao__wrapper"]/section/ul/li[2]/div/a/div[1]/div[2]/div[2]')
            
            # timeA3 = driver.find_element_by_xpath('//*[@id="classificacao__wrapper"]/section/ul/li[3]/div/a/div[1]/div[2]/div[1]/span[1]')
            # timeB3 = driver.find_element_by_xpath('//*[@id="classificacao__wrapper"]/section/ul/li[3]/div/a/div[1]/div[2]/div[3]/span[1]')
            # placar3 = driver.find_element_by_xpath('//*[@id="classificacao__wrapper"]/section/ul/li[3]/div/a/div[1]/div[2]/div[2]')
            
            # timeA4 = driver.find_element_by_xpath('//*[@id="classificacao__wrapper"]/section/ul/li[4]/div/a/div[1]/div[2]/div[1]/span[1]')
            # timeB4 = driver.find_element_by_xpath('//*[@id="classificacao__wrapper"]/section/ul/li[4]/div/a/div[1]/div[2]/div[3]/span[1]')
            # placar4 = driver.find_element_by_xpath('//*[@id="classificacao__wrapper"]/section/ul/li[4]/div/a/div[1]/div[2]/div[2]')
            
            # timeA5 = driver.find_element_by_xpath('//*[@id="classificacao__wrapper"]/section/ul/li[5]/div/a/div[1]/div[2]/div[1]/span[1]')
            # timeB5 = driver.find_element_by_xpath('//*[@id="classificacao__wrapper"]/section/ul/li[5]/div/a/div[1]/div[2]/div[3]/span[1]')
            # placar5 = driver.find_element_by_xpath('//*[@id="classificacao__wrapper"]/section/ul/li[5]/div/a/div[1]/div[2]/div[2]')
            
            
            # timeA6 = driver.find_element_by_xpath('//*[@id="classificacao__wrapper"]/section/ul/li[6]/div/a/div[1]/div[2]/div[1]/span[1]')
            # timeB6 = driver.find_element_by_xpath('//*[@id="classificacao__wrapper"]/section/ul/li[6]/div/a/div[1]/div[2]/div[3]/span[1]')
            # placar6 = driver.find_element_by_xpath('//*[@id="classificacao__wrapper"]/section/ul/li[6]/div/a/div[1]/div[2]/div[2]')
            
            # timeA7 = driver.find_element_by_xpath('//*[@id="classificacao__wrapper"]/section/ul/li[7]/div/a/div[1]/div[2]/div[1]/span[1]')
            # timeB7 = driver.find_element_by_xpath('//*[@id="classificacao__wrapper"]/section/ul/li[7]/div/a/div[1]/div[2]/div[3]/span[1]')
            # placar7 = driver.find_element_by_xpath('//*[@id="classificacao__wrapper"]/section/ul/li[7]/div/a/div[1]/div[2]/div[2]')
            
            # timeA8 = driver.find_element_by_xpath('//*[@id="classificacao__wrapper"]/section/ul/li[8]/div/a/div[1]/div[2]/div[1]/span[1]')
            # timeB8 = driver.find_element_by_xpath('//*[@id="classificacao__wrapper"]/section/ul/li[8]/div/a/div[1]/div[2]/div[3]/span[1]')
            # placar8 = driver.find_element_by_xpath('//*[@id="classificacao__wrapper"]/section/ul/li[8]/div/a/div[1]/div[2]/div[2]')
            
            # timeA9 = driver.find_element_by_xpath('//*[@id="classificacao__wrapper"]/section/ul/li[9]/div/div/div/div[2]/div[1]/span[1]')
            # timeB9 = driver.find_element_by_xpath('//*[@id="classificacao__wrapper"]/section/ul/li[9]/div/div/div/div[2]/div[3]/span[1]')
            # placar9 = driver.find_element_by_xpath('//*[@id="classificacao__wrapper"]/section/ul/li[9]/div/div/div/div[2]/div[2]')
            
            # timeA10 = driver.find_element_by_xpath('//*[@id="classificacao__wrapper"]/section/ul/li[10]/div/div/div/div[2]/div[1]/span[1]')
            # timeB10= driver.find_element_by_xpath('//*[@id="classificacao__wrapper"]/section/ul/li[10]/div/div/div/div[2]/div[3]/span[1]')
            # placar10 = driver.find_element_by_xpath('//*[@id="classificacao__wrapper"]/section/ul/li[10]/div/div/div/div[2]/div[2]')
            
            # inserir(timeA.text,timeB.text,placar.text,rodada.text)
            # inserir(timeA2.text,timeB2.text,placar2.text,rodada.text)
            # inserir(timeA3.text,timeB3.text,placar3.text,rodada.text)
            # inserir(timeA4.text,timeB4.text,placar4.text,rodada.text)
            # inserir(timeA5.text,timeB5.text,placar5.text,rodada.text)
            # inserir(timeA6.text,timeB6.text,placar6.text,rodada.text)
            # inserir(timeA7.text,timeB7.text,placar7.text,rodada.text)
            # inserir(timeA8.text,timeB8.text,placar8.text,rodada.text)
            # inserir(timeA9.text,timeB9.text,placar9.text,rodada.text)
            # inserir(timeA10.text,timeB10.text,placar10.text,rodada.text)