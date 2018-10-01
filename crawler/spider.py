import requests
from config import get_header, TIME_OUT
from util import url_encode
import time
import json


class Spider:
    def __init__(self, db, proxy=False):
        self.db = db
        if proxy:
            # 开启代理
            self.proxy = ''
            pass
        else:
            self.proxy = False

    def __fetch_last(self):
        query_last_id = ('select * from id_queue order by uid desc limit 1')
        self.db.cursor.execute(query_last_id)
        return self.db.cursor.fetchone()

    def __refer(self):
        query_last_id_result = self.__fetch_last()
        params_dict = {
            'judgementId': query_last_id_result[1],
            'area': query_last_id_result[4],
            'index': query_last_id_result[0],
            'sortType': 1,
            'count': query_last_id_result[3],
            'conditions': ['searchWord+法院+1+法院', 'trialYear+2018+7+2018']
        }
        return url_encode('https://www.itslaw.com/detail?', params_dict)

    def __get_params(self):
        query_last_id_result = self.__fetch_last()
        return {
            'timestamp': round((time.time()-5) * 1000),
            'judgementId': query_last_id_result[1],
            'area': query_last_id_result[5],
            'sortType': 1,
            'conditions': 'searchWord+法院+1+法院,trialYear+2018+7+2018'
        }

    def start(self):
        retry = 10
        while True:
            headers = get_header()
            headers['Referer'] = self.__refer()
            params = self.__get_params()
            result = ''
            while True:
                try:
                    if self.proxy:
                        result = requests.get(url='https://www.itslaw.com/api/v1/detail', headers=headers, params=params,timeout=TIME_OUT)
                    else:
                        result = requests.get(url='https://www.itslaw.com/api/v1/detail', headers=headers, params=params,timeout=TIME_OUT)
                except requests.Timeout as err:
                    print('{} connect failed, retry'.format(11-retry))
                    result = 'timeout'
                    if retry == 0:
                        break
                    retry = retry - 1
                if result != 'timeout':
                    res_dict = json.loads(result.text)
                    judgement = res_dict.get('data').get('fullJudgement')
                    last_record = self.__fetch_last()
                    self.db.insert_id(judgement.get('id'), judgement.get('nextId'),
                                      last_record[3], last_record[5], judgement.get('nextArea'))
                    self.db.insert_detail(judgement.get('id'), str(judgement))
            if result == 'timeout':
                break
        print('end')
