import sqlite3


class DataBase:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

        with self.connection:
            self.cursor.execute(
                """CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INT NOT NULL,
                user_name varchar (20),
                money INT NOT NULL DEFAULT '0',
                is_banned BOOLEAN  DEFAULT (False));"""
            )

        with self.connection:
            self.cursor.execute(
                """CREATE TABLE IF NOT EXISTS 'check'(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INT NOT NULL,
                money INT NOT NULL ,
                bill_id VARCHAR NOT NULL);"""
            )

    def user_exsist(self, user_name):
        result = self.cursor.execute("SELECT * FROM users WHERE user_name = ?", (user_name,)).fetchall()
        return bool(len(result))


    def add_user(self, user_id, user_name):
        with self.connection:
            self.cursor.execute("INSERT INTO users (user_id, user_name) VALUES (?,?)", (user_id, user_name,))

    def user_money(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT money FROM users WHERE user_id = ?", (user_id,)).fetchmany(1)
            return int(result[0][0])

    def set_money(self, user_id, money):
        with self.connection:
            return self.cursor.execute("UPDATE users SET money = ? WHERE user_id = ?", (money, user_id,))

    def add_check(self, user_id, money, bill_id):
        with self.connection:
            self.cursor.execute("INSERT INTO 'check' (user_id, money, bill_id) VALUES (?,?,?)",
                                (user_id, money, bill_id,))

    def get_check(self, bill_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM 'check' WHERE bill_id = ?", (bill_id,)).fetchmany(1)
            if not bool(len(result)):
                return False
            return result[0]

    def delete_check(self, bill_id):
        with self.connection:
            return self.cursor.execute("DELETE FROM 'check' WHERE bill_id = ?", (bill_id,))

    def show_all(self):
        with self.connection:
            return self.cursor.execute("SELECT user_name, money FROM users").fetchall()

    def admin_check(self, user_name):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM users WHERE user_name = ?", (user_name,)).fetchall()
            return bool(len(result))

    def admin_set_money(self, user_name, money):
        with self.connection:
            return self.cursor.execute("UPDATE users SET money = ? WHERE user_name = ?", (money, user_name,))


    def check_ban_user(self, user_name):
        with self.connection:
            result = self.cursor.execute("SELECT is_banned FROM users WHERE user_name = ?", (user_name,)).fetchall()
            return bool(int(result[0][0]))


    def ban_set_user(self, user_name, is_banned):
        with self.connection:
            return self.cursor.execute("UPDATE users SET is_banned = ? WHERE user_name = ?", (is_banned, user_name))
