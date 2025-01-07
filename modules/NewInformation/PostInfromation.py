import time

import requests
from bs4 import BeautifulSoup
import datetime
from models.db_use import db_use

class PostInformation(db_use):
    def __init__(self):
        super().__init__()
        self.itc="https://itc.ua/ua/tag/igri-ua/"
        self.poligon="https://www.polygon.com"
        self.vgtimes="https://vgtimes.ru/gaming-news/"

        self.yesterday=datetime.datetime.now() - datetime.timedelta(days=1)

    def check_select_urls(self,data):
        list_urls=self.select_message()
        t=0

        if not list_urls:
            return data
        else:
            sorted_data=[]
            for i in data:
                for s in list_urls:
                    if i[3]==s['url']:
                        t=1
                        break
                if t==0:
                   sorted_data.append(i)
                t=0

            return sorted_data


    def catalog_requests(self):
        data=self.itc_request_catalog()

        for i in self.polygon_request_catalog():
            data.append(i)

        print(data)
        new_data=self.check_select_urls(data=data)
        print(new_data)

        return new_data

    def itc_request_catalog(self):
        datelist=[]

        response=requests.get(self.itc)
        soup=BeautifulSoup(response.content,"html.parser")
        main=soup.find('main',id="content")
        posts=main.findAll('div',class_="post")


        for i in posts:
            date=i.find("span",class_="date").text
            date=date.replace("\n","")
            date=date.replace("\t","")
            date=date.replace(" ","")
            date=date.replace("о"," о ")
            datelist.append((datetime.datetime.strptime(date, "%d.%m.%Y о %H:%M"),i))

        new_list=[]
        for date in datelist:
            if self.yesterday<date[0]:
                new_list.append(date[1])
        last_data=[]
        for i in new_list:
            data = i.find("div",class_="row")
            url = data.find("h2", class_="entry-title").find("a")['href']
            last_data.append(self.itc_post(url))
        return last_data
    def itc_post(self,url):
        response=requests.get(url)

        soup=BeautifulSoup(response.content,"html.parser")
        try:
            delete_element=soup.find("section",id="wrapper").find("div",class_="widget-spec-projects")
            delete_element.decompose()
            soup.prettify()
        except Exception as ex:
            print(f"Error {url}",)

        try:
            delete_element=soup.find("section",id="wrapper").find("p",class_="intro")
            delete_element.decompose()
            soup.prettify()
        except Exception as ex:
            print(f"Error {url}")

        try:
            delete_element=soup.find("section",id="wrapper").find("blockquote",class_="wp-embedded-content")
            delete_element.decompose()
            soup.prettify()
        except Exception as ex:
            print(f"Error {url}")

        try:
            delete_element=soup.find("section",id="wrapper").find("iframe",class_="wp-embedded-content")
            delete_element.decompose()
            soup.prettify()
        except Exception as ex:
            print(f"Error {ex}")

        data=soup.find("section",id="wrapper")
        text_header=soup.find("div",class_="entry-header").find("h1",class_="entry-title")
        text_header=text_header.text.strip()
        img_to_message=data.find("img",class_="img-responsive")['src']
        post_text=data.find("div",class_="post-txt")
        main_text=post_text.text
        main_text=main_text.replace("\n","")

        return (text_header,main_text,img_to_message,url)
    def polygon_request_catalog(self):
        def best_date(value):
            return value[1]

        response=requests.get(self.poligon +"/gaming")

        soup=BeautifulSoup(response.text,"html.parser")
        data=soup.find("main",id="content")
        posts=data.findAll("div",class_="duet--content-cards--content-card")[0:12]

        new_post_list = list()
        for post in posts:
            my_time=post.find("span","duet--article--timestamp")
            url=post.find("a")

            if my_time:
                date_string=str(my_time.find("time")['datetime'])
                parsed_date = datetime.datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S%z")

                new_post_list.append((url,parsed_date))

        new_post_list.sort(key=lambda value: best_date(value),reverse=True)
        print(new_post_list[0][0])
        new_url=new_post_list[0][0]['href']
        new_url=self.poligon + new_url

        my_content= self.polygon_post(url=new_url)
        my_content.append(new_post_list[0][0].text)

        return [(my_content[2],my_content[1],my_content[0],new_url)]


    def polygon_post(self,url):
        response =requests.get(url)

        soup=BeautifulSoup(response.text,"html.parser")

        try:
            delete_element=soup.find("main",id="content").find("div",class_="duet--layout--header-pattern")
            delete_element.decompose()
            soup.prettify()
        except Exception as ex:
            print(f"Error {url}")

        main=soup.find("main",id="content").find("div",class_="duet--layout--entry-body-container").text
        img=soup.find("div",class_="duet--layout--entry-image").find("img")['src']

        return [img,main]

    def vgtimes_request_catalog(self):
        response=requests.get(self.vgtimes)

        soup=BeautifulSoup(response.text,"html.parser")
        data=soup.find("ul",class_="list-items")
        my_li=data.findAll("li")

        content=[]
        for i in my_li:
            date=str(i.find("span",class_="news_item_time").text)

            if date.find("Сегодня")!=-1:
                    main = i.find("div", class_="item-main")
                    text_header = main.find("a").find("span").text
                    img_tag = main.find("img")
                    img_to_message = img_tag['src']
                    url = main.find("a")['href']
                    main_text=self.vgtimes_post(url=url)

                    if main_text != None:
                        content.append((text_header,main_text,img_to_message,url))

        return content

    def vgtimes_post(self,url):
        response=requests.get(url)
        soup=BeautifulSoup(response.text,"html.parser")

        try:
            delete_element=soup.find("div",class_="news_item_content").find("div",class_="news_content_bottom")
            delete_element.decompose()
            soup.prettify()
        except Exception as ex:
            print(f"Error {url}")

        try:
            delete_element=soup.find("div",class_="news_item_content").find("a",class_="tg_ad")
            delete_element.decompose()
            soup.prettify()
        except Exception as ex:
            print(f"Error {url}")

        main=soup.find("div",class_="news_item_content").text
        main=main.replace("\n","")

        return main




posts=PostInformation()
t=posts.vgtimes_request_catalog()
