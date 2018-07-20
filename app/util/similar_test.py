# -*- coding: utf-8 -*-
# @Author   : FELIX
# @Date     : 2018/6/26 10:05

import json
from aip import AipNlp
import re


def translate(content, tolang='zh', fromlang=None):
    import requests
    import random
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

""" 你的 APPID AK SK """
APP_ID = '11258138'
API_KEY = '0GrG6PASzOFbat1azagP5kxc'
SECRET_KEY = 'tpulU5wn8StE0VKE7xBVv553D0PTD6Gk '

client = AipNlp(APP_ID, API_KEY, SECRET_KEY)


def similar(text1, text2):
    return client.simnet(text1, text2)['score']


def read_data2():
    datas2 = []
    with open('墙纸2.txt', 'r', encoding='utf8')as f:
        data2 = f.read().split('\n\n\n')
        for data in data2:
            p = re.compile("'raw_title':(.*?), 'translate_title'")
            p2 = re.compile("'translate_title':(.*?), 'pic_url'")
            try:
                a = str(p.findall(data)[0]).strip("' ").strip('" ')
                b = str(p2.findall(data)[0]).strip("' ").strip('" ')
                datas2.append({"en_title": b, "zh_title": a, "data": data})
            except:
                pass
        return datas2


def read_data1():
    datas1 = []
    with open('墙纸1.txt', 'r', encoding='utf8')as f:
        data1 = f.read().split('\n\n')
        for data in data1:
            # print("########")
            j = str(data.replace(r'\n', ' '))
            p = re.compile("'title':(.*?), 'tran_title'")
            p2 = re.compile("'tran_title':(.*?), 'detail_link'")

            try:
                title = str(p.findall(j)[0]).strip("' ").strip('" ')
                tran_title = str(p2.findall(j)[0]).strip("' ").strip('" ')
                if title:
                    # print(title)
                    # print(tran_title)
                    datas1.append({"en_title": title, "zh_title": tran_title, "data": data})
            except:
                pass
        return datas1

        #     if j:
        #         datas1.append(j)
        # d=0
        # for i in datas1:
        #
        #     print(a)
        #     d+=1


data = read_data1()
data2 = read_data2()
# print(data2)
# print(len(data2))
# print(data)
# print(len(data))

for i in range(len(data)):
    en_max_sim = 0.0
    zh_max_sim = 0.0

    for j in range(len(data2)):
        try:
            print(i, j)
            en_sim = similar(data[i]['en_title'], data2[j]['en_title'])
            zh_sim = similar(data[i]['zh_title'], data2[j]['zh_title'])
            print('en_sim:' + str(en_sim), 'zh_sim:' + str(zh_sim))
            with open('{}_sim.txt'.format(str(i)), 'a', encoding='utf8')as f:
                f.write(
                    str(data[i]) + '\n' + str(data2[j]) + '\n' + 'en_sim:' + str(en_sim) + '    ' + 'zh_sim' + str(
                        zh_sim) + '\n\n')
            if en_max_sim <= en_sim:
                if en_max_sim == en_sim:
                    with open('{}_max_en.txt'.format(str(i)), 'a', encoding='utf8')as ff:
                        ff.write(str(data[i]) + '\n' + str(
                            data2[j]) + '\n' + 'en_max_sim:' + str(en_max_sim) + '    ' + 'zh_sim' + str(
                            zh_sim) + '\n\n')
                else:
                    en_max_sim = en_sim
                    with open('{}_max_en.txt'.format(str(i)), 'w', encoding='utf8')as ff:
                        ff.write(str(data[i]) + '\n' + str(
                            data2[j]) + '\n' + 'en_max_sim:' + str(en_max_sim) + '    ' + 'zh_sim' + str(
                            zh_sim) + '\n\n')

            if zh_max_sim <= zh_sim:
                if zh_max_sim == zh_sim:
                    with open('{}_max_zh.txt'.format(str(i)), 'a', encoding='utf8')as ff:
                        ff.write(str(data[i]) + '\n' + str(
                            data2[j]) + '\n' + 'en_sim:' + str(en_sim) + '    ' + 'zh_max_sim' + str(
                            zh_max_sim) + '\n\n')
                else:
                    zh_max_sim = zh_sim
                    with open('{}_max_zh.txt'.format(str(i)), 'w', encoding='utf8')as ff:
                        ff.write(str(data[i]) + '\n' + str(
                            data2[j]) + '\n' + 'en_sim:' + str(en_sim) + '    ' + 'zh_max_sim' + str(
                            zh_max_sim) + '\n\n')
        except Exception as e:
            print(str(e))
            with open('log.txt', 'a', encoding='utf8')as f:
                f.write(str(e) + '\n\n')
# text1 = 'mondecor PE Foam 3D Wall Stickers Brick Pattern Waterproof\nWallpaper\nLiving Room'
# text2 = 'European TV background wallpaper luxurious simple European pattern modern simple living room wallpaper wall decoration fresco'
#
#
# print(similar(text1,text2))
