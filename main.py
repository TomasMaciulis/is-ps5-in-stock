import os
import winsound
import urllib.request
import time
import random
import webbrowser
from bs4 import BeautifulSoup
from selenium import webdriver
from datetime import datetime

AMAZON_DE_URL = "https://www.amazon.de/dp/B08H93ZRK9/ref=cm_sw_r_tw_dp_x_z3M6FbSNBJJVZ"
AMAZON_CO_UK_URL = "https://www.amazon.co.uk/dp/B08H95Y452/ref=cm_sw_r_tw_dp_x_nUZ6FbZ7V21DT"
TOPOCENTRAS_URL = "https://www.topocentras.lt/zaidimu-kompiuteris-sony-playstation-5.html"
GAMEROOM_URL = "https://gameroom.lt/lt/playstation-5-konsoles/products/playstation-5-zaidimu-konsole-825gb-ps5-4299"
ELEKTROMARKT_URL = "https://elektromarkt.lt/video-zaidimai-ir-iranga/zaidimu-konsoles/playstation-konsoles/konsole-sony-playstation-5"
AVITELA_URL = "https://avitela.lt/video-zaidimai-ir-iranga/zaidimu-konsoles/playstation-konsoles/konsole-sony-playstation-5"
TECHNORAMA_URL = "https://www.technorama.lt/playstation-5/24600-konsole-sony-playstation-5-standart-edition-white.html"


def check_amazon_de():
    soup = get_page_html(AMAZON_DE_URL)

    try:
        availability = soup.find('span', {'class': 'a-size-medium a-color-price'}).text.strip()
    except:
        print("Amazon.de is asking for captcha... sleeping for 10 minutes")
        time.sleep(600)
        return False

    if availability != 'Derzeit nicht verfügbar.':
        try:
            availability = soup.find('span', {'id': 'price_inside_buybox'}).text.strip()
        except:
            return False
        return True

    return False


def check_amazon_co_uk():
    soup = get_page_html(AMAZON_CO_UK_URL)

    try:
        availability = soup.find('span', {'class': 'a-size-medium a-color-price'}).text.strip()
    except:
        print("Amazon.co.uk is asking for captcha... sleeping for 10 minutes")
        time.sleep(600)
        return False

    if availability != 'Currently unavailable.':
        try:
            availability = soup.find('span', {'id': 'price_inside_buybox'}).text.strip()
        except:
            return False
        return True

    return False


def check_topocentras():
    soup = get_page_html_with_javascript(TOPOCENTRAS_URL)

    try:
        soup.find('h1', {'class': 'OutOfStock-title-38o'}).text.strip()
    except:
        try:
            availability = soup.find('div', {'class': 'Price-priceTitle-1Er'}).text.strip()
            if availability:
                return True
        except:
            print("Topocentras.lt doesn't display correctly or is asking for captcha... Sleeping for 10 minutes")
            time.sleep(600)
            return False

        return False

    return False


def check_gameroom():
    soup = get_page_html(GAMEROOM_URL)

    try:
        print(soup.find('span', {'style': 'color:#7cd320;text-decoration:underline;'}).text.strip())
    except:
        try:
            availability = soup.find('button', {'class': 'exclusive btn btn-outline-inverse'}).span.text.strip()
            if availability:
                return True
        except:
            print("Gameroom.lt doesn't display correctly or is asking for captcha... Sleeping for 10 minutes")
            time.sleep(600)
            return False


def check_elektromarkt():
    soup = get_page_html(ELEKTROMARKT_URL)

    try:
        print(soup.find('a', {'id': 'outofstock'}).text.strip())
    except:
        try:
            availability = soup.find('input', {'type': 'button', 'id': 'button-cart'})['value']
            print(availability)

            if availability:
                return True
        except:
            try:
                availability = soup.find('input', {'data-target': '#ribotaskiekis'})['value']
                print(availability)

                if availability:
                    return True
            except:
                print("Elektromarkt.lt doesn't display correctly or is asking for captcha... Sleeping for 10 minutes")
                time.sleep(600)
                return False

    return False


def check_avitela():
    soup = get_page_html(AVITELA_URL)

    try:
        print(soup.find('a', {'id': 'outofstock'}).text.strip())
    except:
        try:
            availability = soup.find('input', {'type': 'button', 'id': 'button-cart'})['value']
            print(availability)

            if availability:
                return True
        except:
            try:
                availability = soup.find('input', {'data-target': '#ribotaskiekis'})['value']
                print(availability)

                if availability:
                    return True
            except:
                print("Avitela.lt doesn't display correctly or is asking for captcha... Sleeping for 10 minutes")
                time.sleep(600)
                return False

    return False

def check_technorama():
    soup = get_page_html(TECHNORAMA_URL)

    try:
        print(soup.find('div', {'class': 'out-of-stock-container'}).text.strip())
    except:
        try:
            availability = soup.find('button', {'data-button-action': 'add-to-cart'}).text.strip()
            if availability:
                return True
        except:
            print("Technorama.lt doesn't display correctly or is asking for captcha... Sleeping for 10 minutes")
            time.sleep(600)
            return False

    return False

def get_page_html(url):
    opener = urllib.request.build_opener()
    opener.addheaders = [
        ('User-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/201001{} Firefox/66.0'.format(random.randrange(0, 99, 1))),
        ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
        ('DNT', '1'),
        ('Connection', 'close'),
        ('Upgrade-Insecure-Requests', 1)
    ]

    page = opener.open(url)

    return BeautifulSoup(page, 'html.parser')


def get_page_html_with_javascript(url):
    os.environ['MOZ_HEADLESS'] = '1'
    browser = webdriver.Firefox()
    browser.get(url)
    time.sleep(5)
    html = browser.page_source.encode('utf-8').strip()
    browser.close()

    return BeautifulSoup(html, 'html.parser')


def success(url):
    webbrowser.open(url)
    winsound.PlaySound('C:\projects\is-in-stock\siren.wav', winsound.SND_FILENAME)
    exit()


if __name__ == '__main__':
    while True:
        print("Checking amazon.de...")
        if check_amazon_de():
            success(AMAZON_DE_URL)
        else:
            print("No luck with Amazon at {} :(".format(datetime.now().time()))

        print("Checking amazon.co.uk...")
        if check_amazon_co_uk():
            success(AMAZON_CO_UK_URL)
        else:
            print("No luck with Amazon at {} :(".format(datetime.now().time()))

        print("Checking technorama.lt...")
        if check_technorama():
            success(TECHNORAMA_URL)
        else:
            print("No luck with Technorama at {} :(".format(datetime.now().time()))


        print("Checking elektromarkt.lt...")
        if check_elektromarkt():
            success(ELEKTROMARKT_URL)
        else:
            print("No luck with Elektromarkt at {} :(".format(datetime.now().time()))

        print("Checking avitela.lt...")
        if check_avitela():
            success(AVITELA_URL)
        else:
            print("No luck with Avitela at {} :(".format(datetime.now().time()))

        print("Checking gameroom.lt...")
        if check_gameroom():
            success(GAMEROOM_URL)
        else:
            print("No luck with Gameroom at {} :(".format(datetime.now().time()))

        print("Checking topocentras.lt...")
        if check_topocentras():
            success(TOPOCENTRAS_URL)
        else:
            print("No luck with Topocentras at {} :(".format(datetime.now().time()))

        sleep_duration = random.randrange(1, 600, 1)
        print("Sleeping for {} seconds.".format(sleep_duration))
        time.sleep(sleep_duration)
