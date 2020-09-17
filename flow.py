#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
flow.py

NUAA Library Flow backend
图书馆人流信息后端

@Author: MiaoTony
@CreateTime: 20200918
"""

from flask import Flask, request, jsonify, make_response, Response
from flask import session as s
from flask_cors import CORS
import urllib.parse
from crawler import Flow

app = Flask(__name__)
app.config['SECRET_KEY'] = "Meow~~~"
CORS(app, supports_credentials=True)  # allow CORS


@app.after_request
def after_request(response):
    """
    after a request.
    """
    print("\033[33m#######################################\033[0m")
    return response


@app.route('/api/libraryFlow', methods=['GET', 'POST'])
def api_LibraryFlow():
    """
    LibraryFlow
    :param date: {str}
    """
    # 从request对象读取表单内容
    print('\033[33m[DEBUG] API LibraryFlow test!\033[0m')
    url = request.url
    # print(url)
    print(urllib.parse.unquote(url))
    # raw_data = request.get_data().decode('utf-8')
    # print(raw_data)
    date = request.args.get('date', '')
    print(date)
    try:
        # Create a `Flow` object
        flow = Flow()
        data = flow.get_flow(date=date)
        print(data)
        return jsonify(state=True, msg="OK!", data=data)
    except Exception as e:
        print('\033[31m[ERROR]', e, '\033[0m')
        return jsonify(state=False, msg=str(e))


if __name__ == '__main__':
    try:
        app.run(debug=False, host='0.0.0.0')  # , port=8888
    except Exception as e:
        print('\033[31m[ERROR]', e, '\033[0m')
