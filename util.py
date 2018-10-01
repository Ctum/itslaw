from config import get_header
import requests
import json
import urllib
query = {
    'startIndex': 0,
    'countPerPage': 20,
    'sortType': 1,
    'conditions': ['searchWord+法院+1+法院', 'trialYear+2018+7+2018'],
    'searchView': 'text'
}
url = 'https://www.itslaw.com/api/v1/caseFiles'
header = get_header()
header['Referer'] = 'https://www.itslaw.com/search?searchMode=judgements&sortType=1&conditions=searchWord%2B%E6%B3%95%E9%99%A2%2B1%2B%E6%B3%95%E9%99%A2&searchView=text'


def get_first():
    try:
        res = requests.get(url=url, headers=header, params=query)
    except Exception as err:
        print(err)
        exit(-1)
    count = json.loads(res.text).get('data').get('searchResult').get('totalCount')
    res_arr = json.loads(res.text).get('data').get('searchResult').get('judgements')
    return {
        'id': res_arr[0].get('id'),
        'next_id': res_arr[1].get('id'),
        'area': 0,
        'next_area': 0,
        'count': count,
    }


def url_encode(url, params):
    '''
    编码字符串，用做refer
    :param url:
    :param params:
    :return:
    '''
    str_con = url
    conditions = params['conditions']
    del params['conditions']
    str_con += urllib.parse.urlencode(params)
    for item in conditions:
        str_con += '&conditions='
        str_con += urllib.parse.quote(item)
    return str_con


if __name__ == "__main__":
    get_first()
