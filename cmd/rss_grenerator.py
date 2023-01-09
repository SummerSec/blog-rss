import requests
from feedgen.feed import FeedGenerator

from cmd.sitemap import SiteMap


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
    print('RSS feed generated successfully!')
