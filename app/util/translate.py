# -*- coding: utf-8 -*-
# @Author   : FELIX
# @Date     : 2018/6/30 15:28

import requests
import random
import json

def from_lang(content):
    if str(content).strip():
        return ''
    try:
        datas = {
            'query': content,
        }
        fromlang = json.loads(requests.post('http://fanyi.baidu.com/langdetect', data=datas).text)['lan']
        # print(fromlang)
        return fromlang
    except Exception as e:
        print(e)


def translate(content, tolang='zh', fromlang=None):
    if str(content).strip():
        return ''
    User_Agent = [
        'Mozilla/5.0 (Linux; Android 8.0; Pixel 2 Build/OPD3.170816.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Mobile Safari/537.36',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
    ]
    datas = {
        'query': content,
    }
    # 自动获取语言类型
    if not fromlang:
        fromlang = json.loads(requests.post('http://fanyi.baidu.com/langdetect', data=datas).text)['lan']
    # print(fromlang)
    data = {
        'from': fromlang,
        'to': tolang,
        'query': content,

    }
    url = 'http://fanyi.baidu.com/basetrans'

    headers = {
        'User-Agent': random.choice(User_Agent)
    }
    try:
        res = requests.post(url=url, data=data, headers=headers)
        # print(res.text)
        result = json.loads(res.text)

        return result['trans'][0]['dst']


    except Exception as e:
        print('翻译出错')
        print(e)
        translate(content, tolang, fromlang)


'''
zh    中文
en    英语
yue    粤语
wyw    文言文
jp    日语
kor    韩语
fra    法语
spa    西班牙语
th    泰语
ara    阿拉伯语
ru    俄语
pt    葡萄牙语
de    德语
it    意大利语
el    希腊语
nl    荷兰语
pl    波兰语
bul    保加利亚语
est    爱沙尼亚语
dan    丹麦语
fin    芬兰语
cs    捷克语
rom    罗马尼亚语
slo    斯洛文尼亚语
swe    瑞典语
hu    匈牙利语
cht    繁体中文
vie    越南语
'''
