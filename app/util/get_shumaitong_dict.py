# -*- coding: utf-8 -*-
# @Author   : FELIX
# @Date     : 2018/6/22 11:39

import time
from pyquery import PyQuery as pq
from util.translate import translate
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from db.mysql_db import insert_one

from util.goto_excel import OperationExcel
from util.myid import my_id_maker

from settings import SEXCELFILENAME, SHOWMANEY, TRANNEEDWHAT


def get_data(page_source):
    # 创建操作Excel的对象
    op = OperationExcel(SEXCELFILENAME)
    START = 0
    try:
        data = {}
        doc = pq(str(page_source))
        items = doc('.util-clearfix.son-list .list-item')
        for item in items.items():
            title = str(item.find(' div.info > h3 > a').text()).replace('\n', ' ').strip()
            tran_title = translate(str(title).replace(r'\n', ' '), 'zh', 'en')
            detail_link = str(item.find(' div.info > h3 > a').attr('href')).split('?')[0]
            if 'http' not in detail_link:
                detail_link = ''.join(['http:', detail_link])
            price = item.find('div.info > span > span.value').text()
            orders = item.find('div > div.info > div > span.order-num > a > em').text()
            img_link = str(item.find('img').attr('image-src'))
            if img_link == 'None':
                img_link = str(item.find('img').attr('src'))
            if 'http' not in img_link:
                img_link = ''.join(['http:', img_link])

            data['type_name'] = TRANNEEDWHAT
            data['en_title'] = title
            data['zh_title'] = tran_title
            data['detail_url'] = detail_link
            data['view_price'] = price
            data['view_sales'] = orders
            data['img_url'] = img_link
            data['my_id'] = my_id_maker()
            data['get_date'] = time.strftime("%Y/%m/%d")

            # 插入Excel
            row_and_col = op.get_max_row_and_col()
            max_rows = row_and_col['max_rows']
            max_cols = row_and_col['max_cols']
            if max_rows == 1 and max_cols == 1:
                print('开始插入Excel标题')
                i = 1
                for key in data.keys():
                    op.write_data(SEXCELFILENAME, i, 1, key)
                    op.write_data(SEXCELFILENAME, i, 2, data[key])
                    i += 1
                print('插入Excel标题成功')
            if max_rows > 1 or max_cols > 1:
                print('开始插入Excel数据')
                j = 1
                for key in data.keys():
                    op.write_data(SEXCELFILENAME, j, max_rows + 1, data[key])
                    j += 1
                print('插入Excel数据成功')
                # 插入数据库
            try:
                insert_one('shumaitong', data)
                print('数据库插入成功')
            except Exception as e:
                print('数据库插入失败\n' + str(e))

            print(title)
            print(tran_title)
            print(detail_link)
            print(price)
            print(orders)
            print(img_link)
            START += 1
            print('##############################')

            with open('{}.txt'.format(TRANNEEDWHAT), 'a', encoding='utf8')as f:
                f.write(str(data) + '\n\n')
    except Exception as e:
        print(str(e))
    return START


def login():
    login_url = 'https://login.aliexpress.com/buyer.htm'
    browser.get(login_url)
    while True:
        inputs = input('登录完成输入y：')
        if inputs == 'y':
            break


def load_all():
    s = 'window.scrollTo({}, {})'
    i = '0'
    m = 40
    j = m
    while j > 0:
        # k = '(document.body.scrollHeight) / {}'.format(str(j))
        k = '(document.body.scrollHeight)/{}*{}'.format(str(m), str(j))
        browser.execute_script(s.format(i, k))
        i = k
        j -= 1
    i = 'document.body.scrollHeight'
    j = 1
    while j <= m:
        # k = '(document.body.scrollHeight) / {}'.format(str(j))
        k = '(document.body.scrollHeight)/{}*{}'.format(str(m), str(j))
        browser.execute_script(s.format(i, k))
        i = k
        j += 1
    time.sleep(1)
    locator2 = (By.CSS_SELECTOR, 'li')
    locator3 = (By.CSS_SELECTOR, 'img')
    locator4 = (By.CSS_SELECTOR, 'div')

    locator5 = (By.CSS_SELECTOR, 'a')

    WebDriverWait(browser, 30, 0.5).until(EC.presence_of_all_elements_located(locator2))
    WebDriverWait(browser, 30, 0.5).until(EC.presence_of_all_elements_located(locator3))
    WebDriverWait(browser, 30, 0.5).until(EC.presence_of_all_elements_located(locator5))


def start_get_shumaitong():
    start = 0
    page = 1
    login()
    while True:
        link = 'https://www.aliexpress.com/wholesale?g=y&SortType=total_tranpro_desc&SearchText={}&page={}'.format(
            TRANNEEDWHAT, str(page))
        try:
            if start < SHOWMANEY:
                browser.get(link)
                load_all()
                start += get_data(browser.page_source)
                page += 1
            else:
                break
        except Exception as e:
            print(str(e))


browser = webdriver.Chrome()

if __name__ == '__main__':

    start_get_shumaitong()
