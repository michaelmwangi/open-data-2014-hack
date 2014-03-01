__author__ = 'micheal mwangi'
DBPATH = "students.sqlite"
CSVFILE = "csvfile.csv"
import csv
import sqlite3 as db


class Database:
    def __init__(self):
        self.conn = db.connect(DBPATH)
        self.cursor = self.conn.cursor()
        sql = '''CREATE TABLE IF NOT EXISTS admissiondata
        (id text Primary key,
        name text,
        gender text,
        primary_school text,
        category text,
        marks text,
        selected_school text,
        district text
        )
        '''
        self.conn.text_factory = str
        self.cursor.execute(sql)
        self.conn.commit()

    def insert_data(self, data):
        stmt = '''INSERT INTO admissiondata VALUES(?,?,?,?,?,?,?,?)'''
        self.cursor.execute(stmt, data)
        self.conn.commit()

    def commit(self):
        self.conn.commit()

    def fetch_data(self, key, value):
        stmt = 'SELECT *FROM admissiondata WHERE ' + key + '=' + '\'' + value + '\''
        res = self.cursor.execute(stmt).fetchall()
        return res

    def fetch_category(self, filter):
        stmt = 'SELECT *FROM admissiondata WHERE  category=' + '\'' + filter + '\''
        res = self.cursor.execute(stmt).fetchall()
        return res

    def fetch_schools(self):
        stm = 'SELECT high_school FROM admissiondata'
        schools = set()
        res = self.cursor.execute(stm).fetchall()
        return set(res)


def get_data_from_csv():
    DB = Database()
    with open(CSVFILE) as csvfile:
        csvdata = csv.reader(csvfile)
        count = 0
        for line in csvdata:
            if count == 0:
                count = 1
                pass
            else:
                DB.insert_data(line[1:])


if __name__ == '__main__':
    get_data_from_csv()
    
