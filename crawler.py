import json
import logging
import requests
from io import BytesIO
import zipfile
import time, random

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
        self.logger.debug('Logger Created')
        
        self.conn = util.get_database_connection()
        self.logger.debug('Database Connection Created')
    
    
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
        self.key = util.get_key('dart')
        
        ## 1분기보고서 : 11013 / 반기보고서 : 11012 / 3분기보고서 : 11014 / 사업보고서 : 11011
        self.report_codes = [11013, 11012, 11014, 11011]
        
        self.logger.debug('Initialization Done')
        
    
    def __del__(self):
        self.conn.close()
        self.logger.debug('Database Connection Closed')
        
        
    def crawl(self):
        '''
        기본적으로 DART에서 수집해야 할 정보를 수집합니다
        
        순서 : corp_code -> company -> financial statement
        '''
        
        self.get_corp_code()
        self.get_company()
        # TODO: financial statement


    def get_corp_code(self) -> None:
        '''
        DART에 등록되어있는 공시대상회사 중 주식시장에 등록된 회사의 고유번호, 회사명, 종목코드, 최근변경일자를 가져옵니다
        '''
        self.logger.debug('get_corp_code Started')
        
        url = 'corpCode.xml'
        param = {'crtfc_key': self.key}
        
        res = requests.get(
            self.base_url + url,
            params=param,
        )
        self.logger.debug(f'GET corpCode Done - {res.status_code}')
        
        if res.status_code != 200:
            self.logger.error(f'Response Failed : res.status_code -  {res.status_code}')
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

                corp_codes.append((corp_code, corp_name, stock_code, modify_date))

        self.logger.debug('Corp Code Parsed')
                
        self.conn.executemany('insert or replace into dart_corp_code values (?, ?, ?, ?)', corp_codes)
        self.conn.commit()
        self.logger.debug('get_corp_code Done')
        
        return
    
    
    def get_company(self) -> None:
        '''
        DART에 등록되어있는 기업의 개황정보를 가져옵니다
        
        dart_corp_code에 있는 업데이트 날짜(modify_date)와 dart_company에 있는 업데이트 날짜(modyfy_date)를 비교하여 업데이트 합니다
        '''
        self.logger.debug('get_company Started')
        
        url = 'company.json'
        
        cursor = self.conn.cursor()
        query_to_find_target = '''
        SELECT
            dart_corp_code.corp_code ,
            dart_corp_code.modify_date ,
            dart_company.modify_date AS dart_company_modify_date
        FROM 
            dart_corp_code
            left join
            dart_company 
            ON dart_corp_code.corp_code  = dart_company.corp_code
        WHERE
            dart_company.modify_date is NULL
            OR dart_corp_code.modify_date > dart_company.modify_date 
        '''
        cursor.execute(query_to_find_target)
        targets = cursor.fetchall()
        self.logger.debug('Getting Targets Done')
        
        query_to_insert = 'insert or replace into dart_company values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
        
        for corp_code, modify_date, __ in targets:
            param = {'crtfc_key': self.key, 'corp_code': corp_code}
            
            res = requests.get(
                self.base_url + url,
                params=param
            )
            if res.status_code != 200:
                self.logger.error(f'Response Failed : res.status_code -  {res.status_code}')
                return
            
            data = res.json()
            if data['status'] != '000':
                self.logger.error(f'Response Failed : data[\'status\'] -  {data['status']}')
                return
            self.logger.debug(f'GET company Done (corp_code: {corp_code})')
        
            curr_d = list()
            curr_d.append(corp_code)
            curr_d.append(data['corp_name'])
            curr_d.append(data['corp_name_eng'])
            curr_d.append(data['stock_name'])
            curr_d.append(data['stock_code'])
            curr_d.append(data['ceo_nm'])
            curr_d.append(data['corp_cls'])
            curr_d.append(data['jurir_no'])
            curr_d.append(data['bizr_no'])
            curr_d.append(data['adres'])
            curr_d.append(data['hm_url'])
            curr_d.append(data['ir_url'])
            curr_d.append(data['phn_no'])
            curr_d.append(data['fax_no'])
            curr_d.append(data['induty_code'])
            curr_d.append(data['est_dt'])
            curr_d.append(data['acc_mt'])
            curr_d.append(modify_date)

            self.conn.execute(query_to_insert, tuple(curr_d))
            self.conn.commit()

            self.logger.debug(f'company Updated (corp_code: {corp_code})')
            
            # Exceeding Request Rate 에러 발생으로 0~0.1초 사이 랜덤으로 sleep 로직 추가
            time.sleep(random.random() / 10)
            
        self.logger.debug('get_company Done')
                

    def get_financial_statement(self, corp_code, year, report_code, fs_div) -> dict:
        '''
        단일 회사의 정기보고서 내에 XBRL재무제표의 모든계정과목을 가져옵니다 (재무제표/연결재무제표 모두 저장)
        '''
        self.logger.debug(f'get_financial_statement Started - corp_code: {corp_code}, year: {year}, report_code: {report_code}, fs_div: {fs_div}')
        
        url = 'fnlttSinglAcntAll.json'
        
        result = list()
        param = {'crtfc_key': self.key, 'corp_code': corp_code, 'bsns_year': year, 'reprt_code': report_code, 'fs_div': fs_div}
        res = requests.get(
            self.base_url + url,
            params=param
        )
        if res.status_code != 200:
            self.logger.error(f'Response Failed : res.status_code -  {res.status_code}')
            return
        
        data = res.json()
        if data['status'] == '013':
            self.logger.warning(f'Response Failed : {data['message']} (corp_code: {corp_code}, year: {year}, report_code: {report_code}), fs_div: {fs_div}')
            
            # 없는 회사 null로 채워넣음
            self.conn.execute(
                'insert or replace into dart_financial_statement values (null, ?, ?, ?, ?, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null)',
                (corp_code, year, report_code, fs_div)
            )
            self.conn.commit()
            self.logger.debug('Insert Done')
            
            return
        elif data['status'] != '000':
            self.logger.error(f'Response Failed : data[\'status\']:  {data['status']}, data[\'message\']:  {data['message']}')
            return
        self.logger.debug(f'GET financial statement Done')
    
        for d in data['list']:
            curr_d = list()
            curr_d.append(d.get('rcept_no', None))
            curr_d.append(d.get('corp_code', None))
            curr_d.append(d.get('bsns_year', None))
            curr_d.append(d.get('reprt_code', None))
            curr_d.append(fs_div)
            curr_d.append(d.get('sj_div', None))
            curr_d.append(d.get('sj_nm', None))
            curr_d.append(d.get('account_id', None))
            curr_d.append(d.get('account_nm', None))
            curr_d.append(d.get('account_detail', None))
            curr_d.append(d.get('thstrm_nm', None))
            curr_d.append(d.get('thstrm_amount', None))
            curr_d.append(d.get('thstrm_add_amount', None))
            curr_d.append(d.get('frmtrm_nm', None))
            curr_d.append(d.get('frmtrm_amount', None))
            curr_d.append(d.get('frmtrm_q_nm', None))
            curr_d.append(d.get('frmtrm_q_amount', None))
            curr_d.append(d.get('frmtrm_add_amount', None))
            curr_d.append(d.get('bfefrmtrm_nm', None))
            curr_d.append(d.get('bfefrmtrm_amount', None))
            curr_d.append(d.get('ord', None))
            curr_d.append(d.get('currency', None))
            
            result.append(curr_d)
        
        query_to_insert = 'insert or replace into dart_financial_statement values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
            
        self.conn.executemany(query_to_insert, result)
        self.conn.commit()
        self.logger.debug('Insert Done')
        
        self.logger.debug('get_financial_statement Done')
        
        
        
    def get_entire_financial_statements(self, year, report_code):
        '''
        전체 회사의 정기보고서 내의 XBRL재무제표의 주요계정과목(재무상태표, 손익계산서)를 가져옵니다 (재무제표/연결재무제표 모두 저장)
        '''
        self.logger.debug(f'get_entire_financial_statements Started - year: {year}, report_code: {report_code}')
        
        cursor = self.conn.cursor()
        
        # OFS:재무제표, CFS:연결재무제표
        for fs_div in ['OFS', 'CFS']:
        
            query_to_find_target = f'''
            SELECT
                dart_corp_code.corp_code,
                krx_company.corp_code AS stock_code,
                krx_company.market_type,
                krx_company.corp_name
            FROM
                krx_company
                left join
                dart_corp_code
                ON krx_company.corp_code = dart_corp_code.stock_code
                LEFT JOIN
                (SELECT
                    corp_code, bsns_year, reprt_code
                FROM
                    dart_financial_statement
                WHERE 
                    bsns_year = '{year}'
                    AND reprt_code = '{report_code}'
                    AND fs_div = '{fs_div}'
                GROUP BY
                    corp_code, bsns_year, reprt_code) fs
                ON dart_corp_code.corp_code = fs.corp_code
            WHERE
                fs.corp_code IS NULL
            '''
        
            cursor.execute(query_to_find_target)
            targets = cursor.fetchall()
            self.logger.debug('Getting Targets Done')
            
            for corp_code, stock_code, market_type, corp_name in targets:
                self.get_financial_statement(corp_code, year, report_code, fs_div)
                
                # Exceeding Request Rate 에러 발생으로 0~0.1초 사이 랜덤으로 sleep 로직 추가
                time.sleep(random.random() / 10)
        
        return
        
        
    
    
class KRXCrawler(BaseCrawler):
    '''
    KRX에서 정보를 수집하는 크롤러
    '''
    
    
    # FIXME: 수정 필요
    def __init__(self, logging_level=logging.DEBUG) -> None:
        '''
        KRXCrawler를 초기화합니다
        '''
        super().__init__(logging_level=logging_level)
        
        self.base_url = 'https://opendart.fss.or.kr/api/'
        self.key = util.get_key('krx')
        
        self.logger.debug('Initialization Done')
        