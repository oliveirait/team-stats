# IMPORTANDO AS BIBLIOTECAS NECESSÁRIAS
import PySimpleGUI as sg
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from time import sleep
from sys import exit

def events():
    event, values = window.read()
    if (event == sg.WIN_CLOSED) or (event == 'Sair'): # if user closes window or clicks cancel
        window.close()
        exit()
    if (not values[0]):
        sg.popup('Favor, verifique os campos vazios antes de continuar')
        return events()
    else:
        return values[0]
        window.close()
        

# -- PROCURA ELEMENTO POR CSS SELECTOR
def proc_css(selector):
    results = browser.find_element(By.CSS_SELECTOR, selector)
    return results

# -- PROCURA ELEMENTO POR XPATH
def proc_xpath(xpath):
    results = browser.find_element( By.XPATH, xpath )
    return results

# -- AGUARDA A PAGINA SER CA
def pageDown():
    page = browser.find_element(By.CSS_SELECTOR, 'body').send_keys(Keys.PAGE_DOWN)

# INICIALIZANDO VARIAVEIS
url = 'https://www.sofascore.com/pt/'


# APLICA TEMA AO SOFTWARE
sg.theme('Dark Grey 13') 

# JANELA DO SOFTWARE
layout = [  [sg.Text('INFORMACOES CLUBE')],
            [sg.Text('EQUIPE: ', size=(15,0),  ), sg.InputText(size=(30,0))],
            [sg.Text('')],
            [sg.Button('Executar', size=(10,0)), sg.Button('Sair', size=(10,0))]]

window = sg.Window('Configurações de Rede do condominio', layout)

# LOOP PARA CARREGAR JANELA E DADOS
while True:
    
    team = events()
        
    # INICIA O NAVEGADOR  
    option = Options()
    option.add_argument('--disable-notifications')
    browser = webdriver.Chrome(options=option)
    browser.implicitly_wait(30)
    browser.maximize_window()
    browser.get(url)
    
    # CLICA NA BARRA DE PESQUISA
    search = proc_xpath('//*[@id="__next"]/div/header/div[1]/div/div[2]/div/form/input')
    search.click()
    search.clear()
    search.send_keys(f"{team}")
    
    searchList = proc_xpath('//*[@id="__next"]/div/header/div[1]/div/div[2]/div/div/div/div[1]/div[1]/a/div/div/span')
    searchList.click()
    
    sleep(2)
    pageDown()
    pageDown()
    
    partidas = int(proc_xpath('//*[@id="__next"]/div/main/div/div[2]/div[2]/div/div[4]/div[3]/div[2]/div[2]/div[1]/span[2]').text)
    gols_partida = float(proc_xpath('//*[@id="__next"]/div/main/div/div[2]/div[2]/div/div[4]/div[3]/div[3]/div[2]/div[1]/span[2]').text)
    media_cartoes_amarelos = float(proc_xpath('//*[@id="__next"]/div/main/div/div[2]/div[2]/div/div[4]/div[3]/div[6]/div[2]/div[7]/span[2]').text)
    cartoes_amarelos = float(media_cartoes_amarelos * partidas)
    cartoes_vermelhos = float(proc_xpath('//*[@id="__next"]/div/main/div/div[2]/div[2]/div/div[4]/div[3]/div[6]/div[2]/div[8]/span[2]').text)
    media_cartoes = (cartoes_amarelos + cartoes_vermelhos) / partidas
    media_escanteio = float(proc_xpath('//*[@id="__next"]/div/main/div/div[2]/div[2]/div/div[4]/div[3]/div[3]/div[2]/div[17]/span[2]').text)
      
    with open('file.txt', 'a') as file:
        file.write(f'{team} \n' )
        file.write(f'{partidas} = Partidas \n' )
        file.write(f'{gols_partida} = Gols por partida \n')
        file.write(f'{round(media_cartoes, 2)} = Media de cartões por jogo \n')
        file.write(f'{media_escanteio} = Média de escanteio por jogo \n\n')
    
    
    
       
    

    
