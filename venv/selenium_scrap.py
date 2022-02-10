from bs4 import BeautifulSoup
from selenium import webdriver
import urllib.request as urllib2
from urllib import parse as urlparse
import ssl
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

driver = webdriver.Firefox()

driver.get('https://farmersweekly.co.nz/s/agri-business')
driver.get('https://farmersweekly.co.nz/s/agri-business')

#goContext = ssl.SSLContext()
#html = urllib2.urlopen("https://farmersweekly.co.nz/s/", context=goContext)
print("before wait")
driver.implicitly_wait(500)
print("after wait")
html = driver.page_source
soup = BeautifulSoup(html,features='html.parser')
print(str(soup))
print("before for")
#with open('./{}.txt'.format('url'), mode='wt', encoding='utf-8') as file:
#    file.write(str(soup))
#for tag in soup.findAll("a", attrs={"class":"js-content-title js-content-navlink slds-text-heading_large"}):
#    print(next(tag.strings))

element = EC.presence_of_element_located((By.LINK_TEXT, "Podcasts"))
WebDriverWait(driver, 20).until(element)
element = driver.find_element_by_link_text("Podcasts")
#element.location_once_scrolled_into_view
print(element)
driver.implicitly_wait(60)
ActionChains(driver).move_to_element(element).click(element).perform()
