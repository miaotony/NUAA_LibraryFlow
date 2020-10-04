#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
save_data.py

NUAA Library Flow
Save data to local storage.
图书馆人流量保存数据到本地

@Author: MiaoTony
@CreateTime: 20201004
@UpdateTime: 20201005
"""

from crawler import Flow
import time
import random
import datetime
import json
import os


def save(data, date_str):
    """
    Save data to local storage.
    :param data: {list} All area flow data.
    :param date_str: {str} date.
    """
    time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(time_now)
    data_dict = dict(time=time_now, data=data)

    # The latest data
    if not os.path.exists("./data/"):
        os.mkdir("./data/")
    if not os.path.exists("./data/latest/"):
        os.mkdir("./data/latest/")
    filename_latest = "./data/latest/" + date_str + ".json"
    with open(filename_latest, 'w', encoding="utf-8") as fout_latest:
        json.dump(data_dict, fout_latest, ensure_ascii=False,
                  indent=2, separators=(',', ': '))

    # All data
    if not os.path.exists("./data/all/"):
        os.mkdir("./data/all/")
    filename_all = "./data/all/" + date_str + ".json"
    if not os.path.exists(filename_all):
        data_all = [data_dict]
        with open(filename_all, 'w', encoding="utf-8") as fout_all:
            json.dump(data_all, fout_all, ensure_ascii=False,
                      indent=2, separators=(',', ': '))
    else:
        with open(filename_all, 'r', encoding="utf-8") as fin_all:
            data_all = json.load(fin_all)
        # print(data_all)
        data_all.append(data_dict)

        with open(filename_all, 'w', encoding="utf-8") as fout_all:
            json.dump(data_all, fout_all, ensure_ascii=False,
                      indent=2, separators=(',', ': '))
        print("\033[33mSave data OK!\033[0m")


if __name__ == "__main__":
    flow = Flow()
    time_start = time.time()
    time_now = datetime.datetime.now()
    print("\033[33mtime_now: ", time_now, "\033[0m")
    hour = int(time_now.strftime("%H"))
    # 超过22点则爬取下一天数据
    if hour < 22:
        date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    else:
        today = datetime.datetime.now()
        tomorrow = today+datetime.timedelta(days=1)
        date_str = tomorrow.strftime("%Y-%m-%d")
    print("\033[33mdate_str: ", date_str, "\033[0m")
    # data = flow.get_flow(date=date_str)
    data = flow.get_flow_parallel(date=date_str)
    print(data)
    print(time.time()-time_start)
    print("\033[33mSave data...\033[0m")
    save(data, date_str)
