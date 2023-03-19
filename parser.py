from threading import Thread
import datetime

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from urllib.parse import urlparse
from urllib.parse import parse_qs

from config import *
from db import *


def parsing_start_daemon():
    t = Thread(target=parsing_daemon)
    t.start()


def parsing_daemon():
    while True:
        try:
            print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' starting parsing')
            parse_threading()
            print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' parsing done')
        except Exception as exc:
            print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' parsing stopped')
            print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' ' + str(exc))


def parse_threading():
    try:
        start_page = 1
        pages_count = get_pages_count()
        number_of_threads = 10  # TREADS COUNT
        number_per_thread = ((pages_count - start_page) // number_of_threads)
        range_start = start_page
        range_end = start_page + number_per_thread

        threads = []
        for number in range(number_of_threads):
            t = Thread(target=parse_data, args=(range_start, range_end))
            t.start()
            threads.append(t)
            range_start = range_end + 1
            range_end = range_start + number_per_thread

    except Exception as exc:
        print(str(exc))


def parse_data(start_page, end_page):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(chrome_options=chrome_options)  # chrome_options=chrome_options
    try:
        page = start_page
        while page <= end_page:
            driver.get(geturl(url_base, str(page)))
            house_urls = []
            try:
                table_element = driver.find_element(By.CSS_SELECTOR, 'body > div.outer > div.main-block > div.container > div:nth-child(12) > table > tbody')
                tr_elements = table_element.find_elements(By.TAG_NAME, 'tr')
                for tr_element in tr_elements:
                    td_elements = tr_element.find_elements(By.TAG_NAME, 'td')
                    house_urls.append(td_elements[1].find_element(By.TAG_NAME, 'a').get_attribute('href'))

                for url in house_urls:
                    driver.get(url)
                    house_table = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[3]/div[1]/dl')
                    dt_elements = house_table.find_elements(By.TAG_NAME, 'dt')
                    house_data = {
                        'id': int(url.replace(url_base, '')),
                        'address': '',
                        'construction_year': 0,
                        'floors': 0,
                        'house_type': '',
                        'apt_count': 0,
                        'emergency': 0,
                        'url': url,
                        'lng': 0,
                        'lat': 0
                    }
                    try:
                        for dt_element in dt_elements:
                            if dt_element.text == 'Адрес':
                                house_data['address'] = get_data_for_element(dt_element, dt_element.text).text.replace('   На карте', '')
                            elif dt_element.text == 'Год ввода в эксплуатацию' or dt_element.text == 'Год постройки':
                                house_data['construction_year'] = int(get_data_for_element(dt_element, dt_element.text).text)
                            elif dt_element.text == 'Количество этажей':
                                house_data['floors'] = int(get_data_for_element(dt_element, dt_element.text).text)
                            elif dt_element.text == 'Тип дома':
                                house_data['house_type'] = get_data_for_element(dt_element, dt_element.text).text
                            elif dt_element.text == 'Жилых помещений':
                                house_data['apt_count'] = int(get_data_for_element(dt_element, dt_element.text).text)
                            elif dt_element.text == 'Дом признан аварийным':
                                emergency_text = get_data_for_element(dt_element, dt_element.text).text
                                if emergency_text == 'Да':
                                    emergency = 1
                                else:
                                    emergency = 0
                                house_data['emergency'] = emergency

                        house_data['lng'] = float(driver.find_element(By.XPATH, '//*[@id="mapcenterlng"]').get_attribute('value'))
                        house_data['lat'] = float(driver.find_element(By.XPATH, '//*[@id="mapcenterlat"]').get_attribute('value'))

                    except:
                        pass
                    try:
                        insert_data(house_data)
                    except Exception as exc:
                        print(url + ': ' + str(exc))
                        continue

                page = page + 1
            except Exception as exc:
                print(str(exc))
                continue

    except Exception as exc:
        print(str(exc))
    driver.quit()


def get_dd_by_dt(dt_element, house_table):
    dt_xpath = gen_xpath(dt_element)
    dd_xpath = dt_xpath.replace('dt', 'dd')
    return house_table.find_element(By.XPATH, dd_xpath)


def get_data_for_element(web_element, value):
    parent = web_element.find_element(By.XPATH, '..')
    children = parent.find_elements(By.XPATH, '*')
    next_return = False
    for c in children:
        if next_return:
            return c
        if c.text == value:
            next_return = True
            continue


def gen_xpath(child, curr=''):
    if (child.tag_name == 'html'): return f'/html[1]{curr}'

    parent = child.find_element(By.XPATH, '..')
    children = parent.find_elements(By.XPATH, '*')
    i = 0
    for c in children:
        if c.tag_name == child.tag_name: i += 1
        if c == child: return gen_xpath(parent, f'/{child.tag_name}[{i}]{curr}')


def geturl(base, page):
    return base+'?page='+page


def get_pages_count():
    chrome_options = Options()
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(chrome_options=chrome_options)
    url = geturl(url_base, str(1))
    driver.get(url)
    last_page_element = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/ul[3]/li[5]/a')
    last_page_element.click()

    parsed_url = urlparse(driver.current_url)
    last_page = parse_qs(parsed_url.query)['page'][0]

    driver.quit()
    return int(last_page)

