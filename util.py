import sqlite3
import json

def get_database_connection() -> sqlite3.Connection:
    '''
    데이터베이스 커넥션을 가져옵니다
    '''
    conn = sqlite3.connect(
        database='data/stock-me-up.db'
    )
    
    return conn


def get_key(api_code) -> str:
    '''
    API 사용에 필요한 key를 가져옵니다
    '''
    key = json.loads(open('keys.json').read())[api_code]
    return key