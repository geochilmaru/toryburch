# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from twisted.enterprise import adbapi
import sys
import datetime
import logging
import sqlite3
from scrapy.exceptions import DropItem
from toryburch.items import ToryburchItem

class ToryburchPipeline(object):
    def __init__(self):
        try:
            self.conn = sqlite3.connect("./db/toryburch.db")
            self.conn.text_factory = str
            self.cursor = self.conn.cursor()

            sql_init_prod = "UPDATE TORY_PROD" \
                            " SET STATUS = 'EXPIRED';"
            self.cursor.execute(sql_init_prod)
            self.conn.commit()
        except sqlite3.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])
            sys.exit(1)

    def process_item(self, item, spider):
        sql_sel_prod = "SELECT ROW_ID FROM TORY_PROD" \
                       " WHERE CATEGORY = :CATEGORY" \
                       " AND (TRIM(NAME) = :NANE" \
                       " OR TRIM(DESC) = :DESC);"
        self.cursor.execute(sql_sel_prod, {"CATEGORY": str(item['category'][0].encode('utf-8')).strip(),
                                           "NANE": str(item['name'][0].encode('utf-8')).strip(),
                                           "DESC": str(item['desc'][0].encode('utf-8')).strip()})
        result_prod = self.cursor.fetchone()

        if result_prod:
            try:
                prod_id = result_prod[0]
                sql_upd_prod = "UPDATE TORY_PROD " \
                               " SET LAST_UPD = DATETIME('NOW', 'LOCALTIME'), STATUS = 'ACTIVE'" \
                               " WHERE ROW_ID = :ROW_ID"
                self.cursor.execute(sql_upd_prod, {"ROW_ID": prod_id})
                self.conn.commit()

                sql_del_color = "DELETE FROM TORY_COLOR " \
                                "WHERE PAR_ROW_ID = :PROD_ID;"
                sql_ins_color = "INSERT INTO TORY_COLOR" \
                                "(PAR_ROW_ID, NAME, URL, IMG_URL, CODE" \
                                ", CREATED, LAST_UPD)" \
                                " VALUES" \
                                " ('" + str(prod_id).encode('utf-8') + "'" \
                                ", :color, :url, :img_url, :col_code " \
                                ", DATETIME('NOW', 'LOCALTIME') " \
                                ", DATETIME('NOW', 'LOCALTIME'))"
                self.cursor.execute(sql_del_color, {"PROD_ID": prod_id})
                self.cursor.executemany(sql_ins_color, item['color'])

                sql_sel_price = "SELECT ROW_ID FROM TORY_PRICE" \
                                " WHERE PAR_ROW_ID = :PROD_ID" \
                                " AND STANDARD_PRICE = :STANDARD_PRICE" \
                                " AND SALES_PRICE = :SALES_PRICE;"
                self.cursor.execute(sql_sel_price, {"PROD_ID": prod_id,
                                                    "STANDARD_PRICE": str(item['standard_price'][0].encode('utf-8')).strip(),
                                                    "SALES_PRICE": str(item['sales_price'][0].encode('utf-8')).strip()})
                result_price = self.cursor.fetchone()
            except sqlite3.Error, e:
                print "Error %d: %s" % (e.args[0], e.args[1])
                return item

            if result_price:
                try:
                    price_id = result_price[0]
                    sql_upd_price = "UPDATE TORY_PRICE " \
                                    "SET LAST_UPD = DATETIME('NOW', 'LOCALTIME')" \
                                    "WHERE ROW_ID = :ROW_ID"
                    self.cursor.execute(sql_upd_price, {"ROW_ID": price_id})
                    self.conn.commit()
                except sqlite3.Error, e:
                    print "Error %d: %s" % (e.args[0], e.args[1])
                    return item
            else:
                try:
                    sql_ins_price = "INSERT INTO TORY_PRICE(PAR_ROW_ID, STANDARD_PRICE, SALES_PRICE" \
                          ", CREATED, LAST_UPD) VALUES (:PAR_ROW_ID, :STANDARD_PRICE, :SALES_PRICE" \
                          ", DATETIME('NOW', 'LOCALTIME'), DATETIME('NOW', 'LOCALTIME'));"
                    self.cursor.execute(sql_ins_price, {"PAR_ROW_ID": prod_id
                        , "STANDARD_PRICE": str(item['standard_price'][0].encode('utf-8'))
                        , "SALES_PRICE": str(item['sales_price'][0].encode('utf-8'))})
                    self.conn.commit()
                except sqlite3.Error, e:
                    print "Error %d: %s" % (e.args[0], e.args[1])
                    return item
        else:
            try:
                sql_ins_prod = "INSERT INTO TORY_PROD(CATEGORY, CATEGORY_URL" \
                      ", NAME, FULL_NAME, DESC, URL, IMG_URL" \
                      ", ALT_IMG_URL, ALT_IMG_DESC, DETAILS" \
                      ", STANDARD_PRICE, SALES_PRICE, STATUS, CREATED, LAST_UPD)" \
                      " VALUES (:CATEGORY, :CATEGORY_URL, :NAME, :FULL_NAME, :DESC, :URL" \
                      ", :IMG_URL, :ALT_IMG_URL, :ALT_IMG_DESC, :DETAILS" \
                      ", :STANDARD_PRICE, :SALES_PRICE, 'ACTIVE' " \
                      ", DATETIME('NOW', 'LOCALTIME'), DATETIME('NOW', 'LOCALTIME'));"
                self.cursor.execute(sql_ins_prod, {"CATEGORY":str(item['category'].encode('utf-8'))
                    , "CATEGORY_URL":str(item['category_url'].encode('utf-8'))
                    , "NAME":str(item['name'][0].encode('utf-8')).strip()
                    , "FULL_NAME":str(item['full_name'][0].encode('utf-8')).strip()
                    , "DESC":str(item['desc'][0].encode('utf-8')).strip()
                    , "URL":str(item['url'][0].encode('utf-8'))
                    , "IMG_URL":str(item['img_url'][0].encode('utf-8'))
                    , "ALT_IMG_URL":str(item['alt_img_url'][0].encode('utf-8'))
                    , "ALT_IMG_DESC":str(item['alt_img_desc'][0].encode('utf-8'))
                    , "DETAILS":item['details'].strip()
                    , "STANDARD_PRICE":str(item['standard_price'][0].replace('$','').encode('utf-8'))
                    , "SALES_PRICE":str(item['sales_price'][0].replace('$','').encode('utf-8'))
                                  })
                prod_id = self.cursor.lastrowid

                sql_ins_color = "INSERT INTO TORY_COLOR" \
                                "(PAR_ROW_ID, NAME, URL, IMG_URL, CODE" \
                                ", CREATED, LAST_UPD)" \
                                " VALUES" \
                                " ('" + str(prod_id).encode('utf-8') + "'" \
                                ", :color, :url, :img_url, :col_code " \
                                ", DATETIME('NOW', 'LOCALTIME') " \
                                ", DATETIME('NOW', 'LOCALTIME'))"
                self.cursor.executemany(sql_ins_color, item['color'])

                sql_ins_price = "INSERT INTO TORY_PRICE(PAR_ROW_ID, STANDARD_PRICE, SALES_PRICE" \
                                ", CREATED, LAST_UPD) VALUES (:PAR_ROW_ID, :STANDARD_PRICE, :SALES_PRICE" \
                                ", DATETIME('NOW', 'LOCALTIME'), DATETIME('NOW', 'LOCALTIME'));"
                self.cursor.execute(sql_ins_price, {"PAR_ROW_ID": prod_id
                    , "STANDARD_PRICE": str(item['standard_price'][0].replace('$','').encode('utf-8'))
                    , "SALES_PRICE": str(item['sales_price'][0].replace('$','').encode('utf-8'))})
                self.conn.commit()
            except sqlite3.Error, e:
                print "Error %d: %s" % (e.args[0], e.args[1])
                return item
        # self.conn.close()