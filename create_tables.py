import psycopg2
from config import config


def create_tables():
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
            id_product INT NOT NULL REFERENCES product(id),
            id_group INT NOT NULL REFERENCES groups(id),
            PRIMARY KEY (id_product, id_group)
        )
        """)
    conn = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # create table one by one
        for command in commands:
            cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    create_tables()
