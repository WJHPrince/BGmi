# coding=utf-8
import os
import sqlite3
from collections import defaultdict


STATUS_NORMAL = 0
STATUS_FOLLOWED = 1
STATUS_REMOVED = 2

DB_PATH = os.path.join(os.path.dirname(__file__), '../bangumi.db')


class DB(object):
    _id = None
    fields = ()
    table = None
    conn = None

    @staticmethod
    def _make_sql(method, table, fields=None, data=None, select=None, condition=None):
        if method not in ('select', 'update', 'delete', 'insert'):
            raise Exception('unexpected operation %s' % method)

        if not isinstance(condition, (type(None), tuple, list, set, str)):
            raise Exception('`condition` expected sequences')

        if not isinstance(select, (type(None), tuple, list, set, str)):
            raise Exception('`select` expected sequences or string')

        if not isinstance(table, str):
            raise Exception('unexpected type %s of table' % type(table))

        def make_condition(condition, operation='AND'):
            sql = ''
            if isinstance(condition, (tuple, list, set)):
                for f in condition:
                    sql += '`%s`=? %s ' % (f, operation)
                sql = sql[:-(len(operation)+1)]
            elif isinstance(condition, str):
                sql += '`%s`=?' % condition
            else:
                sql += '1'
            return sql

        def make_fields(fields):
            sql = ''
            for f in fields:
                sql += '`%s`,' % f
            sql = sql[:-1]
            return sql

        if method == 'insert':
            sql = 'INSERT INTO %s ' % table
            if fields is not None:
                sql += '(%s)' % make_fields(fields)

            sql += ' VALUES ('
            for i in range(len(fields)):
                sql += '?,'
            sql = sql[:-1]
            sql += ')'

        elif method == 'select':

            if select is None:
                select = '*'
            else:
                if not isinstance(select, str):
                    f = ''
                    for f in select:
                        f += '`%s`,' % select
                    select = f[:-1]
                else:
                    select = '`%s`' % select

            sql = 'SELECT %s FROM `%s` WHERE ' % (select, table)
            sql += make_condition(condition)

        elif method == 'update':
            sql = 'UPDATE %s SET ' % table
            if fields is not None:
                sql += make_condition(fields, ',')
            else:
                raise Exception('unexpected UPDATE null fields')

            sql += ' WHERE '
            sql += make_condition(condition)
        else:
            sql = ''

        return sql

    def _unicodeize(self):
        for i in self.fields:
            v = self.__dict__.get(i, '')
            if isinstance(v, str):
                v = unicode(v.decode('utf-8'))
                self.__dict__[i] = v

    @staticmethod
    def connect_db():
        return sqlite3.connect(DB_PATH)

    @staticmethod
    def close_db(db_instance):
        db_instance.commit()
        db_instance.close()

    def _connect_db(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()

    def _close_db(self):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    def _pair(self):
        values = tuple([self.__dict__.get(i, '') for i in self.fields])
        return self.fields, values

    def select(self, condition=None, one=False):
        if not isinstance(condition, (dict, type(None))):
            raise Exception('condition expected dict')
        if condition is None:
            if self._id is None:
                k = []
                v = []
                for i in self.fields:
                    if self.__dict__.get(i, None):
                        k.append(i)
                        v.append(self.__dict__.get(i))
            else:
                k, v = ('id', ), (self._id, )
        else:
            k, v = condition.keys(), condition.values()

        self._connect_db()
        sql = Bangumi._make_sql('select', table=self.table, condition=k)
        self.cursor.execute(sql, v)
        ret = self.cursor.fetchall() if not one else self.cursor.fetchone()
        self._close_db()

        return ret

    def update(self, data=None):
        obj = self.select(one=True)
        if obj:
            self._id = obj['id']
        else:
            raise Exception('%s not exist' % self.__repr__())

        if not isinstance(data, (dict, type(None))):
            raise Exception('update data expected dict')

        if data is None:
            data = {}
            for i in self.fields:
                data.update({i: self.__dict__.get(i, '')})

        sql = self._make_sql('update', self.table, fields=data.keys(), condition=('id', ))
        self._connect_db()
        params = data.values()
        params.append(self._id)
        self.cursor.execute(sql, params)
        self._close_db()


class Bangumi(DB):
    table = 'bangumi'
    fields = ('name', 'update_time', 'subtitle_group', 'status')
    week = ('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun')

    def __init__(self, **kwargs):
        if 'name' not in kwargs:
            raise ValueError('bangumi name required')
        self.name = kwargs.get('name')
        update_time = kwargs.get('update_time', '').title()
        if update_time not in self.week:
            raise ValueError('unexcept update time %s' % update_time)
        self.update_time = update_time
        self.subtitle_group = ', '.join(kwargs.get('subtitle_group', []))
        self.status = kwargs.get('status', STATUS_NORMAL)

        self._unicodeize()

    def save(self):
        _f, _v = self._pair()

        obj = self.select(one=True)
        if obj:
            self._id = obj['id']
            self.update()
            return self

        self._connect_db()
        sql = self._make_sql('insert', self.table, _f)
        self.cursor.execute(sql, _v)
        self._id = self.cursor.lastrowid
        self._close_db()

        return self

    def __repr__(self):
        return self.name

    def __str__(self):
        return 'Bangumi<%s>' % self.name

    @staticmethod
    def get_all_bangumi(status=None):
        db = Bangumi.connect_db()
        db.row_factory = sqlite3.Row
        cur = db.cursor()
        if status is None:
            sql = Bangumi._make_sql('select', table=Bangumi.table)
            cur.execute(sql)
        else:
            sql = Bangumi._make_sql('select', table=Bangumi.table, condition='status')
            cur.execute(sql, (status, ))
        data = cur.fetchall()
        Bangumi.close_db(db)

        weekly_list = defaultdict(list)

        for bangumi_item in data:
            weekly_list[bangumi_item['update_time'].lower()].append(dict(bangumi_item))

        return weekly_list