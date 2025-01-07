import datetime
import asyncio

from modules.FindFreeGame.steam import Steam
from modules.FindFreeGame.epicgames import EpicGames
from modules.TelegramBot.telegram import telegram
from ChatGPTAPI.chatgpt import ChatGPT
from modules.NewInformation.PostInfromation import PostInformation


async def send_photos(data, ai, tg):
    for i in data:
        try:
            my_data = await asyncio.to_thread(ai.itc_push, i)
            await tg.sendPhoto(img=i[2], data=my_data, url=i[3])
            print("Повідомлення відправлено")
        except Exception as ex:
            print(f"Error: {ex}")

        await asyncio.sleep(720)
async def main_loop():
    AI = ChatGPT()
    tg_print = telegram()
    my_settings = {
        "post": {
            "steamfind": 0,
            "epicfind": 0,
            "sendMessageEpic": 0,
            "sendMessageSteam": 0,
            "sendNewPost": 0,
        },
        "date": datetime.datetime.now().day,
    }
    this_time=None
    while True:
        my_time = datetime.datetime.now().hour
        if 2 <= my_time <= 8 and my_settings['post']['steamfind'] == 0:
            my_settings['post']['steamfind'] = 1
            steam = Steam()
            await steam.page_confirms()

        if 19 <= my_time <= 20 and my_settings['post']['epicfind'] == 0:
            my_settings['post']['epicfind'] = 1
            epic = EpicGames()
            data = epic.find_free()

            for i in data:
                try:
                    my_data = await asyncio.to_thread(AI.epic_push, i)
                    await tg_print.sendPhoto(img=i[0], data=my_data)
                    await asyncio.sleep(20)
                except Exception as ex:
                    print(f"Error: {ex}")

        if 13 <= my_time <= 20 and my_settings['post']['sendNewPost'] == 0:
            my_settings['post']['sendNewPost'] = 1
            this_time=my_time

            post = PostInformation()
            data = post.catalog_requests()

            await send_photos(data, AI, tg_print)

        if 10 <= my_time <=12 and my_settings['post']['sendMessageSteam'] == 0:
            my_settings['post']['sendMessageSteam'] = 1
            steam=Steam()
            catalog=steam.catalog_messages()
            if catalog['free']:
                my_data = await asyncio.to_thread(AI.steam_free_push, catalog['free'])
                await tg_print.sendPhoto(img=catalog['free'][0]['img'], data=my_data)
                await asyncio.sleep(20)
            await asyncio.sleep(100)
            if catalog['sales']:
                my_data = await asyncio.to_thread(AI.steam_sales_push, catalog['sales'])
                await tg_print.sendMessage(text=my_data)
                await asyncio.sleep(20)
        try:
            if this_time+2==my_time:
                my_settings['post']['sendNewPost']=0
        except Exception as ex:
            print(f"Error {ex}")

        if my_settings['date'] < datetime.datetime.now().day:
            my_settings['post'] = {
                "steamfind": 0,
                "epicfind": 0,
                "sendMessageEpic": 0,
                "sendMessageSteam": 0,
                "sendNewPost": 0,
            }
            my_settings['date'] = datetime.datetime.now().day

        await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(main_loop())



