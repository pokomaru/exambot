import json
import os
import pymysql.cursors


class Function:
    def __init__(self):
        abs_path = os.path.abspath('conf.json')
        with open(abs_path, 'r') as file:
            CONF_DATA = json.load(file)

        self.connection = pymysql.connect(
            host=CONF_DATA["HOST_NAME"],
            port=CONF_DATA["PORT_NUMBER"],
            user=CONF_DATA["USER_NAME"],
            password=CONF_DATA["DB_PASSWORD"],
            db=CONF_DATA["DB_NAME"],
            charset=CONF_DATA["CHARSET"],
        )

    # Insert処理: on_followイベント時
    def insert_user(self, user_id, name):
        with self.connection.cursor() as cursor:
            sql = "INSERT INTO users (id, name) VALUES (%s, %s)"
            cursor.execute(sql, (user_id, name))
            self.connection.commit()

        self.connection.close()

        # Insert処理: join_groupイベント時
    def insert_group(self, group_id):
        with self.connection.cursor() as cursor:
            sql = "INSERT INTO group_datas (id) VALUES (%s)"
            cursor.execute(sql, (group_id))
            self.connection.commit()

        self.connection.close()

    # Delete処理: un_followイベント時

    def delete_user(self, user_id):
        with self.connection.cursor() as cursor:
            sql = "DELETE FROM users WHERE id = %s"
            cursor.execute(sql, (user_id))
            self.connection.commit()

        self.connection.close()

       # Delete処理: leave_groupイベント時
    def delete_group(self, group_id):
        with self.connection.cursor() as cursor:
            sql = "DELETE FROM group_datas WHERE id = %s"
            cursor.execute(sql, (group_id))
            self.connection.commit()

        self.connection.close()

    # get user_id: push messageを送る時
    def get_user_id(self):
        with self.connection.cursor() as cursor:
            sql = "SELECT id FROM users"
            cursor.execute(sql)
            user_id_all = cursor.fetchall()
            return user_id_all

        self.connection.close()

    # get group_id: push messageを送る時
    def get_group_id(self):
        with self.connection.cursor() as cursor:
            sql = "SELECT id FROM group_datas"
            cursor.execute(sql)
            group_id_all = cursor.fetchall()
            return group_id_all

        self.connection.close()
