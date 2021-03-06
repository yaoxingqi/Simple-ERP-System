# -*- coding: UTF-8 -*-
"""
流水页面所有数据库的操作
"""
import traceback
import sqlite3

__author__ = 'sonnyhcl'


class Transactions(object):
    def add_transactions(self, m_id, amount, t_note):
        conn = sqlite3.connect("demo.db")
        param = (m_id, amount, t_note)
        try:
            conn.execute(
                'INSERT INTO transactions(m_id, t_amount, t_note) '
                'VALUES (?, ?, ?);',
                param)
        except Exception:
            conn.close()
            return "Fail", traceback.print_exc()
        conn.commit()
        conn.close()
        return "Success", ""

    def delete_transactions(self, t_id):
        conn = sqlite3.connect("demo.db")
        param = (t_id,)
        try:
            conn.execute('DELETE FROM transactions WHERE t_id = ?;', param)
        except Exception:
            conn.close()
            return "Fail", traceback.print_exc()
        conn.commit()
        conn.close()
        return "Success", ""

    def update_transactions(self, t_id, t_amount=None, t_note=None):
        conn = sqlite3.connect("demo.db")
        param = (t_id,)
        try:
            response = conn.execute(
                'SELECT * FROM transactions WHERE t_id = ?;', param)
            origin = response.fetchall()[0]
            origin = list(origin)
            if t_amount is not None:
                origin[1] = t_amount
            if t_note is not None:
                origin[3] = t_note

            param = tuple(origin) + (t_id,)
            conn.execute(
                'UPDATE transactions '
                'SET t_id = ?, t_amount = ?, t_timestamp = ?, '
                't_note = ?, m_id = ?'
                'WHERE t_id = ?;',
                param)
        except Exception:
            conn.close()
            return "Fail", traceback.print_exc()
        conn.commit()
        conn.close()
        return "Success", ""

    def get_transactions(self, t_id):
        conn = sqlite3.connect("demo.db")
        param = (t_id,)
        try:
            response = conn.execute(
                'SELECT * FROM transactions WHERE t_id = ?;',
                param)
            response = response.fetchall()
        except Exception:
            conn.close()
            return "Fail", traceback.print_exc()
        conn.close()
        return "Success", response

    def get_transactions_by_cid(self, c_id):
        conn = sqlite3.connect("demo.db")
        if c_id == 0:
            try:
                response = conn.execute('SELECT * '
                                        'FROM transactions, mission, orders, '
                                        'product, user, community, item '
                                        'WHERE transactions.m_id = mission.m_id'
                                        ' AND mission.o_id = orders.o_id '
                                        'AND mission.u_id = user.u_id '
                                        'AND mission.i_id = item.i_id '
                                        'AND orders.p_id = product.p_id '
                                        'AND orders.c_id = community.c_id;')
                response = response.fetchall()
            except Exception:
                conn.close()
                return "Fail", traceback.print_exc()
        else:
            param = (c_id,)
            try:
                response = conn.execute('SELECT * '
                                        'FROM transactions, mission, orders, '
                                        'product, user, community, item '
                                        'WHERE transactions.m_id = mission.m_id'
                                        ' AND mission.o_id = orders.o_id '
                                        'AND mission.u_id = user.u_id '
                                        'AND mission.i_id = item.i_id '
                                        'AND orders.p_id = product.p_id '
                                        'AND orders.c_id = community.c_id '
                                        'AND orders.c_id = ?;',
                                        param)
                response = response.fetchall()
            except Exception:
                conn.close()
                return "Fail", traceback.print_exc()

        conn.close()
        return "Success", response

    def get_transactions_by_uid(self, u_id):
        conn = sqlite3.connect("demo.db")
        param = (u_id,)
        try:
            response = conn.execute('SELECT * '
                                    'FROM transactions, mission, orders, '
                                    'product, user, community, item '
                                    'WHERE transactions.m_id = mission.m_id '
                                    'AND mission.o_id = orders.o_id '
                                    'AND mission.u_id = user.u_id '
                                    'AND mission.i_id = item.i_id '
                                    'AND orders.p_id = product.p_id '
                                    'AND orders.c_id = community.c_id '
                                    'AND user.u_id = ?;',
                                    param)
            response = response.fetchall()
        except Exception:
            conn.close()
            return "Fail", traceback.print_exc()
        conn.close()
        return "Success", response

    def get_all(self, ):
        conn = sqlite3.connect("demo.db")
        try:
            response = conn.execute('SELECT * FROM transactions;')
            response = response.fetchall()
        except Exception:
            conn.close()
            return "Fail", traceback.print_exc()
        conn.close()
        return "Success", response


transaction = Transactions()
