import json
import logging
import requests
from io import BytesIO
import zipfile

from lxml import etree

class DARTCrawler():
    '''
    DART에서 정보를 수집하는 크롤러
    
    Attributes:
    - key : api 사용하기 위한 key (별도 파일에 보관됨)
    '''
    
    
    def __init__(self) -> None:
        '''
        DARTCrawler 클래스를 초기화합니다
        '''
        self.base_url = 'https://opendart.fss.or.kr/api/'
        self.key = json.loads(open('keys.json').read())['dart']
        
        self.logger = self._get_logger(self.__class__.__name__)
        
    
    def _get_logger(self, name, level=logging.DEBUG) -> logging.Logger:
        '''
        logger를 생성합니다
        
        Args:
            name (string): logger의 이름 (주로 클래스명)
            level (string, optional): logger의 레벨 (default: DEBUG)
        
        Returns:
            logging.Logger: 해당 클래스에서 사용할 logger
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
            


    def get_corp_code(self):
        '''
        DART에 등록되어있는 공시대상회사 중 주식시장에 등록된 회사의 고유번호, 회사명, 종목코드, 최근변경일자를 가져옵니다
        '''
        self.logger.debug('get_corp_code Started')
        
        url = 'corpCode.xml'
        param = {'crtfc_key': self.key}
        
        res = requests.get(
            self.base_url + url,
            params=param
        )
        
        self.logger.debug('GET corpCode Done!')
        
        if res.status_code != 200:
            self.logger.error(f'Response Failed - {res.status_code}')
            return
        
        zip_file = BytesIO(res.content)
        zip_ref = zipfile.ZipFile(zip_file)
        
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

                corp_codes.append(curr_d)
        
        return corp_codes
                
                
                