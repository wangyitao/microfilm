# -*- coding: utf-8 -*-
# @Author   : FELIX
# @Date     : 2018/7/23 10:27

import requests

access_token = '9a70c1a63cc34711917baf947306c615'


# 添加产品
def add_product(dic):
    post_url = 'https://merchant.wish.com/api/v2/product/add'
    dic['access_token']=access_token
    data = {
        'access_token': access_token,  # 秘钥
        'main_image': 'http://i.imgur.com/Q1a32kD.jpg',  # 主图
        'name': 'red shoe',  # 向愿望用户显示的产品名称
        'description': 'this is a cool shoed',  # 产品描述
        'tags': 'red,shoe,cool',  # 用逗号分隔的描述产品的字符串列表。只允许10个。任何过去10的标签都会被忽略。
        'sku': 'red-shoe-10',  # 不能重复 系统用来识别此产品的唯一标识符
        'inventory': '100',  # 库存 此产品的物理量最多为500,000
        'price': '100',  # 用户购买时的变化价格，最高100,000
        'shipping': '10',  # 标准配送
        'shipping_time': '',  # 5-10 运送时间
        'extra_images': 'http://i.imgur.com/Cxagv.jpg|http://i.imgur.com/Cxagv.jpg',  # 其他图片
        'parent_sku': 'red-shoe',  # 父类 可选在定义产品的变体时，我们必须知道要将变体附加到哪个产品。parent_sku是稍后您在使用添加产品变体API时可以使用的产品的唯一ID。
        'declared_name': '',  # 物流申报的产品名称
        'declared_local_name': '',  # 产品名称用当地语言写成，用于物流申报
        'pieces': '',  # 与此商品相关的件数
        'color': '',  # 可选产品的颜色。例如：红色，蓝色，绿色 Example: red, blue, green
        'size': '',  # 可选产品尺寸。示例：大，中，小，5,6,7.5
        'brand': '',  # 可选品牌或您的产品的制造商
        'landing_page_url': '',  # 包含产品详细信息的网站上的可选网址
        'upc': '',  # 可选的 12位通用产品代码（UPC） - 不包含字母或其他字符
        'max_quantity': '',  # 可选每件订单的最大产品数量。

    }
    print('开始上传产品')
    response = requests.post(url=post_url, data=dic)
    if response.status_code == 200:
        print('上传产品成功')
    print(response)
    print(response.text)
