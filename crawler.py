import json
import logging
from logging import DEBUG
import requests
from io import BytesIO
import zipfile

from lxml import etree

import util


class BaseCrawler():
    '''
    기본이 되는 Crawler
    
    지원 기능
    - logging 설정
    '''

    def __init__(self, logging_level=logging.DEBUG) -> None:
        '''
        BaseCrawler를 초기화합니다
        '''
        self.logger = self._get_logger(self.__class__.__name__, logging_level)
    
    
    def _get_logger(self, name, level) -> logging.Logger:
        '''
        logger를 생성합니다
        '''
        
        logger = logging.getLogger(name)
        logger.setLevel(level)
        
        handler = logging.StreamHandler()
        handler.setLevel(level)
        
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)-7s - %(message)s')
        handler.setFormatter(formatter)
        
        if not logger.hasHandlers():
            logger.addHandler(handler)
        
        return logger


class DARTCrawler(BaseCrawler):
    '''
    DART에서 정보를 수집하는 크롤러
    '''
    
    
    def __init__(self, logging_level=logging.DEBUG) -> None:
        '''
        DARTCrawler 클래스를 초기화합니다
        '''
        super().__init__(logging_level=logging_level)
        
        self.base_url = 'https://opendart.fss.or.kr/api/'
        self.key = json.loads(open('keys.json').read())['dart']
        
        self.conn = util.get_database_connection()
        self.logger.debug('Database Connection Created')
        
        self.logger.debug('Initialization Done')
        
    
    def __del__(self):
        self.conn.close()
        self.logger.debug('Database Connection Closed')


    def get_corp_code(self) -> None:
        '''
        DART에 등록되어있는 공시대상회사 중 주식시장에 등록된 회사의 고유번호, 회사명, 종목코드, 최근변경일자를 가져옵니다
        '''
        self.logger.debug('get_corp_code Started')
        
        url = 'corpCode.xml'
        param = {'crtfc_key': self.key}
        self.logger.debug('Key Load Completed')
        
        res = requests.get(
            self.base_url + url,
            params=param
        )
        self.logger.debug('GET corpCode Done - {res.status_code}')
        
        if res.status_code != 200:
            self.logger.error(f'Response Failed - {res.status_code}')
            return
        
        zip_file = BytesIO(res.content)
        zip_ref = zipfile.ZipFile(zip_file)
        self.logger.debug('Zip File Extracted')
        
        corp_code_xml = etree.fromstring(zip_ref.read('CORPCODE.xml'))
        
        corp_codes = list()
        for l in corp_code_xml.getchildren():
            stock_code = l.find('stock_code').text

            if stock_code != ' ':
                corp_code = l.find('corp_code').text
                corp_name = l.find('corp_name').text
                modify_date = l.find('modify_date').text
                
                curr_d = dict()
                curr_d['corp_code'] = corp_code
                curr_d['corp_name'] = corp_name
                curr_d['stock_code'] = stock_code
                curr_d['modify_date'] = modify_date

                corp_codes.append((corp_code, corp_name, stock_code, modify_date))
        self.logger.debug('Corp Code Parsed')
                
        self.conn.executemany('insert or replace into dart_corp_code values (?, ?, ?, ?)', corp_codes)
        self.conn.commit()
        self.logger.debug('Corp Code Updated')
        
        return
                
                
  
    
    
class KRXCrawler(BaseCrawler):
    '''
    KRX에서 정보를 수집하는 크롤러
    '''
    
    
    def __init__(self, logging_level=logging.DEBUG) -> None:
        '''
        KRXCrawler를 초기화합니다
        '''
        super().__init__(logging_level)
        