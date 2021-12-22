# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import datetime
import time
import urllib.request as urllib2
from urllib import parse as urlparse
import requests
from bs4 import BeautifulSoup
import re
import ssl
import certifi
import pandas as pd
from htmldate import find_date
import wget
# import subprocess
import glob, os
import zipfile


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
    #r = requests.get(link)
    goContext = ssl.SSLContext()
    r = urllib2.urlopen(link,context=goContext).read()
    soup = BeautifulSoup(r, features='html.parser')
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


def prepare_zip(path, zip_name):
    """
           Creates zip for all pages extracted from pdfs
           param: directory path and name of zip
           """
    img_files = []
    os.chdir(path)
    print(path)
    # get all the images files names in a list
    for file in glob.glob("page_*"):
        img_files.append(file)
    # create zip with list of files
    with zipfile.ZipFile(zip_name + '.zip', 'w') as zipF:
        for files in img_files:
            zipF.write(files, compress_type=zipfile.ZIP_DEFLATED)
    print('Zip Created Successfully!!')


def issuu_scraper(pdf_url, pages):
    for page in range(1, pages + 1):
        soup = get_soup(pdf_url)
        # locate the image asset
        pg_title = soup.find('meta', attrs={'property': 'og:title'})['content']
        img_link3 = soup.find('meta', attrs={'property': 'og:image'})['content']
        img_link2 = img_link3.replace('1.jpg', '')
        img_link = img_link2 + str(page) + ".jpg"
        # download image asset
        wget.download(img_link)
        print('\nPage {}: {}\n'.format(page, img_link))
        with open('urls.txt', 'a') as f:
            f.write(img_link + '\n')
    prepare_zip(os.getcwd(), pg_title)
    for files in glob.glob("page_*"):
        os.remove(files)


    """
    # convert pages to pdf
    params = ['convert', 'page_*', pagetitle + '.pdf']
    subprocess.run(params)
        
    # collect information on the file
    metadata = {'URL': url, 'description': soup.find('meta', attrs={'property': 'og:description'})['content'],
                'uploaded': extract_date(pdf_url)}

    upload_link_soup = soup.find('div', attrs={'class': 'PublisherInfo__name--3j27Y'})
    #metadata['uploader_link'] = "https://issuu.com" + upload_link_soup.a['href']

    #metadata['uploader'] = soup.find('a', attrs={'itemprop': 'author'}).contents[0]

    metadata_out = '\n'.join({'{}: {}'.format(k, v) for k, v in metadata.items()})
    print(metadata_out)

    with open('info.txt', 'w') as f:
        f.write(metadata_out)
        """


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
    dates = [j for i in dates for j in i]
    dates = set(dates)
    dates = list(dates)
    if dates:
        for i in dates:
            if (len(i) > 8):
                return i
                break
    else:
        return None


def find_internal_url(urlp, depth=0, max_depth=0):
    urls = []
    soup = get_soup(urlp)
    a_tags = soup.find_all('a', href=True)
    print('inside internal url')
    print(a_tags)
    #    if URL.endswith("/"):
    #       domain = URL
    #    else:
    #       domain = "/".join(URL.split("/")[:-1])
    domain = urlparse.urlparse(urlp)
    pattern_url = domain.scheme + "://" + domain.netloc + domain.path
    pattern = re.compile(rf"{pattern_url}.*")
    # print(domain)
    # print(pattern_url)
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
            status_dict = {"url": url, "status_code": get_status_code(url), "timestamp": datetime.datetime.now(),
                           "depth": depth + 1}
            if url not in [urls[i]["url"] for i in range(len(urls))] and re.match(pattern_url, url) and \
                    status_dict["status_code"] == 200:
                urls.append(status_dict)
    return urls


def get_scrap(urls):
    scrap_df = []
    for i in range(len(urls)):
        soup = get_soup(urls[i]["url"])
        dt = extract_date(soup)  # soup.find('time').get('datetime')
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
    url = "https://www.agribusinessgroup.com/news"
    #pdf_urls = "https://issuu.com/ashguardian/docs/guardian_farming_-_2021-12-18_48_pages_for_uploa"
    #issuu_scraper(pdf_urls, 47)
    #"""
    depth = 0
    all_urls = find_internal_url(url, 0, 2)
    if depth > 1:
        for status_dict in all_urls:
            find_internal_url(status_dict["url"])
    df = pd.DataFrame(get_scrap(all_urls))
    pd.set_option("display.max_colwidth", None)
    df.to_csv("agribusiness.csv", encoding="utf-8", index= False, header= True)
#"""

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
