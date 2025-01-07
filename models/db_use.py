import datetime

import pymysql
import pymysql.cursors
import models.config as config

class db_use():
    def __init__(self):
        self.user=config.user
        self.port=config.port
        self.host=config.host
        self.password=config.password
        self.db_name=config.db_name
        self.connection=self.connect_base()
    def connect_base(self):
        try:
            connection=pymysql.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.db_name,
                cursorclass=pymysql.cursors.DictCursor
            )
            print("TopConnect")
            return connection
        except Exception as ex:
            print(f'Невдалось приєднатися до БД:\n{ex}')
    def insert_steam(self,data):
        with self.connection.cursor() as cursor:
            query="""
                INSERT INTO steam (appid, name, developer, positive, negative, discount, price) 
                VALUES (%s, %s, %s, %s, %s, %s, %s);
                """
            for field in data:
                print(field)
                cursor.execute(query,field)
            print("Кінець сторінки")
            self.connection.commit()
    def select_steam(self):
        with self.connection.cursor() as cursor:
            query="""SELECT * FROM steam
                    WHERE discount = 100
            """
            cursor.execute(query)
            return cursor.fetchall()

    def delete_steam(self):
        with self.connection.cursor() as cursor:
            query="DELETE FROM steam"
            cursor.execute(query)
            self.connection.commit()
    def new_sales_steam(self):
        with self.connection.cursor() as cursor:
            query = """
            SELECT steam.*
            FROM steam
            LEFT JOIN steamNew ON steam.appid = steamNew.appid
            WHERE steamNew.appid IS NULL;
            """

            cursor.execute(query)
            return cursor.fetchall()
    def steam_rename(self):
        interim_name = "steamreload"
        name_base = "steam"
        new_steam = "steamnew"

        try:
            with self.connection.cursor() as cursor:

                self.connection.autocommit = False

                cursor.execute(f"RENAME TABLE {new_steam} TO {interim_name}")
                cursor.execute(f"RENAME TABLE {name_base} TO {new_steam}")
                cursor.execute(f"RENAME TABLE {interim_name} TO {name_base}")

                self.connection.commit()
                self.delete_steam()

                print("Таблиці успішно перейменовані.")
        except Exception as e:
            self.connection.rollback()
            print(f"Помилка при перейменуванні таблиць: {e}")

        self.delete_steam()
    def select_epic(self):
        with self.connection.cursor() as cursor:
            query="SELECT * FROM epicgames"
            cursor.execute(query)

            return cursor.fetchall()
    def insert_epic(self,data):
        new_data=[]

        with self.connection.cursor() as cursor:
            query="""
            INSERT INTO epicgames (`img`,`title`, `id`, `description`, `datestart`, `datefinish`, `originalprice`, `discountprice`)
            VALUES (%s,%s, %s, %s, %s, %s, %s, %s);
            """
            self.delete_epic_time()

            for values in data:
                if self.find_publish_epic(values):
                    new_data.append(values)
                    cursor.execute(query,values)

            self.connection.commit()

        return new_data
    def delete_epic(self):
        with self.connection.cursor() as cursor:
            query="DELETE FROM epicgames"
            cursor.execute(query)
            self.connection.commit()
    def delete_epic_time(self):
        time=datetime.datetime.now()
        with self.connection.cursor() as cursor:
            query="""
            DELETE FROM publishepic
            WHERE dateEnd < NOW()
            """
            cursor.execute(query)
            self.connection.commit()
    def insert_publish_epic(self,new_data:list):
        with self.connection.cursor() as cursor:
            query="""
            INSERT INTO publishepic (`id`, `title`, `dateEnd`) 
            VALUES (%s,%s,%s);
            """
            for data in new_data:
                values=(data[3],data[2],data[5])
                print(data)
                print(f"value - {values}")
                cursor.execute(query,values)
            self.connection.commit()
    def find_publish_epic(self, new_data):
        try:
            with self.connection.cursor() as cursor:
                query = """
                SELECT * FROM publishepic
                WHERE title = %s AND id = %s
                """
                values = (new_data[2], new_data[3])

                cursor.execute(query, values)
                data = cursor.fetchall()

                if data:
                    return False

        except Exception as ex:
            print(f"Error: {ex}")

        return True

    def select_message(self):
        with self.connection.cursor() as cursor:
            query = """
            SELECT * FROM `message_push`
            """
            cursor.execute(query)

            return cursor.fetchall()
    def insert_message(self,url):
        with self.connection.cursor() as cursor:
            query="""
            INSERT INTO `message_push` (`url`) VALUES (%s);
            """
            values=(url,)

            cursor.execute(query,values)
            self.connection.commit()