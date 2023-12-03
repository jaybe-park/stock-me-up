from datetime import datetime
import requests

import conf

URL = conf.get_url('data_go_kr_stock')
KEY = conf.get_key('data_go_kr_stock')


def get_prices(date_id: str = None):
    """Get Stock Prices for Specific Date
    
    Args:
        date_id: YYY-MM-DD (ex. 2023-01-01) / If null, today
    """

    if date_id is None:
        date_id = datetime.today().strftime('%Y-%m-%d')

    url = URL + '/getStockPriceInfo'

    # totalCount
    params = dict()
    params['serviceKey'] = KEY
    params['numOfRows'] = 10
    params['resultType'] = 'json'

    res = requests.get(
        url=url,
        params=params
    )
    data = res.json()
    total_count = data['response']['body']['totalCount']


    # data
    params['numOfRows'] = total_count

    res = requests.get(
        url=url,
        params=params
    )
    data = res.json()

    result = data['response']['body']['items']['item']

    return result
