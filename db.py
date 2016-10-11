# -*- coding: utf-8 -*-
from sqlite3 import dbapi2 as sqlite3


DATABASE = './db/toryburch.db'
SCHEMA = './db/schema.sql'


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(DATABASE)
    rv.row_factory = dict_factory   #sqlite3.Row
    return rv


def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


def init_db():
    """Initializes the database."""
    db = connect_db()
    with open(SCHEMA, 'r') as f:
        db.cursor().executescript(f.read())
    db.commit()


def initdb_command():
    """Creates the database tables."""
    init_db()
    print('Initialized the database.')


def get_categories(show_type):
    cate_url_all = "https://www.toryburch.com/handbags/view-all/"
    db = connect_db()
    if show_type.upper() == "/ALL":
        sql_prod = 'SELECT CATEGORY, CATEGORY_URL, COUNT(1) AS COUNT ' \
                   'FROM TORY_PROD ' \
                   'WHERE STATUS=\'ACTIVE\' ' \
                   'GROUP BY CATEGORY '\
                   'UNION ALL '\
                   'SELECT \'View All\' AS CATEGORY, \''+ cate_url_all +'\' AS CATEGORY_URL '\
                   ', COUNT(1) AS COUNT '\
                   'FROM TORY_PROD ' \
                   'WHERE STATUS=\'ACTIVE\''
    elif show_type.upper() == "/SALE":
        sql_prod = 'SELECT CATEGORY, CATEGORY_URL, COUNT(1) AS COUNT ' \
                   'FROM TORY_PROD ' \
                   'WHERE SALES_PRICE <> \'0\' AND STATUS=\'ACTIVE\' ' \
                   'GROUP BY CATEGORY '\
                   'UNION ALL '\
                   'SELECT \'View All\' AS CATEGORY, \''+ cate_url_all +'\' AS CATEGORY_URL '\
                   ', COUNT(1) AS COUNT '\
                   'FROM TORY_PROD ' \
                   'WHERE SALES_PRICE <> \'0\' AND STATUS=\'ACTIVE\''
    cur_prod = db.execute(sql_prod)
    cates = cur_prod.fetchall()
    return cates
    db.close()
