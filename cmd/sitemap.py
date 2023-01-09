import requests
from urllib3.util import url


class SiteMap(object):
    """Class to Parser the sitemap.xml file"""

    def __init__(self):
        """Constructor"""
        self.urls = None
        self.xml_content = None
        self.sitemap_url = "https://sumsec.me/resources/sitemap.xml"

    def get_sitemap(self):
        """Get the sitemap.xml file"""
        sitemap = requests.get(self.sitemap_url)
        if sitemap.status_code == 200:
            self.xml_content = sitemap.text
        else:
            print("Error: Can't get the sitemap.xml file")

    def get_urls(self):
        """Get all the urls from the sitemap.xml file"""
        if self.xml_content is None:
            self.get_sitemap()
        urls = []
        for line in self.xml_content.splitlines():
            if line.replace(" ", "").startswith('<loc>'):
                urls.append(line.replace('<loc>', '').replace('</loc>', '').replace(" ", ""))
        self.urls = urls

    def exclude_urls(self):
        """Exclude the urls from the sitemap.xml file"""
        exclude_urls = ["/resources", ]
        url_list = self.urls.copy()
        for url_str in url_list:
            # print("url_str: " + url_str)
            for exclude_url in exclude_urls:
                if exclude_url in url_str:
                    self.urls.remove(url_str)
                    break
                elif url_str.endswith("/"):
                    self.urls.remove(url_str)
                    break
        # print(self.urls)








    def get_all_urls(self):
        """Get all the urls from the sitemap.xml file"""
        if self.urls is None:
            self.get_urls()
        self.exclude_urls()
