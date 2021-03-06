import sqlite3


class User:
    def __init__(
        self,
        id,
        user_name,
        password,
        first_name,
        last_name,
        goal,
        weight,
        height,
        experiencie,
    ):
        self.id = id
        self.user_name = user_name
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.goal = goal
        self.weight = weight
        self.height = height
        self.experiencie = experiencie

    def full_name(self):
        return self.first_name + " " + self.last_name

    def to_dict(self):
        return {
            "id": self.id,
            "user_name": self.user_name,
            "password": self.password,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "full_name": self.full_name(),
            "goal": self.goal,
            "weight": self.weight,
            "height": self.height,
            "experiencie": self.experiencie,
        }


class UserRepository:
    def __init__(self, database_path):
        self.database_path = database_path
        self.init_tables()

    def create_conn(self):
        conn = sqlite3.connect(self.database_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_tables(self):
        sql = """
            create table if not exists users (
               id VARCHAR PRIMARY KEY,
               user_name VARCHAR,
               password VARCHAR,
               first_name VARCHAR,
               last_name VARCHAR, 
               goal VARCHAR, 
               weight VARCHAR, 
               height VARCHAR, 
               experiencie INTEGER
            )
        """
        conn = self.create_conn()
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()

    def get_users(self):
        sql = """select * from users"""
        conn = self.create_conn()
        cursor = conn.cursor()
        cursor.execute(sql)

        data = cursor.fetchall()

        all_users = [User(**item) for item in data]

        return all_users

    def get_by_user_name(self, user_name):
        sql = """SELECT * FROM users WHERE user_name=:user_name"""
        conn = self.create_conn()
        cursor = conn.cursor()
        cursor.execute(sql, {"user_name": user_name})

        data = cursor.fetchone()
        if data is None:
            return None
        else:
            user = User(**data)
        return user

    def save(self, user):
        sql = """insert or replace into users (id, user_name, password, first_name, last_name, goal, weight, height, experiencie) 
                 values (:id, :user_name, :password, :first_name, :last_name, :goal, :weight, :height, :experiencie)"""
        conn = self.create_conn()
        cursor = conn.cursor()
        cursor.execute(sql, user.to_dict())

        conn.commit()
