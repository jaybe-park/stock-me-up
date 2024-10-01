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

FIXME: 컬럼 맞는지 확인하기
## dart_financial_statement
| 컬럼              | 의미               | 설명                                                                                           | 비고                            |
|-------------------|--------------------|------------------------------------------------------------------------------------------------|---------------------------------|
| rcept_no          | 접수번호            | 접수번호(14자리)                                                                                |                                 |
| reprt_code        | 보고서 코드         | 1분기보고서 : 11013, 반기보고서 : 11012, 3분기보고서 : 11014, 사업보고서 : 11011                 |                                 |
| bsns_year         | 사업 연도           | 2018                                                                                           |                                 |
| corp_code         | 고유번호            | 공시대상회사의 고유번호(8자리)                                                                  |                                 |
| sj_div            | 재무제표구분        | BS : 재무상태표, IS : 손익계산서, CIS : 포괄손익계산서, CF : 현금흐름표, SCE : 자본변동표         |                                 |
| sj_nm             | 재무제표명          | ex) 재무상태표 또는 손익계산서 출력                                                             |                                 |
| account_id        | 계정ID              | XBRL 표준계정ID, 표준계정ID가 아닐 경우 ""-표준계정코드 미사용-"" 표시                          |                                 |
| account_nm        | 계정명              | ex) 자본총계                                                                                    |                                 |
| account_detail    | 계정상세            | ex) 자본 [member]|지배기업 소유주지분 - 자본 [member]|지배기업 소유주지분|기타포괄손익누계액 [member] | 자본변동표에만 출력             |
| thstrm_nm         | 당기명              | ex) 제 13 기                                                                                   |                                 |
| thstrm_amount     | 당기금액            | 분/반기 보고서이면서 (포괄)손익계산서일 경우 [3개월] 금액                                       |                                 |
| thstrm_add_amount | 당기누적금액        |                                                                                                |                                 |
| frmtrm_nm         | 전기명              | ex) 제 12 기말                                                                                 |                                 |
| frmtrm_amount     | 전기금액            |                                                                                                |                                 |
| frmtrm_q_nm       | 전기명(분/반기)     | ex) 제 18 기 반기                                                                               |                                 |
| frmtrm_q_amount   | 전기금액(분/반기)   | 분/반기 보고서이면서 (포괄)손익계산서일 경우 [3개월] 금액                                       |                                 |
| frmtrm_add_amount | 전기누적금액        |                                                                                                |                                 |
| bfefrmtrm_nm      | 전전기명            | ex) 제 11 기말 (사업보고서의 경우에만 출력)                                                     |                                 |
| bfefrmtrm_amount  | 전전기금액          | 사업보고서의 경우에만 출력                                                                      |                                 |
| ord               | 계정과목 정렬순서   | 계정과목 정렬순서                                                                               |                                 |
| currency          | 통화 단위           | 통화 단위                                                                                      |                                 |

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
