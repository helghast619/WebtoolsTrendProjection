# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import datetime
import time
import urllib.request as urllib2
from urllib import parse as urlparse
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd


class Throttle:
    """Add a delay between downloads to the same domain """

    def __init__(self, delay):
        # amount of delay between downloads for each domain
        self.delay = delay
        # timestamp when a domain was last accessed
        self.domains = {}

    def wait(self, url):
        domain = urlparse.urlparse(url).netloc
        last_accessed = self.domains.get(domain)

        if self.delay > 0 and last_accessed is not None:
            sleep_secs = self.delay - (datetime.datetime.now() - last_accessed).seconds
            if sleep_secs > 0:
                # domain has been accessed recently
                # so need to sleep
                time.sleep(sleep_secs)
            # update the last accessed
            self.domains[domain] = datetime.datetime.now()


def get_soup(link):
    """
        Return the BeautifulSoup object for input link
        """
    throttle = Throttle(4)
    throttle.wait(link)
    r = requests.get(link)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup


def get_status_code(link):
    """
       Return the error code for any url
       param: link
       """
    try:
        error_code = requests.get(link).status_code
    except requests.exceptions.ConnectionError:
        error_code = -1
    return error_code


def find_interal_url(URL, depth=0, max_depth=0):
    urls = []
    soup = get_soup(URL)
    a_tags = soup.find_all('a', href=True)
    #    if URL.endswith("/"):
    #       domain = URL
    #    else:
    #       domain = "/".join(URL.split("/")[:-1])
    domain = urlparse.urlparse(URL)
    pattern_url = domain.scheme + "://" + domain.netloc + domain.path
    pattern = re.compile(rf"{pattern_url}.*")
    #print(domain)
    #print(pattern_url)
    if depth > max_depth:
        return {}
    else:
        for a_tag in a_tags:
            if "http://" not in a_tag["href"] and "https://" not in a_tag["href"] and "/" in a_tag["href"]:
                url = domain.scheme + "://" + domain.netloc + a_tag["href"]
            elif "http://" in a_tag["href"] or "https://" in a_tag["href"]:
                url = a_tag["href"]
            else:
                continue
            print("Fetching...URLs...")
            status_dict = {}
            status_dict["url"] = url
            status_dict["status_code"] = get_status_code(url)
            status_dict["timestamp"] = datetime.datetime.now()
            status_dict["depth"] = depth + 1
            if url not in [urls[i]["url"] for i in range(len(urls))] and re.match(pattern_url, url):
                urls.append(status_dict)
    return urls


def get_scrap(urls):
    scrap_df = []
    for i in range(len(urls)):
        soup = get_soup(urls[i]["url"])
        dt = soup.find('time').get('datetime')
        text_content = []
        for para in soup.find_all('p'):
            text_content.append(para.get_text())
        scrap_dic = {}
        scrap_dic["url"] = urls[i]["url"]
        scrap_dic["date"] = dt
        scrap_dic["content"] = text_content
        scrap_df.append(scrap_dic)
        print('Scraping....')
    return scrap_df


if __name__ == "__main__":
    url = "https://www.nzherald.co.nz/the-country/news/"
    depth = 0
    all_urls = find_interal_url(url, 0, 2)
    if depth > 1:
        for status_dict in all_urls:
            find_interal_url(status_dict["url"])
    df = pd.DataFrame(get_scrap(all_urls))
    print(df)

# URL = "https://www.nzherald.co.nz/the-country/"
# r = requests.get(URL)
# soup = BeautifulSoup(r.text, 'html.parser')
# print(soup.a)
# for l in soup.find_all('a'):
#   print(l.get('href'))


# print(soup.prettify())


# print(builtwith.parse('https://www.stuff.co.nz'))

# print(whois.whois('stuff.co.nz'))


##def download(url):
##  print("Downloading..", url)
##try:
##  html = urllib2.urlopen(url).read()
##except  urllib2.HTTPErrorProcessor as e:
##  print("Download error", e.reason)
##html = None
## return html


##print(download("https://www.stuff.co.nz"))
