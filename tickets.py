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

from prettytable import PrettyTable

from stations import stations
from stations_all import stations_en2ch

class TrainsCollection:
    header = '车次 车次(始终) 路线(始终) 时间 历时 一等 二等 软卧 硬卧 硬座 无座'.split()

    def __init__(self, datas, options, maps):
        """查询到的火车班次集合
            :param datas: 数据列表
            :param options: 查询选项
            """
        self.datas = datas
        self.opts = options
        self.maps = maps

    @property
    def trains(self):
        for data in self.datas :
            info = data.split('|')
            opt = info[3][0].lower()
            if not self.opts or opt in self.opts :
                train = [
                    info[3],
                    '\n'.join([stations_en2ch[info[4]], stations_en2ch[info[5]]]),
                    '\n'.join([stations_en2ch[info[6]], stations_en2ch[info[7]]]),
                    '\n'.join([info[8],info[9]]),
                    info[10],
                    info[31],
                    info[30],
                    info[28],
                    info[26],
                    info[25],
                    info[24],
                ]
                yield train

    def pretty_print(self):
        pt = PrettyTable()
        pt._set_field_names(self.header)
        for train in self.trains :
            pt.add_row(train)
        print(pt)

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
    url_query = 'https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&leftTicketDTO.to_station={}&purpose_codes=ADULT'.format(
        date, from_station, to_station
    )
    # url_log = 'https://kyfw.12306.cn/otn/leftTicket/log?purpose_codes=ADULT&leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&leftTicketDTO.to_station={}'.format(
    #     date, from_station, to_station
    # )

    # 获取参数
    options = ''.join([
        key for key, value in arguments.items() if value is True
    ])

    # 添加verify=False参数不验证证书
    # r = requests.get(url_log, verify=False)
    # r = requests.get(url_log)
    r = requests.get(url_query, verify=False)
    r_json = r.json()
    # print(r)
    # print(r.url)
    # print(r.text)
    # print(r_json['data']['map'])

    TrainsCollection(r_json['data']['result'], options, r_json['data']['map']).pretty_print()

if __name__ == '__main__' :
    cli()
