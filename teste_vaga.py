from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from datetime import datetime
import pytz
import time
import json

def Carregar_selenium_options(webdriver):
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-popup-blocking')
    options.add_argument('--disable-notifications')
    options.add_argument("--disable-extensions")
    return options


def Carregar_selenium_driver(webdriver, options):
    driver = webdriver.Chrome(options=options)
    return driver

options = Carregar_selenium_options(webdriver)
driver = Carregar_selenium_driver(webdriver, options)

url = "https://veri.bet/odds-picks?filter=upcoming"
driver.get(url)

lista_tabelas_colunas = WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.XPATH, '//table[@id="odds-picks"]/tbody/tr')))
def moneyline1(jogo):
    dicionario_teste['line_type'] = 'moneyline'
    price = jogo.find_element(By.XPATH, './div/div/div/div/table/tbody/tr[2]/td[2]/table/tbody/tr/td/span').text
    dicionario_teste['price'] = price
    dicionario_teste['side'] = team1
    dicionario_teste['team'] = team1
    dicionario_teste['spread'] = '0'
    lista_dicionario.append(dicionario_teste.copy())

def moneyline2(jogo):
    dicionario_teste['line_type'] = 'moneyline'
    price = jogo.find_element(By.XPATH, './div/div/div/div/table/tbody/tr[3]/td[2]/table/tbody/tr/td/span').text
    dicionario_teste['price'] = price
    dicionario_teste['side'] = team2
    dicionario_teste['team'] = team2
    dicionario_teste['spread'] = '0'
    lista_dicionario.append(dicionario_teste.copy())


def spread1(jogo):
    dicionario_teste['line_type'] = 'spread'
    price = jogo.find_element(By.XPATH, './div/div/div/div/table/tbody/tr[2]/td[3]/table/tbody/tr/td/span').text
    if 'N/A' in price:
        price = ['N/A', 'N/A']
    if '(' in price:
        price = price.replace('(', '').replace(')', '').splitlines()
    dicionario_teste['price'] = price[1]
    dicionario_teste['side'] = team1
    dicionario_teste['team'] = team1
    dicionario_teste['spread'] = price[0]
    lista_dicionario.append(dicionario_teste.copy())

def spread2(jogo):
    dicionario_teste['line_type'] = 'spread'
    price = jogo.find_element(By.XPATH, './div/div/div/div/table/tbody/tr[3]/td[3]/table/tbody/tr/td/span').text
    if 'N/A' in price:
        price = ['N/A', 'N/A']
    if '(' in price:
        price = price.replace('(', '').replace(')', '').splitlines()
    dicionario_teste['price'] = price[1]
    dicionario_teste['side'] = team2
    dicionario_teste['team'] = team2
    dicionario_teste['spread'] = price[0]
    lista_dicionario.append(dicionario_teste.copy())

def over_under1(jogo):
    dicionario_teste['line_type'] = 'over/under'
    price = jogo.find_element(By.XPATH, './div/div/div/div/table/tbody/tr[2]/td[4]/table/tbody/tr/td/span').text
    if 'N/A' in price:
        price = ['N/A', 'N/A']
    if '(' in price:
        price = price.replace('(', '').replace(')', '').splitlines()
    dicionario_teste['price'] = price[1]
    dicionario_teste['side'] = "over"
    dicionario_teste['team'] = "total"
    dicionario_teste['spread'] = price[0].replace('O ', '')
    lista_dicionario.append(dicionario_teste.copy())

def over_under2(jogo):
    dicionario_teste['line_type'] = 'over/under'
    price = jogo.find_element(By.XPATH, './div/div/div/div/table/tbody/tr[3]/td[4]/table/tbody/tr/td/span').text
    if 'N/A' in price:
        price = ['N/A', 'N/A']
    if '(' in price:
        price = price.replace('(', '').replace(')', '').splitlines()
    dicionario_teste['price'] = price[1]
    dicionario_teste['side'] = "under"
    dicionario_teste['team'] = "total"
    dicionario_teste['spread'] = price[0].replace('U ', '')
    lista_dicionario.append(dicionario_teste.copy())

lista_dicionario = []

for tabela_coluna in lista_tabelas_colunas:
    tabela_coluna_html = tabela_coluna.get_attribute('outerHTML')
    soup = BeautifulSoup(tabela_coluna_html, 'html.parser')
    elemento_td = soup.find('td')
    num_divs_td = len(elemento_td.find_all('div', recursive=False))
    # Se o numero de divs dentro da tag <td> for igual a 2, isso significa que é uma tabela de liga esportiva, se não é uma tabela de jogos
    if num_divs_td == 2:
        sport_league = elemento_td.text.strip().splitlines()[0]
    if num_divs_td == 1:
        jogos_elemento = tabela_coluna.find_elements(By.XPATH, './td/div/div/div/div')
        for jogo in jogos_elemento:
            dicionario_teste = {}
            dicionario_teste['sport_league'] = sport_league
            event_date_utc = jogo.find_element(By.XPATH, './div/div/div/div/table/tbody/tr[4]/td[1]/table/tbody/tr/td/span[2]').text
            try:
                data_hora = datetime.strptime(event_date_utc, "%I:%M %p ET (%m/%d/%Y)")
                fuso_horario_et = pytz.timezone('US/Eastern')
                data_hora_et = fuso_horario_et.localize(data_hora)
                formato_iso8601 = "%Y-%m-%dT%H:%M:%S%z"
                event_date_utc = data_hora_et.strftime(formato_iso8601)
            except:
                pass
            dicionario_teste['event_date_utc'] = event_date_utc
            team1 = jogo.find_element(By.XPATH, './div/div/div/div/table/tbody/tr[2]/td[1]/table/tbody/tr/td/table/tbody/tr/td[1]/a/span').text
            dicionario_teste['team1'] = team1
            
            team2 = jogo.find_element(By.XPATH, './div/div/div/div/table/tbody/tr[3]/td[1]/table/tbody/tr/td/table/tbody/tr/td[1]/a/span').text
            dicionario_teste['team2'] = team2
            dicionario_teste['pitcher'] = ''
            if sport_league == "SOCCER":
                draw_price = jogo.find_element(By.XPATH, './div/div/div/div/table/tbody/tr[4]/td[2]/table/tbody/tr/td/span').text.splitlines()[1]
                dicionario_teste['draw_price'] = draw_price

            period = jogo.find_element(By.XPATH, './div/div/div/div/table/tbody/tr[1]/td[1]/span').text
            period = period.replace(" ODDS", "")
            dicionario_teste['period'] = period
            moneyline1(jogo)
            moneyline2(jogo)
            spread1(jogo)
            spread2(jogo)
            over_under1(jogo)
            over_under2(jogo)
            
with open("output.json", 'w') as arquivo_json:
    json.dump(lista_dicionario, arquivo_json, indent=2)

driver.quit()
