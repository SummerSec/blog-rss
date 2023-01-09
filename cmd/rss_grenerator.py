import os

import requests
from feedgen.feed import FeedGenerator

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

def get_description(html_link) -> str:
    """Get the description of the article from the html file"""
    description_url = ""
    response = requests.request(url=html_link)
    if response.status_code == 200:
        html_content = response.text
        for line in html_content.splitlines():
            if line.startswith('<meta name="description" content="'):
                description_url = line.replace('<meta name="description" content="', '').replace('">', '')
    return description_url


def git_push_file():
    """Git Push the file to the github"""
    # set author and email
    try:
        username = "git config --global user.name SummerSec"
        email = "git config --global user.email SummerSec@users.noreply.github.com"
        os.system(username)
        os.system(email)
        # git add
        git_add = "git add ."
        os.system(git_add)
        # git commit
        git_commit = "git commit -m \":fire: update rss.xml\""
        os.system(git_commit)
        # git push
        git_push = "git push"
        os.system(git_push)


    except Exception as e:
        print("Error: " + str(e))


if __name__ == '__main__':
    print('Start generating RSS feed...')
    fg = FeedGenerator()
    fg.id("https://sumsec.me")
    fg.title("SumSec's Blog")
    fg.description("像清水一般清澈透明")
    fg.link(href="https://sumsec.me", rel='alternate')
    fg.language("zh-CN")
    sitemap = SiteMap()
    sitemap.get_all_urls()
    # 颠倒顺序
    sitemap.urls.reverse()
    for md_link in sitemap.urls:
        fe = fg.add_entry()
        md_link = md_link.replace(" ", "")
        fe.id(md_link)
        fe.title(md_link)
        fe.link(href=md_link, rel='alternate')
        # description = get_description(md_link)
        # print(description)
        # fe.description(description)

    fg.rss_file("../rss.xml")
    fg.atom_file("../atom.xml")
    print('RSS feed generated successfully!')
    git_push_file()


