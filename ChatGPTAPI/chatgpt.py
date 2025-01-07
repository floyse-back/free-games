from g4f.client import Client
from datetime import datetime
from langdetect import detect_langs
import asyncio

class ChatGPT():
    def text_filter(self, text):
        if not text or not isinstance(text, str):
            return False
        try:
            data = detect_langs(text)
            for lang in data:
                if lang.lang == 'uk' and lang.prob > 0.9:
                    return True
        except Exception as ex:
            print(f"Language detection error: {ex}")
        return False
    async def push(self, content):
        client = Client()
        timer = 0
        response = None
        while timer < 8:
            timer += 1
            try:
                response = await asyncio.to_thread(
                    lambda: client.chat.completions.create(
                        model="gpt-4o",
                        messages=[{"role": "user", "content": f"{content}"}],
                    )
                )
                if response and response.choices:
                    new_content = response.choices[0].message.content
                    print(new_content)
                    if len(new_content) > 256 and len(new_content) < 1024 and self.text_filter(new_content):
                        return new_content
            except Exception as ex:
                print(f"Error {ex}")
        return None
    def epic_push(self, data):
        if not data or len(data) < 8:
            raise ValueError("Invalid data structure passed to epic_push.")
        content = self.epic_prompt(data)
        return asyncio.run(self.push(content))
    def itc_push(self, data):
        content = self.post_prompt(data)
        return asyncio.run(self.push(content))
    def steam_sales_push(self, data):
        text=self.steam_sales_prompt(data=data)
        return text
    def steam_free_push(self, data):
        content = self.steam_free_prompt(data)
        return asyncio.run(self.push(content))
    def epic_prompt(self,data):
        return f"""
        Ви досвідчений менеджер соціальних медіа з великим досвідом створення цікавих та інформативних публікацій для каналів Telegram, зокрема для тих, що зосереджені на безкоштовних іграх та спеціальних акціях. Ваше завдання — створити захоплюючий допис у Telegram-каналі про акцію безкоштовної гри «{data[1]}». Ось деталі, які мають бути включені в допис:
        Якщо ціна без знижки дорівнює 0, то напишіть "безкоштовно".
        Якщо ціна без знижки дорівнює ціні зі знижкою, то згадуйте лише знижку.
        Публікація має бути захоплюючою та інформативною, без прямих посилань на саму гру, але з акцентом на її унікальні особливості.
        Деталі акції:
        Розпродаж проводиться в Epic Games.
        Назва: {data[1]}
        Опис гри: {data[3]}
        Ціна без знижки: {data[6]} (центи)
        Ціна зі знижкою: {data[7]} (центи)
        Дата початку: {data[4]}
        Дата кінця: {data[5]}
        Сьогодні: {datetime.now().date()}
        Пам'ятайте, публікація має бути емоційною та підкреслювати цікаві моменти, як захоплюючий сюжет і інноваційні особливості ігрового процесу, щоб мотивувати спільноту взяти участь у цій акції.
        Примітка: Тон має бути дружнім та привабливим, ніби ви спілкуєтеся безпосередньо зі своєю аудиторією.
        """
    def post_prompt(self,data):
        return f"""\
            Твоє завдання — взяти наданий текст, який був опублікований на певному сайті, і перетворити його у формат, зручний для публікації в Telegram-каналі, присвяченому іграм.
            Вимоги до тексту:
            1. Скорочення: залиш тільки найважливіші деталі, уникни зайвої інформації.
            2. Заголовок: придумай короткий, яскравий заголовок, який одразу приверне увагу.
            3. Емодзі: використовуй доречні емодзі для покращення сприйняття тексту.
            4. Заклик до дії: додай наприкінці фразу, яка мотивуватиме взаємодіяти з постом (наприклад, "Напишіть, що ви думаєте!" або "Слідкуйте за новинами нашого каналу!").
            5. Посилання на джерело: якщо є, перефразуй інформацію так, щоб передати суть, уникаючи прямого копіювання.
            Формат для обробки:  
            {data[0]}   
            {data[1]}  
            Очікуваний вихідний текст:
            1. Лаконічний і чіткий.
            2. Зрозумілий для аудиторії Telegram-каналу.
            3. Українською мовою.
        """

    def steam_free_prompt(self,data):
        print(data)
        return f"""
        Ти створюєш короткий, цікавий і структурований пост для телеграм-каналу про знижки на ігри. Вхідні дані:
        
        Назва гри: {data[0]['name']}
        Короткий опис: {data[0]['description']}
        Початкова ціна: {data[0]['initial_formatted']}
        Ціна зі знижкою: {data[0]['final_formatted']}
        Правила:

        Пост не повинен перевищувати 1024 символи.
        Текст повинен містити: назву гри, опис (максимально лаконічний), вказівку на знижку та нову ціну.
        Завжди додавай заклик до дії, наприклад, "Купити зараз!" або "Скористайся знижкою!"
        Збережи стиль, який зацікавить геймерів.
        Напиши пост, який виглядає привабливо та заохочує до покупки.
        """
    def steam_sales_prompt(self,data):
        print(data)
        txt = "# Steam найкращі знижки дня!!!\n"
        for index, value in enumerate(data):
            txt += f"{index + 1}. *{value['name']}* {value['final_formatted']} ~~{value['initial_formatted']}~~ \n".replace("~~~~","")

        print(txt)
        return txt