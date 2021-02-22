"""   Url data extractor """

from urllib.request import urlopen
import urllib.request
import http.cookiejar as cookie
from lxml.html import parse
from bs4 import BeautifulSoup
import mechanize
import requests


class Extractor:
    """
    Extractor class for Url data extractor
    """
    def __init__(self, url):
        """
        Init method to initilize the object

        """
        self._url = url
        self._parser = 'html.parser'
        self._resp = urllib.request.urlopen(self._url)
        self._soup = BeautifulSoup(self._resp, self._parser)

    def get_title(self):
        """
        Extract the tile from web page
        """
        page = urlopen(self._url)
        parse_page = parse(page)
        return parse_page.find(".//title").text

    def check_if_login_form_present(self):
        """
        Extract login form if this form exist in the page

        """
        try:
            cookie_jar = cookie.CookieJar()
            browser = mechanize.Browser()
            browser.set_cookiejar(cookie_jar)
            browser.open(self._url)
            browser.select_form(nr=0)
            return True
        except Exception:
            return False

    def get_all_links(self):
        """
        Extract all the accessible and inaccessible link in the page

        """
        links = []
        for link in self._soup.find_all('a', href=True):
            if "http" in link['href']:
                links.append(link['href'])

        return links

    @staticmethod
    def get_inaccesible_links(links):
        """
        Extract all inaccessible link in the page

        """
        inaccessible_link = []
        for link in links:
            return_value = requests.get(link)
            if return_value.status_code != 200:
                inaccessible_link.append(link)
        return inaccessible_link

    def get_headings_count_per_level(self):
        """
        Extract all the levels in the page

        """
        level_heading = {}
        levels = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']
        for level in levels:
            headings = self._soup.find_all(level)
            headings_count = len(headings)  # Gets the number of <h1> tags
            level_heading[level] = headings_count
        return level_heading

    def extract_all_data(self):
        """
        Extract all required data and return it as json format
        :return: all data in json format
        """
        output = {}
        output["title"] = self.get_title()
        output["All links"] = self.get_all_links()
        output["headings per level"] = self.get_headings_count_per_level()
        output["inaccessible links"] = self.get_inaccesible_links(output["All links"])
        output["login from present"] = self.check_if_login_form_present()
        return output
