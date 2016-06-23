# coding:utf-8
from bs4 import BeautifulSoup

class HtmlParser(object):

    def parse_pages_urls(self,response):
        soup = BeautifulSoup(response)
        urls = []
        pages = int(soup.find("a",{"class":"next"}).previous_sibling.get_text())
        for i in range(pages):
            urls.append(url + '#page=' + str(i))
        # like ['http://app.mi.com/category/5#page=7']
        return urls

    def parse_applist_urls(self,response):
        soup = BeautifulSoup(response.text)
        a = soup.find("ul",{"id":"all-applist"}).children
        urls = []
        for li in a:
            urls.append('http://app.mi.com' + li.a['href'])
        # like ['http://app.mi.com/detail/125493']
        return urls



    def parse_app_details(self,response):
        # how to handle exception?
        item = {}
        soup = BeautifulSoup(response.text)
        # intro titles section
        intro = soup.find('div', {"class":"intro-titles"})
        item["name"] = intro.h3.get_text()
        item["company"] = intro.findAll("p")[0].get_text()
        item["category"] = intro.findAll("p")[1].findAll('b')[0].next_sibling
        item["support"] = intro.findAll("p")[1].findAll('b')[1].next_sibling
        item["rating"] = intro.div.div['class']
        item["comments_num"] = intro.find("span",{"class":"app-intro-comment"}).get_text()

        # ul class=" cf" section
        ul = soup.find("ul",{"class":" cf"}).children
        for i, li in enumerate(ul):
            if i == 1:
                item["size"] = li.get_text()
            if i == 3:
                item["version"] = li.get_text()
            if i == 5:
                item["updated_at"] = li.get_text()

        item["root"] = soup.find("ul",{"class":"second-ul"}).get_text()
        item["url"] = response.url
        # return dict for dumping into json file
        return item