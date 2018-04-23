#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
# @Time    : 18-4-8 上午11:44
# @Author  : 无敌小龙虾
# @File    : Wechat.py
# @Software: PyCharm

import requests

APP_ID = ''
APP_SECRET = ''


def get_session_key(code):
    url = 'https://api.weixin.qq.com/sns/' \
          'jscode2session?appid=%s&secret=%s&js_code=%s&' \
          'grant_type=authorization_code' % (APP_ID, APP_SECRET, code)
    res = requests.get(url)
    json_data = res.json()
    # print(json_data)
    openid = json_data.get('openid', None)
    session = json_data.get('session_key', None)
    if openid and session:
        return True, openid, session
    return False, None, None
