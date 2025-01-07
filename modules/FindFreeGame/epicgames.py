from datetime import datetime

from epicstore_api import EpicGamesStoreAPI
from models.db_use import db_use

class EpicGames(db_use):
    def __init__(self):
        super().__init__()
    def dict_to_tuple(self,data:dict):
        return tuple(data.values())
    def filter_data(self,data):
        new_list = []
        for game in data:
            try:
                my_dict=dict()
                my_dict['img']=game['keyImages'][0]['url']
                my_dict['title']=game['title']
                my_dict['id']=game['id']
                my_dict['description']=game['description']
                my_dict['datestart']=datetime.strptime(game['promotions']['promotionalOffers'][0]['promotionalOffers'][0]['startDate'], "%Y-%m-%dT%H:%M:%S.%fZ")
                my_dict['datefinish']=datetime.strptime(game['promotions']['promotionalOffers'][0]['promotionalOffers'][0]['endDate'], "%Y-%m-%dT%H:%M:%S.%fZ")
                my_dict['originalprice']=game['price']['totalPrice']['originalPrice']
                my_dict['discountprice']=game['price']['totalPrice']['discountPrice']

                if my_dict['discountprice']==0:
                    my_tuple=self.dict_to_tuple(my_dict)
                    print(my_tuple)
                    new_list.append(my_tuple)

            except Exception as ex:
                print(f"Error {ex}")

        return new_list
    def find_free(self):
        free_games=EpicGamesStoreAPI()
        free=free_games.get_free_games()
        data = self.filter_data(free['data']['Catalog']['searchStore']['elements'])

        self.delete_epic()
        new_data = self.insert_epic(data)
        print(new_data,"- data")
        self.insert_publish_epic(new_data)
        return new_data