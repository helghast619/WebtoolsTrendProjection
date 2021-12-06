# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import datetime
import time
import urllib.request as urllib2
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup

class Throttle:
    """Add a delay between downloads to the same domain """
    def _init_(self,delay):
        #amount of delay between downloads for each domain
        self.delay = delay
        #timestamp when a domian was last accessed
        self.domain = {}
def wait(self,url):
    domain = urlparse.urlparse(url).netloc()
    last_accessed = self.domains.get(domain)

    if self.delay > 0 and last_accessed is not None:
        sleep_secs = self.delay - (datetime.datetime.now()-last_accessed).seconds
        if sleep_secs > 0:
            # domain has been accessed recently
            # so need to sleep
            time.sleep(sleep_secs)
        #update the last accessed
        self.domains[domain] = datetime.datetime.now()


URL = "https://www.nzherald.co.nz/the-country/"
r = requests.get(URL)
soup = BeautifulSoup(r.text, 'html.parser')
for l in soup.find_all('a'):
    print(l.get('href'))





# print(soup.prettify())


# print(builtwith.parse('https://www.stuff.co.nz'))

#print(whois.whois('stuff.co.nz'))


##def download(url):
  ##  print("Downloading..", url)
    ##try:
      ##  html = urllib2.urlopen(url).read()
    ##except  urllib2.HTTPErrorProcessor as e:
      ##  print("Download error", e.reason)
        ##html = None
   ## return html


##print(download("https://www.stuff.co.nz"))
