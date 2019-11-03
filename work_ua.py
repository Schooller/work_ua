from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
from bs4 import BeautifulSoup

DRIVER_PATH = 'options/chromedriver.exe'
URL_TEMPLATE = 'https://www.work.ua/ru/jobs-odesa/?page='

options = Options()
options.add_argument('--headless')
driver = webdriver.Chrome(DRIVER_PATH, chrome_options=options)


def get_page_info(url: str):
    result_list = []
    driver.get(url)
    sleep(0.3)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    names = soup.find_all('h2', class_='add-bottom-sm')
    for name in names:
        result_list.append(name.a.text)
    return result_list


def get_max_value_page():
    driver.get(URL_TEMPLATE+'1')
    sleep(0.3)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    return int(soup.find('span', class_='text-default').text[10:])


def parser_work_ua(max_value: int):
    result_list = []
    for i in range(1,max_value+1):
        array = get_page_info(URL_TEMPLATE+str(i))
        result_list.append(array)
    return result_list


if __name__ == '__main__':
    max_value = get_max_value_page()
    print(parser_work_ua(max_value))