
DEFAULT_CONFIG = {
    'host'      : 'localhost',
    'dbname'    : 'pypgsqlstore',
    'username'  : 'pypgsqlstore',
    'password'  : 'pypgsqlstore',
    'tablename' : 'docs',
    'pool.connections.min': 1,
    'pool.connections.max': 3,
}

def prepare_dsn(config):

    return 'host={host} dbname={dbname} user={username} password={password}'.format(
        host        = config.get('host', None),
        dbname      = config.get('dbname', None),
        username    = config.get('username', None),
        password    = config.get('password', None),
    )
