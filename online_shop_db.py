import psycopg2
from config import config


class OnlineShopDB:
    def __init__(self):
        """ Create new PostgreSQL database """
        self.connect(('CREATE DATABASE online_shop',), 'db.ini', 'for_creating_new_db')

    def connect(self, commands, filename='db.ini', section='postgresql'):
        """ Connect to the PostgreSQL database server """
        conn = None
        try:
            params = config(filename, section)
            conn = psycopg2.connect(**params)
            conn.autocommit = True
            cur = conn.cursor()
            for command in commands:
                cur.execute(command)
            cur.close()
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

    def create_tables(self):
        """ Create tables for online shop in PostgreSQL database """
        commands = (
            """
            CREATE TABLE user_status (
                id SERIAL PRIMARY KEY NOT NULL,
                name VARCHAR(255) NOT NULL,
                discount INT NOT NULL
            )
            """,
            """
            CREATE TABLE users (
                id SERIAL PRIMARY KEY NOT NULL,
                full_name VARCHAR(255) NOT NULL,
                login VARCHAR(255) NOT NULL,
                password VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                phone BIGINT NOT NULL,
                sms_code BIGINT NOT NULL,
                id_user_status INT REFERENCES user_status(id)
            )
            """,
            """
            CREATE TABLE product (
                id SERIAL PRIMARY KEY NOT NULL,
                name VARCHAR(255) NOT NULL,
                price INT NOT NULL
            )
            """,
            """
            CREATE TABLE groups (
                id SERIAL PRIMARY KEY NOT NULL,
                name VARCHAR(255) NOT NULL,
                id_parent INT REFERENCES groups(id)
            )
            """,
            """
            CREATE TABLE product_groups (
                id_product INT NOT NULL REFERENCES product(id) PRIMARY KEY,
                id_group INT NOT NULL REFERENCES groups(id)
            )
            """)
        self.connect(commands)

    def drop_tables(self):
        """ Drop tables from the PostgreSQL database """
        commands = (
            'DROP TABLE users',
            'DROP TABLE user_status',
            'DROP TABLE product_groups',
            'DROP TABLE product',
            'DROP TABLE groups'
        )
        self.connect(commands)

    def drop_db(self):
        """ Drop the PostgreSQL database """
        self.connect(
            ("""
            SELECT pg_terminate_backend(pid)
                FROM pg_stat_activity
                    WHERE datname = 'online_shop'
            """,))
        self.connect(('DROP DATABASE online_shop;',), 'db.ini', 'for_creating_new_db')
