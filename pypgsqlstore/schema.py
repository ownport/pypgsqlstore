
SQL_CREATE_TABLE    = 'CREATE TABLE IF NOT EXISTS {tablename} (key VARCHAR COLLATE "C", data bytea);'
SQL_CREATE_INDEX    = 'CREATE UNIQUE INDEX IF NOT EXISTS {tablename}_key_idx ON {tablename} (key);'
SQL_FETCH_DATA      = 'SELECT key, data FROM {tablename} WHERE key=ANY(%s);'
SQL_INSERT_DATA     = 'INSERT INTO {tablename} (key, data) VALUES %s ON CONFLICT DO NOTHING;'
SQL_DELETE_DATA     = 'DELETE FROM {tablename} WHERE key=%s;'
SQL_DROP_TABLE      = 'DROP TABLE IF EXISTS {tablename};'
