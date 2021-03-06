# -*- coding: UTF-8 -*-
"""
订单页面所有的数据库操作
"""
import sqlite3
import traceback
from flask import session
from webapp.mylog import log

__author__ = 'sonnyhcl'


class Order(object):
    def add_order(self, o_amount, o_note, p_id, c_id):
        conn = sqlite3.connect("demo.db")
        param = (o_amount, o_note, p_id, c_id,)
        try:
            conn.execute('INSERT INTO orders(o_amount, o_note, p_id, c_id)'
                         'VALUES (?, ?, ?, ?);', param)
        except Exception:
            conn.close()
            return "Fail", traceback.print_exc()
        conn.commit()
        conn.close()
        return "Success", ""

    def delete_order(self, o_id):
        conn = sqlite3.connect("demo.db")
        param = (o_id,)
        try:
            conn.execute('DELETE FROM orders WHERE o_id = ?;', param)
        except Exception:
            conn.close()
            return "Fail", traceback.print_exc()
        conn.commit()
        conn.close()
        return "Success", ""

    def update_order(self, o_id, o_amount, o_note, p_id, c_id):
        conn = sqlite3.connect("demo.db")
        try:
            param = (o_amount, o_note, p_id, c_id, o_id)
            conn.execute(
                'UPDATE orders '
                'SET o_amount = ?, o_note = ?, p_id = ? ,c_id = ?'
                'WHERE o_id = ?;',
                param)
        except Exception:
            conn.close()
            return "Fail", traceback.print_exc()
        conn.commit()
        conn.close()
        return "Success", ""

    def get_order_by_cid(self, c_id):
        conn = sqlite3.connect("demo.db")
        param = (c_id,)
        try:
            if c_id == 0:
                response = conn.execute('SELECT * '
                                        'FROM orders, product, community '
                                        'WHERE orders.p_id = product.p_id '
                                        'AND orders.c_id = community.c_id;')
            else:
                response = conn.execute('SELECT * '
                                        'FROM orders, product, community '
                                        'WHERE orders.p_id = product.p_id '
                                        'AND orders.c_id = community.c_id '
                                        'AND orders.c_id = ?;', param)
            response = response.fetchall()
        except Exception:
            conn.close()
            return "Fail", traceback.print_exc()

        conn.close()
        return "Success", response


order = Order()
