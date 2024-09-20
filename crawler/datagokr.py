import json

class DataGoKrCrawler():
    '''
    공공데이터포털에서 정보를 수집하는 크롤러
    
    속성:
    - url : 수집하는 주소 (https://apis.data.go.kr/1160100/service/GetStockSecuritiesInfoService)
    - key : api 사용하기 위한 key (별도 파일에 보관됨)
    '''
    
    
    def __init__(self) -> None:
        '''
        DataGoKrCrawler 클래스를 초기화하는 함수
        '''
        self.base_url = 'https://apis.data.go.kr/1160100/service/GetStockSecuritiesInfoService'
        self.key = json.loads(open('keys.json').read())['data_go_kr']
        pass
