#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
crawler.py

NUAA Library Flow Crawler
图书馆预约系统爬虫

@Author: MiaoTony
@CreateTime: 20200918
"""

import requests
from bs4 import BeautifulSoup
import re
import json
import time
import random
import datetime


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
        self.data = {}

    def _get_booking_url(self, place, date):
        """
        Get the booking url of a specefic place.
        :param place: {str} 
        :param date: {str} 
        :return: url_booking {str}
        """
        # date_str = time.strftime("%Y-%m-%d", time.localtime())
        url_place = f"http://kjcx.nuaa.edu.cn/book/more/lib/{place}/type/4/day/{date}"
        resp = requests.get(url_place, headers=self.headers, timeout=10)
        resp.encoding = 'utf-8'
        # print(resp.text)
        soup = BeautifulSoup(resp.text, 'lxml')
        # 提取预约链接
        tag_url_booking = soup.select('a.btn.btn-info')[0]
        url_booking = self.host + tag_url_booking['href']
        return url_booking

    def _get_flow_from_url(self, url):
        """
        Get the flow of a specific place url.
        :param url: {str} The url of a specific booking page.
        :return: people_info {list} [current, total]
        """
        # url = r"http://kjcx.nuaa.edu.cn/book/notice/act_id/650/type/4/lib/12"  # debug
        resp = requests.get(url, headers=self.headers, timeout=10)  #
        resp.encoding = 'utf-8'
        # print(resp.text)
        # soup = BeautifulSoup(resp.text, 'lxml')
        # tag_people_num = soup.select('.info')[1]
        # print(tag_people_num)
        re_people_num = re.compile(r'预约人数</b>：\[(\d+?)/(\d+?)\]')
        people_info = re_people_num.search(resp.text)
        people_info = [people_info.group(1), people_info.group(2)]
        print(people_info)
        return people_info

    def get_flow(self, date):
        """
        Convert the data to a JSON list.
        :param date: {str} 
        :return: data_all {dict} A dict of all libraries flow data.
        """
        data_all = {}
        for place in self.lib_id:
            place_id = self.lib_id[place]
            try:
                url = self._get_booking_url(place_id, date)
                info = self._get_flow_from_url(url)
                current = info[0]
                total = info[1]
            except Exception as e:
                print('\033[31m[ERROR]', e, '\033[0m')
                current = ''
                total = ''
            data_single = dict(current=current, total=total)
            data_all[place] = data_single
        return data_all


if __name__ == "__main__":
    flow = Flow()
    time_start = time.time()
    data = flow.get_flow(date='')
    print(data)
    print(time.time()-time_start)
