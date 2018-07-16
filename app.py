# -*- coding: utf-8 -*-
# @Author : Felix Wang
# @time   : 2018/7/9 21:47

from flask import Flask

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    return 'ddd'


if __name__ == '__main__':
    app.run()
