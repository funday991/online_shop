import psycopg2
from config import config


class OSBaseTable:
    def __init__(self):
        self.name = input('Input table name: ')
        self.fields = input('Input table fields separated by spaces:\n').split()

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
            if commands[0][:6] == 'SELECT':
                row = cur.fetchone()
                if row is None:
                    print('No data.')
                while row is not None:
                    print(row)
                    row = cur.fetchone()
            cur.close()
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

    def get_by_id(self, line_id):
        """ Get table line by id """
        print('List of fields:\n' + ' '.join(self.fields) + '\n')
        self.connect(('SELECT * FROM ' + self.name + ' WHERE id = ' + str(line_id),))

    def full_list(self):
        """ Get all table lines """
        print('List of fields:\n' + ', '.join(self.fields) + '\n')
        self.connect(('SELECT * FROM ' + self.name,))

    def delete_line_by_id(self, line_id):
        """ Delete table line by id """
        self.connect(('DELETE FROM ' + self.name + ' WHERE id = ' + str(line_id),))
        print('Successfully deleted.')

    def delete_all_lines(self):
        """ Delete all table lines """
        self.connect(('DELETE FROM ' + self.name,))
        print('Successfully deleted.')
