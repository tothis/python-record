#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = '李磊'

import re
import time

import pymysql
import requests
from lxml import html


def is_number(num):
    match = re.compile(r'^[-+]?[-0-9]\d*\.\d*|[-+]?\.?[0-9]\d*$').match(num)
    return True if match else False


# 下载文件
def download_file(file_path, file_name):
    r = requests.get(file_path)
    # 保存图片至当前image目录下 也可使用绝对路径D:/image/ 此目录不会自动创建需手动创建
    path = file_name
    with open(path, 'wb') as f:
        f.write(r.content)


# 打开数据库连接
db = pymysql.connect('localhost', 'root', '123456', 'test')
# 创建一个游标对象
cursor = db.cursor()
cursor.execute('''
CREATE TABLE `菜品` (
`id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
`菜品名称` VARCHAR ( 100 ) DEFAULT '' COMMENT '菜品名称',
`菜品类型` VARCHAR ( 100 ) DEFAULT '' COMMENT '菜品类型',
`卡路里` INT UNSIGNED DEFAULT NULL COMMENT '卡路里',
`蛋白质` FLOAT UNSIGNED DEFAULT NULL COMMENT '蛋白质',
`碳水化合物含量` FLOAT UNSIGNED DEFAULT NULL COMMENT '碳水化合物含量',
`脂肪` FLOAT UNSIGNED DEFAULT NULL COMMENT '脂肪',
`适应症` VARCHAR ( 255 ) DEFAULT '' COMMENT '适应症',
`图片` VARCHAR ( 255 ) DEFAULT '' COMMENT '图片',
PRIMARY KEY ( `id` )
)
''')

url = 'https://food.hiyd.com/list-1-html?page='

max_count = 712

for i in range(1, max_count + 1):
    new_url = url + str(i)
    print('url' + new_url)
    response = requests.get(new_url).text
    # 解析html文本 获取_Element对象
    html_result = html.etree.HTML(response)
    # 菜谱列表
    li_list = html_result.xpath("//*[@class='list-main']/div/div[2]/ul/li")

    # decode 修改换行符
    # print('结果', html.tostring(html_result, encoding='utf8').decode())
    # print('结果', html.etree.tostring(li_list[0], encoding='utf8').decode())

    for li in li_list:
        click = li.xpath('./a/@href')[0]
        # print('结果', click)
        # 模仿点击
        new_page_response = requests.get('https:' + click).text
        # print('结果', new_page_response)
        new_html_result = html.etree.HTML(new_page_response)

        # 页面404
        try:
            new_page_info = new_html_result.xpath("//*[@class='info-base']/div")[0]
            # print('结果', html.etree.tostring(new_page_info, encoding='utf8').decode())
        except IndexError:
            continue

        # 字段缺失则设置为空
        try:
            菜品类型 = new_html_result.xpath("//*[@class='mod-crumbs']/a[3]/text()")[0]
        except IndexError:
            菜品类型 = ''
        try:
            图片 = new_page_info.xpath('./div/img/@src')[0]
        except IndexError:
            图片 = ''
        # print('图片地址', 图片)
        # 保存文件
        # download_file(图片, 'image/' + str(0) + '.png')
        # 保存菜品信息
        try:
            菜品名称 = new_page_info.xpath('./h1/em/text()')[0]
        except IndexError:
            菜品名称 = ''
        try:
            卡路里 = new_page_info.xpath('./ul/li/p/em/text()')[0]
        except IndexError:
            卡路里 = 'null'
        try:
            蛋白质 = new_page_info.xpath('./ul/li[2]/p/em/text()')[0]
        except IndexError:
            蛋白质 = 'null'
        try:
            碳水化合物含量 = new_page_info.xpath('./ul/li[3]/p/em/text()')[0]
        except IndexError:
            碳水化合物含量 = 'null'
        try:
            脂肪 = new_page_info.xpath('./ul/li[4]/p/em/text()')[0]
        except IndexError:
            脂肪 = 'null'
        try:
            适应症 = new_page_info.xpath('./p/text()')[0][:-1]
        except IndexError:
            适应症 = ''
        print(菜品名称, 菜品类型, 卡路里, 蛋白质, 碳水化合物含量, 脂肪, 适应症, 图片)
        # 执行SQL
        # 使用预处理语句创建表
        sql = '''
        INSERT INTO 菜品 (
            菜品名称,
            菜品类型,
            卡路里,
            蛋白质,
            碳水化合物含量,
            脂肪,
            适应症,
            图片
        )
        VALUE ( %s, %s, %s, %s, %s, %s, %s, %s )
        '''
        print('sql', sql)
        cursor.execute(sql, (
            菜品名称,
            菜品类型,
            卡路里 if is_number(卡路里) else None,
            蛋白质 if is_number(蛋白质) else None,
            碳水化合物含量 if is_number(碳水化合物含量) else None,
            脂肪 if is_number(脂肪) else None,
            适应症,
            图片))
        db.commit()
        # 睡眠20秒 防止限制IP
        time.sleep(20)

# 关闭游标
cursor.close()
# 关闭数据库连接
db.close()
