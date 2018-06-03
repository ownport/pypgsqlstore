
# Original code: https://github.com/addok/addok-psql-store

import os
import logging

import psycopg2
from psycopg2 import pool
from psycopg2.extras import execute_values

# from addok.config import config

from pypgsqlstore import schema
from pypgsqlstore.conf import DEFAULT_CONFIG
from pypgsqlstore.conf import prepare_dsn

logger = logging.getLogger(__name__)


class Storage():

    def __init__(self, **kwargs):

        self._config = dict()
        if not kwargs:
            self._config = DEFAULT_CONFIG
        else:
            self._config = kwargs

        try:
            self.pool = pool.SimpleConnectionPool(
                            minconn = self._config.get('pool.connection.min', DEFAULT_CONFIG.get('pool.connections.min')),
                            maxconn = self._config.get('pool.connection.max', DEFAULT_CONFIG.get('pool.connections.max')),
                            dsn     = prepare_dsn(self._config)
            )
        except psycopg2.OperationalError as err:
            logger.info(err)
            raise IOError(err)

        create_table_query = schema.SQL_CREATE_TABLE.format(self._config)
        create_index_query = schema.SQL_CREATE_INDEX.format(self._config)
        
        with self.getconn() as conn, conn.cursor() as curs:
            curs.execute(create_table_query)
            curs.execute(create_index_query)

    def getconn(self):
        # Use pid as connection id so we can reuse the connection within the
        # same process.
        return self.pool.getconn(key=os.getpid())

    def fetch(self, *keys):
        # Using ANY results in valid SQL if `keys` is empty.
        select_query = schema.SQL_FETCH_DATA.format(self._config)
        with self.getconn() as conn, conn.cursor() as curs:
            curs.execute(select_query, ([key.decode() for key in keys],))
            for key, data in curs.fetchall():
                yield key.encode(), data

    def upsert(self, *docs):
        """
        Potential performance boost, using copy_from:
        * https://gist.github.com/jsheedy/efa9a69926a754bebf0e9078fd085df6
        * https://gist.github.com/jsheedy/ed81cdf18190183b3b7d

        Or event copy_expert for mixed binary content:
        * http://stackoverflow.com/a/8150329
        """
        insert_into_query = schema.SQL_INSERT_DATA.format(self._config)
        with self.getconn() as conn, conn.cursor() as curs:
            execute_values(curs, insert_into_query, docs)

    def remove(self, *keys):
        delete_from_query = schema.SQL_DELETE_DATA.format(self._config)
        with self.getconn() as conn, conn.cursor() as curs:
            curs.executemany(delete_from_query, (keys, ))

    def flushdb(self):
        drop_table_query = schema.SQL_DROP_TABLE.format(self._config)
        with self.getconn() as conn, conn.cursor() as curs:
            curs.execute(drop_table_query)
