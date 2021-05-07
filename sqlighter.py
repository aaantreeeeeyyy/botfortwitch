import os
import psycopg2


class SQLighter:
    def __init__(self):
        DATABASE_URL = os.environ['jdbc:postgresql://localhost:5432/postgres']
        self.connection = psycopg2.connect(DATABASE_URL, sslmode='require')
        # self.connection = psycopg2.connect(
        #     host="localhost",
        #     database="postgres 2",
        #     user="postgres",
        #     password="9xvG2cn")
        self.cursor = self.connection.cursor()

    def get_subscriptions(self, status=True):
        """Получаем всех активных подписчиков бота"""
        with self.connection:
            return self.cursor.execute("SELECT * FROM `profile` WHERE `status` = ?", (status,)).fetchall()

    def subscriber_exists(self, user_id):
        """Проверяем, есть ли уже юзер в базе"""
        with self.connection:
            result = self.cursor.execute('SELECT * FROM `profile` WHERE `user_id` = ?', (user_id,)).fetchall()
            return bool(len(result))

    def add_subscriber(self, user_id, status=True):
        """Добавляем нового подписчика"""
        with self.connection:
            return self.cursor.execute("INSERT INTO `profile` (`user_id`, `status`) VALUES(?,?)", (user_id, status))

    def update_subscription(self, user_id, status):
        """Обновляем статус подписки пользователя"""
        with self.connection:
            return self.cursor.execute("UPDATE `profile` SET `status` = ? WHERE `user_id` = ?", (status, user_id))

    def update_name(self, user_id, name):
        with self.connection:
            return self.cursor.execute("INSERT INTO `profile` (`user_id`, `username`) VALUES(?,?)", (user_id, name))

    def close(self):
        """Закрываем соединение с БД"""
        self.connection.close()
        self.cursor.close()
