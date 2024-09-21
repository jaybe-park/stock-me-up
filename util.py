import sqlite3


def get_database_connection() -> sqlite3.Connection:
    '''
    데이터베이스 커넥션을 가져옵니다
    '''
    conn = sqlite3.connect(
        database='data/stock-me-up.db'
    )
    
    return conn