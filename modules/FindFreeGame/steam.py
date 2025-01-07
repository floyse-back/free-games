import time
import steamspypi
import asyncio

from models.db_use import db_use
from deep_translator import GoogleTranslator


import requests
class Steam(db_use):
    def __init__(self,sleep=60):
        super().__init__()
        self.freegames=False
        self.sleep=sleep
        self.stop_find=5
        self.app_details=f"https://store.steampowered.com/api/appdetails?appids="

        self.sourse="auto"
        self.target="uk"
        self.translator=GoogleTranslator(target=self.target,source=self.sourse)

    def translate_to(self,text):
        txt = self.translator.translate(text)
        return txt

    def element_correct(self,data):
        return (
            data['appid'],
            data['name'],
            data['developer'],
            data['positive'],
            data['negative'],
            data['discount'],
            data['price']
        )
    async def filter_data(self,data):
        new_data=list(data.values())
        new_list=[]
        for i in new_data:
            try:
                if int(i['discount'])>=70:
                    new_list.append(self.element_correct(i))
            except Exception as ex:
                print(f"Error {ex}\n {i['discount']}")

        self.insert_steam(new_list)
    async def page_confirms(self):
        stopper=0
        page=0
        self.steam_rename()
        while stopper < self.stop_find:
            data = self.page_collect(page)
            if len(data)==0:
                stopper+=1
            page+=1
            await self.filter_data(data)
            time.sleep(60)
    def page_collect(self,page:int=0):
        detail_page=dict()
        detail_page['request'] = 'all'
        detail_page['page']=str(page)

        data = steamspypi.download(data_request=detail_page)
        return data
    def catalog_messages(self):
        data=self.new_sales_steam()
        my_dict={
            "free":self.free_game(data),
            "sales":self.send_sales_message(data)
        }
        if len(my_dict['free'])>0:
            my_dict['free']=self.steam_details(my_dict['free'])

        if len(my_dict['sales'])>0:
            my_dict['sales']=self.steam_details(my_dict['sales'])

        return my_dict

    def send_sales_message(self,data):
        def positive_key(val):
            return val['positive']-val['negative']

        sales=[]
        best_sales=[]

        for i in data:
            if i['positive']+i['negative']>5000 and i['positive']>i['negative']+1000 and i['discount']>90 and i['discount']!=100:
                best_sales.append(i)
            elif i['positive']+i['negative']>4000 and i['positive']>i['negative'] and i['discount']>85:
                sales.append(i)
        if len(best_sales)>=10:
            best_sales.sort(key=lambda val:positive_key(val))
            best_sales=best_sales[0:9]
        elif len(best_sales)<10:
            num_cut=10-len(best_sales)
            if len(sales)>=num_cut:
                sales.sort(key=lambda val:positive_key(val))
                sales=sales[0:num_cut]
                best_sales=best_sales+sales
            else:
                if len(sales)>0:
                    best_sales=best_sales+sales


        return best_sales

    def free_game(self,data):
        free=[]

        for i in data:
            if i['discount'] == 100:
                free.append(i)

        return free
    def steam_details(self,data):
        new_data=[]

        if not isinstance(data,list):
            data=list(data)

        for i in data:
            response=requests.get(url=f"{self.app_details}{i['appid']}")
            print(f"{self.app_details}{i['appid']}")
            my_data=response.json()[f'{i['appid']}']['data']
            new_data.append(self.filter_details(my_data))
        return new_data

    def filter_details(self,data):
        text_translate=self.translate_to(text=data['short_description'])
        my_dict={
            "img":data['header_image'],
            "name":data['name'],
            "description":text_translate,
            "initial_formatted":data['price_overview']['initial_formatted'],
            "final_formatted":data['price_overview']['final_formatted']
        }

        return my_dict