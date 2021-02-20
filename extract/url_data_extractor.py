from urllib.request import urlopen
from lxml.html import parse
from bs4 import BeautifulSoup
import urllib.request
import http.cookiejar as cookie
import mechanize
import requests

import logging


class Extractor:
    def __init__(self, url):
        """

        """
        self._url = url

    def get_title(self):
        """
        Extract the tile from web page
        """
        page = urlopen(self._url)
        p = parse(page)
        return p.find(".//title").text

    def check_if_login_form_present(self):
        """
        Extract login form if this form exist in the page

        """
        try:
            cj = cookie.CookieJar()
            br = mechanize.Browser()
            br.set_cookiejar(cj)
            br.open(self._url)
            br.select_form(nr=0)
            return True
        except Exception:
            return False

    def get_all_links(self):
        """
        Extract all the accessible and inaccessible link in the page

        """
        links = []
        parser = 'html.parser'  # or 'lxml' (preferred) or 'html5lib', if installed
        resp = urllib.request.urlopen(self._url)
        soup = BeautifulSoup(resp, parser, from_encoding=resp.info().get_param('charset'))

        for link in soup.find_all('a', href=True):
            if "http" in link['href']:
                links.append(link['href'])

        return links

    def get_inaccesible_links(self, links):
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
        soup = BeautifulSoup(self._url, 'html.parser')
        for level in levels:
            headings = soup.find_all(level)
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
        #print(output)
        return output
