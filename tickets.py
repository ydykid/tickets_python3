# coding: utf-8

"""命令行火车票查看器


Usage:
    tickets [-gdtkz] <from> <to> <date>


Options:
    -h,--help   显示帮助菜单
    -g          高铁
    -d          动车
    -t          特快
    -k          快速
    -z          直达


Example:
    tickets  北京  上海  2016-10-10
    tickets  -dg  成都  南京  2016-10-10

"""

import re

import requests

from docopt import docopt

from stations import stations
# import stations


def cli():
    """command-line interface"""
    arguments = docopt(__doc__)
    # print(arguments)
    from_station = stations.get(arguments['<from>'])

    to_station = stations.get(arguments['<to>'])

    date = arguments['<date>']

    print('from_station'+from_station)
    print('to_station'+to_station)
    print('date'+date)

    # 构建url
    url = 'https://kyfw.12306.cn/otn/lcxxcx/query?purpost_codes=ADULT&queryDate={}&from_station={}&to_station={}'.format(
        date, from_station, to_station
    )

    # 添加verify=False参数不验证证书
    r = requests.get(url, verify=False)

    print(r)

    print(r.json())


if __name__ == '__main__' :
    cli()
