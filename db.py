# coding=utf-8

import sqlite3
from datetime import datetime, timedelta


class Mdb:

    def __init__(self):
        """

        """
        # for DEBUG can store DB in file
        self.db = sqlite3.connect(':memory:')
        # self.db = sqlite3.connect('db.sqlite3')

        self.cursor = self.db.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS circles(id INTEGER PRIMARY KEY,
                                 x INTEGER, y INTEGER, r INTEGER, dt DATETIME)
        ''')
        self.db.commit()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS kv(id INTEGER PRIMARY KEY,
                                 key VARCHAR(20), val VARCHAR(20), dt DATETIME)
        ''')
        self.db.commit()

    def setupdate_value_for_key(self, key, value='1'):
        """
        set value for key (if not exists)
        or update existing value
        :return:
        """
        if not isinstance(value, basestring):
            value = str(value)
        self.cursor.execute('''SELECT dt FROM kv WHERE key = ? ''', (key, ))
        db_exists = self.cursor.fetchone()
        if db_exists:
            self.cursor.execute('''UPDATE kv SET val = ? , dt = ? WHERE key = ? ''',
                                (value, datetime.now(), key))
        else:
            self.cursor.execute('''INSERT INTO kv (key, val, dt)VALUES(?, ?, ?) ''',
                                (key, value, datetime.now()))
        self.db.commit()
        return None

    def get_setdefault_value_for_key(self, key, default_value='0', valid_sec=None):
        """
        gey value for key,
        if not exists -set and return default
        if stared valid_sec and value is TRUE (==1),
        if value was set earlier than valid_sec seconds - reset it to FALSE (=0)
        :return:
        """
        value = default_value
        if not isinstance(default_value, basestring):
            default_value = str(default_value)
        self.cursor.execute('''SELECT val, dt FROM kv WHERE key = ? ''', (key, ))
        db_exists = self.cursor.fetchone()
        if db_exists:
            value = db_exists[0]
            if valid_sec and value == '1':
                # print 'db_exists[1]', db_exists[1]  # 2018-10-04 14:05:04.218126
                datetime_object = datetime.strptime(db_exists[1], '%Y-%m-%d %H:%M:%S.%f')
                # print datetime_object
                # print timedelta(seconds=valid_sec)
                # print datetime.now() - datetime_object
                if timedelta(seconds=valid_sec) < datetime.now() - datetime_object:
                    self.cursor.execute('''UPDATE kv SET val = ? , dt = ? WHERE key = ? ''',
                                        (0, datetime.now(), key))
                    self.db.commit()
                    value = 0
        else:
            self.cursor.execute('''INSERT INTO kv (key, val, dt)VALUES(?, ?, ?) ''',
                                (key, default_value, datetime.now()))
        self.db.commit()
        if isinstance(value, basestring) and value.isdigit():
            value = int(value)
        return value

    def delete_old_circles(self, delete_older_than_seconds):
        """
        delete old stored circles
        :return:
        """
        self.cursor.execute('''DELETE FROM circles WHERE dt < ? ''',
                            (str(datetime.now() -
                                 timedelta(seconds=delete_older_than_seconds)),))
        self.db.commit()
        return None

    def insert_new_circle(self, x, y, r):
        """
        insert new discovered circle
        :param x:
        :param y:
        :param r:
        :return:
        """
        self.cursor.execute('''INSERT INTO circles(x, y, r, dt) VALUES(?,?,?,?)''', (x, y, r, datetime.now()))
        self.db.commit()
        return None

    def select_similar_circles(self, xmin, xmax, ymin, ymax, rmin, rmax):
        """
        find stored circles, similar to one
        - with center position in range and radius in range
        :param xmin:
        :param xmax:
        :param ymin:
        :param ymax:
        :param rmin:
        :param rmax:
        :return:
        """
        self.cursor.execute('''SELECT x,y,r FROM circles
        WHERE x > ? AND x < ? AND y > ? AND y < ? AND r > ? AND r < ? ''', (xmin, xmax,
                                                                            ymin, ymax,
                                                                            rmin, rmax)
                            )
        like_this_circle = self.cursor.fetchall()
        return like_this_circle
