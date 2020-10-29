#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = '李磊'

import requests
from lxml import html

url = 'https://www.kuaidaili.com/free/inha/{}/'

page_no = 1
max_count = 10

ip_pool = []

for i in range(0, max_count):
    response = requests.get(url.format(page_no)).text
    response_html = html.etree.HTML(response)
    tr_list = response_html.xpath('//tbody/tr')
    # print('结果', html.etree.tostring(tr_list[0], encoding='utf8').decode())

    for tr in tr_list:
        ip = tr.xpath("td[1]/text()")[0]
        # print('ip', ip)
        ip_pool.append(ip)
    page_no += 1

print('ip_pool', ip_pool)
