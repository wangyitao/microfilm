# -*- coding: utf-8 -*-
# @Author : Felix Wang
# @time   : 2018/7/9 21:46

# 入口脚本文件

from app import app

if __name__ == '__main__':
    app.run() # 本地访问
    # app.run(host='0.0.0.0', port=5000)  # 局域网访问，
