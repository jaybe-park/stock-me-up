# DART
## dart_corp_code
- DART에 등록되어있는 공시대상회사의 고유번호에 대한 데이터

| 컬럼        | 자료형 | 의미         | 설명                                    | 비고          |
|-------------|--------|--------------|-----------------------------------------|---------------|
| corp_code   | text   | 고유번호     | 공시대상회사의 고유번호(8자리)           | Primary Key   |
| corp_name   | text   | 정식명칭     | 정식회사명칭                            |               |
| stock_code  | text   | 종목코드     | 상장회사인 경우 주식의 종목코드(6자리)   |               |
| modify_date | text   | 최종변경일자 | 기업개황정보 최종변경일자(YYYYMMDD)      |               |

## dart_company
- DART 기반 기업의 개황정보

| 컬럼         | 자료형 | 의미                                              | 설명                                         | 비고          |
|--------------|--------|---------------------------------------------------|----------------------------------------------|---------------|
| corp_name    | text   | 정식명칭                                           | 정식회사명칭                                 | Primary Key   |
| corp_name_eng| text   | 영문명칭                                           | 영문정식회사명칭                             |               |
| stock_name   | text   | 종목명(상장사) 또는 약식명칭(기타법인)              | 종목명(상장사) 또는 약식명칭(기타법인)        |               |
| stock_code   | text   | 상장회사인 경우 주식의 종목코드                    | 상장회사의 종목코드(6자리)                   |               |
| ceo_nm       | text   | 대표자명                                           | 대표자명                                     |               |
| corp_cls     | text   | 법인구분                                           | 법인구분 : Y(유가), K(코스닥), N(코넥스), E(기타) |               |
| jurir_no     | text   | 법인등록번호                                       | 법인등록번호                                 |               |
| bizr_no      | text   | 사업자등록번호                                     | 사업자등록번호                               |               |
| adres        | text   | 주소                                               | 주소                                         |               |
| hm_url       | text   | 홈페이지                                           | 홈페이지                                     |               |
| ir_url       | text   | IR홈페이지                                         | IR홈페이지                                   |               |
| phn_no       | text   | 전화번호                                           | 전화번호                                     |               |
| fax_no       | text   | 팩스번호                                           | 팩스번호                                     |               |
| induty_code  | text   | 업종코드                                           | 업종코드                                     |               |
| est_dt       | text   | 설립일(YYYYMMDD)                                   | 설립일(YYYYMMDD)                             |               |
| acc_mt       | text   | 결산월(MM)                                         | 결산월(MM)                                   |               |

> [!주의]  
> DART에서의 corp_code는 DART 고유의 기업 코드  
> KRX에서의 corp_code는 ticker이며, dart에서는 stock_code랑 조인해야 함

# KRX
## krx_company

- [링크](http://data.krx.co.kr/contents/MDC/MDI/mdiLoader/index.cmd?menuId=MDC0201020501)에서 다운받아 수동으로 만든 테이블
- 나중에 자동으로 가져오게 수정해야 함
- 액면가가 KRW가 아니거나, 무액면인 기업은 일단 제외함

| 컬럼         | 자료형 | 의미           | 설명                | 비고         |
|--------------|--------|----------------|---------------------|--------------|
| corp_code    | text   | 기업 고유번호  | DART에서의 종목코드 | Primary Key  |
| corp_name    | text   | 기업 이름      |                     |              |
| market_type  | text   | 시장 이름      | KOSPI/KOSDAQ/KONEX   |              |
| industry_code| text   | 업종 코드      |                     |              |
| industry_name| text   | 업종 이름      |                     |              |
| settle_month | integer| 결산월         |                     |              |
| stock_count  | integer| 총 주식 수     |                     |              |
| par_value    | integer| 액면가         |                     |              |