# dart_corp_code


# dart_company
- DART 기반 기업의 정보를 저장하는 테이블


> [!주의]
> DART에서의 corp_code는 DART 고유의 기업 코드
> KRX에서의 corp_code는 ticker이며, dart에서는 stock_code랑 조인해야 함


# krx_company

- [링크](http://data.krx.co.kr/contents/MDC/MDI/mdiLoader/index.cmd?menuId=MDC0201020501)에서 다운받아 수동으로 만든 테이블
- 나중에 자동으로 가져오게 수정해야 함
- 액면가가 KRW가 아니거나, 무액면인 기업은 일단 제외함
