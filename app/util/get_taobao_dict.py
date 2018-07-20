# -*- coding: utf-8 -*-
# @Author   : FELIX
# @Date     : 2018/6/30 15:58
import requests
import re
import json
from app.util.translate import translate
# from settings import HOWMANEY, NEEDWHAT, EXCELFILENAME
# from db.mysql_db import insert_one
from app.util.myid import my_id_maker
import time

from app.util.goto_excel import OperationExcel


def get_detail_dict(url, params):
    response = requests.get(url, params=params)
    response.encoding = response.apparent_encoding
    data = str(response.text).replace(r'\u003d', '=').replace(r'\u0026', '&').replace(r'\u003c', '<').replace(r'\u003e',
                                                                                                              '>')
    p = re.compile('<script>.*?(g_page_config.*?)</script>', re.S)
    a = p.findall(data)
    p2 = re.compile('g_page_config =(.*?)g_srp_loadCss', re.S)
    b = p2.findall(str(a[0]))

    products = u'%s' % str(b[0]).strip()[:-1]

    p3 = re.compile('("auctions":.*?)"recommendAuctions"', re.S)
    c = p3.findall(str(products))
    cc = str(c[0]).strip()[:-1]
    # print(cc)
    aa = '{' + cc + '}'
    products_dict = json.loads(aa)
    print(products_dict['auctions'])
    # with open('a.html','w',encoding='utf8') as f:
    #     f.write(data)
    return products_dict


def get_datas(name, url, params):
    # 创建操作Excel的对象
    # op = OperationExcel(EXCELFILENAME)
    START = 0
    for info in get_detail_dict(url, params=params)['auctions']:
        data = {}
        data["type_name"] = name
        if 'raw_title' in info.keys():
            title = info["raw_title"]
            data["zh_title"] = str(title).replace("'", '')
            print(title)
            translate_title = translate(title, 'en', 'zh')
            data["en_title"] = str(translate_title).replace("'", '')
            print(translate_title)
        if 'pic_url' in info.keys():
            pic_url = ''.join(['http:', info['pic_url']])
            data["img_url"] = str(pic_url).replace("'", '')
            print(pic_url)
        if 'view_price' in info.keys():
            view_price = info['view_price']
            data['view_price'] = str(view_price).replace("'", '')
            print(view_price)
        if 'view_sales' in info.keys():
            view_sales = info['view_sales']
            data["view_sales"] = str(view_sales).replace("'", '')
            print(view_sales)
        if 'detail_url' in info.keys():
            detail_url = ''.join(['http:', info['detail_url']])
            data["detail_url"] = str(detail_url).replace("'", '')
            print(detail_url)
        if 'item_loc' in info.keys():
            item_loc = info['item_loc']
            data["item_loc"] = str(item_loc).replace("'", '')
            print(item_loc)
            tran_loc = translate(item_loc, 'en', 'zh')
            data["tran_loc"] = str(tran_loc).replace("'", '')
            print(tran_loc)
        print('3#################################')
        START += 1
        data['my_id'] = my_id_maker()
        data['get_date'] = time.strftime("%Y/%m/%d")

        from app.models import Taobao
        from app import db
        taobao = Taobao(
            type_name=data["type_name"],
            zh_title=data["zh_title"],
            en_title=data["en_title"],
            img_url=data["img_url"],
            view_sales=data["view_sales"],
            detail_url=data["detail_url"],
        )
        db.session.add(taobao)  # 添加
        db.session.commit()  # 提交

        # # 插入数据库
        # try:
        #     insert_one('taobao', data)
        #     print('数据库插入成功')
        #
        #     row_and_col = op.get_max_row_and_col()
        #     max_rows = row_and_col['max_rows']
        #     max_cols = row_and_col['max_cols']
        #     if max_rows == 1 and max_cols == 1:
        #         print('开始插入Excel标题')
        #         i = 1
        #         for key in data.keys():
        #             op.write_data(EXCELFILENAME, i, 1, key)
        #             op.write_data(EXCELFILENAME, i, 2, data[key])
        #             i += 1
        #         print('插入Excel标题成功')
        #     if max_rows > 1 or max_cols > 1:
        #         print('开始插入Excel数据')
        #         j = 1
        #         for key in data.keys():
        #             op.write_data(EXCELFILENAME, j, max_rows + 1, data[key])
        #             j += 1
        #         print('插入Excel数据成功')
        # except Exception as e:
        #     print('数据库插入失败\n' + str(e))
        #
        # with open('{}.txt'.format(data['type_name']), 'a', encoding='utf8')as f:
        #     f.write(str(data) + '\n\n\n')
    return START


def start_get_taobao(NEEDWHAT,HOWMANEY):
    baseurl = 'https://s.taobao.com/search'

    params = {
        'q': NEEDWHAT,
        'search_type': 'item',
        'sort': 'sale-desc',
        's': '0',
    }
    num = 0
    s = 0
    while True:
        if num < HOWMANEY:
            print('开始抓取第{}条'.format(num))
            num += get_datas(NEEDWHAT, baseurl, params)
            s += 44
            params['s'] = str(s)
        else:
            break
