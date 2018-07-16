# -*- coding: utf-8 -*-
# @Author : Felix Wang
# @time   : 2018/7/9 21:50

# 定义蓝图

from flask import Blueprint

admin = Blueprint('admin',__name__)

import app.admin.views
