# coding: utf-8
import re

import requests

from pprint import pprint

url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9015'

response = requests.get(url, verify=False)

# s = response.text.decode("gb2312").encode("utf-8")

# print s

stations = re.findall(u'([\u4e00-\u9fa5]+)\|([A-Z]+)', response.text)

# print("hello world")
#
# for s in stations :
#     print(s[0])

# pprint(stations, indent=4)

# pprint(dict(stations), indent=4)

f = open('stations.py','w+',encoding='utf-8')
f.write('# coding: utf-8\n{\n')
for s in stations :
    f.write("    '"+s[0]+"':'"+s[1]+"',\n")
f.write('}')
f.close()
