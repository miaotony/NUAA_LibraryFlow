#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
crawler.py

NUAA Library Flow Crawler
图书馆预约系统爬虫

@Author: MiaoTony
@CreateTime: 20200918
@UpdateTime: 20201004
"""

import requests
from bs4 import BeautifulSoup
import re
import json
import time
import random
import datetime
import multiprocessing


class Flow(object):
    """
    人流量类
    """

    def __init__(self):
        self.host = r"http://kjcx.nuaa.edu.cn"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0",
            "Accept": "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
        }
        # 明故宫图书馆二楼
        # 明故宫图书馆三楼
        # 明故宫图书馆四楼
        # 将军路图书馆二楼
        # 将军路图书馆三楼
        # 将军路图书馆四楼
        # 将军路图书馆五楼
        # 将军路图书馆六楼
        # 天目湖图书馆
        self.lib_id = {"MGG2F": "11",
                       "MGG3F": "12",
                       "MGG4F": "13",
                       "JJL2F": "15",
                       "JJL3F": "16",
                       "JJL4F": "17",
                       "JJL5F": "18",
                       "JJL6F": "19",
                       "TMH": "20"}
        # self.data = []

    def _get_booking_url(self, place, date):
        """
        Get the booking url of a specefic place.
        :param place: {str} 
        :param date: {str} 
        :return: url_booking {str}
        """
        # date_str = time.strftime("%Y-%m-%d", time.localtime())
        url_place = f"http://kjcx.nuaa.edu.cn/book/more/lib/{place}/type/4/day/{date}"
        retry_cnt = 4
        while retry_cnt > 0:
            resp = requests.get(url_place, headers=self.headers, timeout=10)
            resp.encoding = 'utf-8'
            # print(resp.text)
            soup = BeautifulSoup(resp.text, 'lxml')
            # 提取预约链接
            tag_url_booking = soup.select('a.btn.btn-info')[0]
            if tag_url_booking:
                url_booking = self.host + tag_url_booking['href']
                return url_booking
            retry_cnt -= 1
            time.sleep(random.uniform(0.4, 0.8))
        return None

    def _get_flow_from_url(self, url):
        """
        Get the flow of a specific place url.
        :param url: {str} The url of a specific booking page.
        :return: people_info {list} [current, total]
        """
        # url = r"http://kjcx.nuaa.edu.cn/book/notice/act_id/650/type/4/lib/12"  # debug
        if not url:
            raise Exception('URL is None...')
        retry_cnt = 4
        while retry_cnt > 0:
            resp = requests.get(url, headers=self.headers, timeout=10)
            resp.encoding = 'utf-8'
            # print(resp.text)
            re_people_num = re.compile(r'预约人数</b>：\[(\d+?)/(\d+?)\]')
            people_info = re_people_num.search(resp.text)
            if people_info:
                people_info = [people_info.group(1), people_info.group(2)]
                print(people_info)
                return people_info
            retry_cnt -= 1
            time.sleep(random.uniform(0.4, 0.8))
        return []

    def _run_job(self, q, place, date):
        try:
            print(place)
            place_id = self.lib_id[place]
            url = self._get_booking_url(place_id, date)
            info = self._get_flow_from_url(url)
            now = info[0]
            total = info[1]
        except Exception as e:
            print('\033[31m[ERROR]', e, '\033[0m')
            now = ''
            total = ''
        data_single = dict(area=place, now=now, all=total)
        q.put(data_single)
        return data_single

    def _read_job(self, q, rtn_list):
        while True:
            value = q.get(True)
            print('Get from queue:', str(value))
            rtn_list.append(value)

    def get_flow(self, date):
        """
        Convert the data to a JSON list.
        :param date: {str} 
        :return: data_all {dict} A dict of all libraries flow data.
        """
        data_all = []
        for place in self.lib_id:
            place_id = self.lib_id[place]
            try:
                url = self._get_booking_url(place_id, date)
                info = self._get_flow_from_url(url)
                now = info[0]
                total = info[1]
            except Exception as e:
                print('\033[31m[ERROR]', e, '\033[0m')
                now = ''
                total = ''
            data_single = dict(area=place, now=now, all=total)
            data_all.append(data_single)
        return data_all

    def get_flow_parallel(self, date):
        """
        Convert the data to a JSON list with multiprocessing.
        """
        cpu_count = multiprocessing.cpu_count()
        print("cpu: ", cpu_count)
        q = multiprocessing.Queue()
        manager = multiprocessing.Manager()
        return_list = manager.list()
        pr_job = multiprocessing.Process(
            target=self._read_job, args=(q, return_list))
        # 启动子进程pr，读取:
        pr_job.start()
        pw_jobs = []
        for place in self.lib_id:
            p = multiprocessing.Process(
                target=self._run_job, args=(q, place, date))
            pw_jobs.append(p)
            p.start()
            time.sleep(random.uniform(0.05, 0.15))
        for proc in pw_jobs:
            proc.join()
        # pr进程里是死循环，无法等待其结束，只能强行终止:
        pr_job.terminate()
        # self.data = list(return_list)
        return list(return_list)


if __name__ == "__main__":
    flow = Flow()
    time_start = time.time()
    # data = flow.get_flow(date='')
    data = flow.get_flow_parallel(date='')
    print(data)
    print(time.time()-time_start)
