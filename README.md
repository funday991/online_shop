**ONLINE SHOP**

`db.ini` needs to be parsed by function `config()`.

TEMPLATE OF `db.ini`:

[your_section_name]  
host=localhost (or your IP)  
database=your_db_name  
user=your_user_name (default: postgres)  
password=your_password

You will have to add your `db.ini` file.

HOW IT WORKS:

1) Function `config()` from `config.py` parses `db.ini` file and saves parameters required for server authorization.
2) Function `connect()` from `connect.py` checks out the access to the server and prints the database version.
3) File `online_shop_db.py` includes base methods for db, e.g. `create_tables()` or `drop_db()`.
4) File `online_shop_main.py` only includes the class `OSBaseTable` with base methods for all tables. As you can see, 
there is no method which inserts lines into a table. The reason is that different tables consist of different fields,
so the insertion method will be local for every subclass of `OSBaseTable`. Other methods will be inherited.

WHAT'S NEXT:

Further the new tables and the subclasses for each required table will be added.