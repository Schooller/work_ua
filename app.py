from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
from bs4 import BeautifulSoup
import datetime

DRIVER_PATH = 'options/chromedriver.exe'
URL_TEMPLATE = 'https://csgoempire.com/'

options = Options()
options.add_argument('--headless')
driver = webdriver.Chrome(DRIVER_PATH, chrome_options=options)


def get_info():
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    info = soup.find('div', class_='flex items-center justify-end')
    results = info.find_all('div', class_='mr-2')[1:]
    return int(results[0].text), int(results[1].text), int(results[2].text)


if __name__ == '__main__':
    driver.get(URL_TEMPLATE)
    sleep(15) #Даем страничке прогрузится, зависит от интернета, поставил 10 - страничка тяжелая
    start_time = datetime.datetime.now()
    print('Started')
    Result = [0, 0, 0]
    Unresult = [0, 0, 0]
    active, value = 0, 0
    value1, value2, value3 = 0, 0, 0
    pace_ct, pace_x14, pace_t = 0, 0, 0
    roll = 0
    while(True):
        xct, x14, xt = get_info()
        print(xct, x14, xt)
        if xct == pace_ct+1:
            print('ct',end=" ")
            Unresult[0] = max(Unresult[0], value1)
            value2+=1
            value3+=1
            Unresult[1] = max(Unresult[1], value2)
            Unresult[2] = max(Unresult[2], value3)
            value1 = 0
            if active == 0:
                value+=1
                Result[active] = max(Result[active], value)
            else:
                active = 0
                value = 1
                Result[active] = max(Result[active], value)
            print(value)
            roll+=1
        elif xt == pace_t+1:
            print('t',end=" ")
            Unresult[2] = max(Unresult[2], value3)
            value2+=1
            value1+=1
            Unresult[1] = max(Unresult[1], value2)
            Unresult[0] = max(Unresult[0], value1)
            value3 = 0
            if active == 2:
                value+=1
                Result[active] = max(Result[active], value)
            else:
                active = 2
                value = 1
                Result[active] = max(Result[active], value)
            print(value)
            roll+=1
        elif x14 == pace_x14+1:
            print('x14',end=" ")
            Unresult[1] = max(Unresult[1], value2)
            value1+=1
            value3+=1
            Unresult[0] = max(Unresult[0], value1)
            Unresult[2] = max(Unresult[2], value3)
            value2 = 0
            if active == 1:
                value+=1
                Result[active] = max(Result[active], value)
            else:
                active = 1
                value = 1
                Result[active] = max(Result[active], value)
            print(value)
            roll+=1
        handle = open("result.txt", "w")
        handle.write("Всего роллов: "+str(roll)+"\nМаксимальное количество повторений:\nДля CT(x2): "+str(Result[0])+", Для T(x2): "+str(Result[2])+", Для x14: "+str(Result[1])+"\nСамая длинная серия  не выпадений:\nДля CT(x2): "+str(Unresult[0])+", Для T(x2): "+str(Unresult[2])+", Для x14: "+str(Unresult[1])+"\nВремя выполнения: с "+str(start_time)+" до "+str(datetime.datetime.now()))
        handle.close()
        pace_ct, pace_x14, pace_t = xct, x14, xt
        sleep(1)