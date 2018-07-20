# -*- coding: utf-8 -*-
# @Author   : FELIX
# @Date     : 2018/6/30 13:48


def my_id_maker():
    import uuid
    from hashlib import md5
    import datetime
    import random
    return md5(str('{0:%Y%m%d%H%M%S%f}'.format(datetime.datetime.now()) + ''.join(
        [str(random.randint(1, 10)) for i in range(5)])).encode('utf8') + str(uuid.uuid1()).encode('utf8')).hexdigest()

    # 简单版本的下面就行了
    # return '{0:%Y%m%d%H%M%S%f}'.format(datetime.datetime.now()) + ''.join(
    #     [str(random.randint(1, 10)) for i in range(5)])

if __name__ == '__main__':

    for i in range(10):
        print(len(my_id_maker()))
