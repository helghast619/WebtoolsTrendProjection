# Import statements
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException
import re
import pandas as pd


def get_driver(url):
    """
    creates chrome driver with url
    :param url: website link to be scrapped
    :return: driver object
    """
    options = webdriver.ChromeOptions()
    options.add_argument("ignore-certificate-errors")
    driver_create = webdriver.Chrome(chrome_options=options)
    driver_create.get(url)
    time.sleep(6)
    return driver_create


def get_source(driver_param):
    """
    gets the page source and returns a beautifulsoup object
    :param driver_param: driver object for the source
    :return: beautifulsoup object
    """
    time.sleep(10)
    source_code = driver_param.page_source
    soupy = BeautifulSoup(source_code, features='html.parser')
    return soupy


def get_link_headers(soupy):
    """
    returns all the header names of clickable links
    :param soupy: beautifulsoup object
    :return: list of all headers
    """
    time.sleep(6)
    tags = []
    print(soupy.find_all('h3'))
    for tag in soupy.find_all('h3'): #, attrs={"class": "post-title post-url"})
        for i in tag.find_all('a'):
            tags.append(i.text)
    # tags.append(tag.string.strip())
    print(tags)
    return tags


def extract_date(soup_url):
    """
           Return date for soup object
           param: soup object
           """
    months = []
    pat = re.compile(r"(\d{1,2}\s(Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|"
                     r"Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)((,)|(\s))\d{4})|(((Jan(?:uary)?|Feb(?:"
                     r"ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|"
                     r"Nov(?:ember)?|Dec(?:ember)?)\s\d{1,2}((,)|(\s))(()|(\s))\d{4})|((\d{1,2}\s(Jan(?:uary)?|Feb(?:"
                     r"ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|"
                     r"Nov(?:ember)?|Dec(?:ember)?)(,)\s\d{4})))")  # re.compile(r"(\d{1,2}\s\w*((,)|(\s))\d{4})|((
    # \w*\s\
    # d{1,2}((,)|(\s))(()|(\s))\d{4})|((\d{1,2}\s\w*(,)
    # \s\d{4})))")
    dates = re.findall(pat, str(soup_url))
    dates = [j for k in dates for j in k]
    dates = set(dates)
    dates = list(dates)
    if dates:
        for i in dates:
            if len(i) > 8:
                return i
                break
    else:
        return None


def scrap_paragraphs(soupy):
    """
    returns a list of all paragraphs contains from soup object
    :param soupy: beautifulsoup object
    :return: list of strings
    """
    time.sleep(6)
    text_content = []
    for para in soup.find_all('p'):
        text_content.append(para.get_text())
    return text_content


if __name__ == "__main__":
    df = pd.DataFrame(columns=["title", "date", "summary"])
    links = "https://www.azom.com/materials-news.aspx?CatID=33"
    driver = get_driver(links)
    soup = get_source(driver)
    headers = get_link_headers(soup)
    for i in headers:
        print(i)
        element = ec.presence_of_element_located(
            (By.PARTIAL_LINK_TEXT, i))
        try:
            WebDriverWait(driver, 20).until(element)
            element = driver.find_element(By.PARTIAL_LINK_TEXT, i)
            element.location_once_scrolled_into_view
            driver.execute_script("window.scrollTo(0, -1);")
            time.sleep(3)
            ActionChains(driver).move_to_element(element).click().perform()
            soup = get_source(driver)
            dt = extract_date(soup)
            text = scrap_paragraphs(soup)
            df = df.append(pd.DataFrame([[i, dt, text]], columns=["title", "date", "summary"]))
            print("Before Back Print.................")
            driver.back()
            print("After Back print...........")
            time.sleep(10)
        except TimeoutException as ex:
            print("Exception has been thrown. " + str(ex))
            break
    file_name = 'azom.csv'
    # file_name = driver.current_url.split("/")[-1] + ".csv"
    df.to_csv(file_name, encoding="utf-8", header=True, sep=',')
    print(df)
