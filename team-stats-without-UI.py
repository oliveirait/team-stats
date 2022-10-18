# IMPORTANDO AS BIBLIOTECAS NECESSÁRIAS
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from time import sleep
from sys import exit

# -- PROCURA ELEMENTO POR CSS SELECTOR
def proc_css(selector):
    results = browser.find_element(By.CSS_SELECTOR, selector)
    return results

# -- PROCURA ELEMENTO POR XPATH
def proc_xpath(xpath):
    results = browser.find_element( By.XPATH, xpath )
    return results

# -- AGUARDA A PAGINA SER CARREGADA 
def pageDown(browser):
    return browser.find_element(By.CSS_SELECTOR, 'body').send_keys(Keys.PAGE_DOWN)

def qtde_times():
    qtde = str(input('Insira quantos times pretende buscar: '))
    if not qtde.isdigit():
        print('Favor, insira apenas números!')
        return qtde_times()
    else:
        return int(qtde)
    
def write_file(counter):
    with open('results.txt', 'a') as file:
        try:
            file.write(f'{team_list[counter]} \n' )
            file.write(f'Partidas           = {partidas}\n' )
            file.write(f'Media de gols      = {gols_partida}\n')
            file.write(f'Media de cartões   = {round(media_cartoes, 2)}\n')
            file.write(f'Média de escanteio = {media_escanteio}\n\n')
        except Exception as e:
            print('Não foi possível abrir o arquivo', e)
            exit()
            
def get_url(navigator, route):
    browser.get(url)
    
# INICIALIZANDO VARIAVEIS
url = 'https://www.sofascore.com/pt/'
team_list = []
qtde = qtde_times()

counter = 1
for i in range(qtde):
    team = str(input(f'Insira o {counter}° time: '))
    team_list.append(team)
    counter += 1
    
# INICIA O NAVEGADOR  
option = Options()
option.add_argument('--disable-notifications')
option.add_argument("start-maximized")
option.add_argument('--disable-blink-features=AutomationControlled')
browser = webdriver.Chrome(options=option)
browser.implicitly_wait(30)

# LOOP PARA CARREGAR JANELA E DADOS
while True:
    
    counter = 0
    for i in range(len(team_list)):
        
        get_url(browser, url)
            
        # CLICA NA BARRA DE PESQUISA
        search = proc_xpath('//*[@id="__next"]/div/header/div[1]/div/div[2]/div/form/input')
        search.click()
        search.clear()
        search.send_keys(f"{team_list[counter]}")
        
        searchList = proc_xpath('//*[@id="__next"]/div/header/div[1]/div/div[2]/div/div/div/div[1]/div[1]/a/div/div/span')
        searchList.click()
        sleep(2)
        
        pageDown(browser)
        pageDown(browser)
        pageDown(browser)
        
        partidas = int(
            proc_xpath(
                '//*[@id="__next"]/div/main/div/div[2]/div[2]/div/div[4]/div[3]/div[2]/div[2]/div[1]/span[2]').text
            )
        gols_partida = float(
            proc_xpath(
                '//*[@id="__next"]/div/main/div/div[2]/div[2]/div/div[4]/div[3]/div[3]/div[2]/div[1]/span[2]').text
            )
        media_cartoes_amarelos = float(
            proc_xpath(
                '//*[@id="__next"]/div/main/div/div[2]/div[2]/div/div[4]/div[3]/div[6]/div[2]/div[7]/span[2]').text
            )
        cartoes_amarelos = float(
            media_cartoes_amarelos * partidas
            )
        cartoes_vermelhos = float(
            proc_xpath(
                '//*[@id="__next"]/div/main/div/div[2]/div[2]/div/div[4]/div[3]/div[6]/div[2]/div[8]/span[2]').text
            )
        media_cartoes = (cartoes_amarelos + cartoes_vermelhos) / partidas
        media_escanteio = float(
            proc_xpath(
                '//*[@id="__next"]/div/main/div/div[2]/div[2]/div/div[4]/div[3]/div[3]/div[2]/div[17]/span[2]').text
            )
        
        write_file(counter)
        
        counter += 1
    
    browser.close()
    exit()
    
    
