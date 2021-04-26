#!/usr/bin/env python
# coding: utf-8
import json
import time

import pymysql
import requests
from lxml import html

if __name__ == '__main__':

    tr_type = ['食部(Edible)', '水分(Water)', '能量(Energy)', '蛋白质(Protein)', '脂肪(Fat)', '胆固醇(Cholesterol)', '灰分(Ash)',
               '碳水化合物(CHO)',
               '总膳食纤维(Dietary fiber)'
        , '胡萝卜素(Carotene)', '维生素A(Vitamin)', 'α-TE', '硫胺素(Thiamin)', '核黄素(Riboflavin)', '烟酸(Niacin)', '维生素C(Vitamin C)'
        , '钙(Ca)', '磷(P)', '钾(K)', '钠(Na)', '镁(Mg)', '铁(Fe)', '锌(Zn)', '硒(Se)', '铜(Cu)', '锰(Mn)', '碘(I)'
        , '饱和脂肪酸(SFA)', '单不饱和脂肪酸(MUFA)', '多不饱和脂肪酸(PUFA)', '合计(Total)']
    detail_type = ['含量', '同类排名', '同类均值']

    # 拼接数据库字段
    tr_type_field = ''
    for type_item in tr_type:
        for detail_type_item in detail_type:
            tr_type_field_text = type_item + '_' + detail_type_item
            tr_type_field += '`{}` TEXT COMMENT "{}",'.format(tr_type_field_text, tr_type_field_text)

    # 打开数据库连接
    db = pymysql.connect('192.168.1.128', 'root', '123456', 'test')
    # 创建一个游标对象
    cursor = db.cursor()
    table = '''
    CREATE TABLE `食物营养成分查询平台` (
    	`id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    	`大分类名称` VARCHAR ( 255 ) COMMENT '大分类名称',
    	`分类名称` VARCHAR ( 255 ) COMMENT '分类名称',
    	`食物名称` VARCHAR ( 255 ) COMMENT '食物名称',
    	{}
    PRIMARY KEY ( `id` )
    )
    '''.format(tr_type_field)
    print('table', table)
    # cursor.execute(table)

    base_url = 'https://fq.chinafcd.org'
    data_url = 'https://fq.chinafcd.org/FoodInfoQueryAction!queryFoodInfoList.do?' \
               'categoryOne={}&categoryTwo={}' \
               '&foodName=0&pageNum={}&field=0&flag=0'

    # 大分类
    大分类s = html.etree.HTML(requests.get(base_url).text).xpath('//*[contains(@class, "food_box")]')

    for 大分类 in 大分类s:
        大分类名称 = 大分类.xpath('string(div/h3/a)')
        分类s = 大分类.xpath('ul/li/a')
        for 分类 in 分类s:
            分类名称 = 分类.xpath('string()')
            data_pid = 分类.xpath('@data_pid')[0]
            data_id = 分类.xpath('@data_id')[0]
            # 睡眠1秒
            time.sleep(1)
            json_data = json.loads(requests.get(data_url.format(data_pid, data_id, 1)).text)
            data = json_data['list']
            data_num = int(json_data['totalPages'])
            print('data num', data_num)
            # 页数大于1则分页获取数据
            if data_num > 1:
                for num in range(data_num - 1):
                    # 睡眠1秒
                    time.sleep(1)
                    data.extend(json.loads(requests.get(data_url.format(data_pid, data_id, num + 2)).text)['list'])
            for item in data:
                # 睡眠1秒
                time.sleep(1)
                trs = html.etree.HTML(requests.get(base_url + '/foodinfo/{}.html'.format(item[0])).text).xpath('//tr')
                # 删除表格标题
                trs.pop(0)
                字段名称 = ''
                字段占位符 = ''
                字段值 = [大分类名称, 分类名称, item[2]]
                for tr_index, tr in enumerate(trs):
                    tds = tr.xpath('td')
                    字段名称 += '`{}_含量`,`{}_同类排名`,`{}_同类均值`,'.format(tr_type[tr_index], tr_type[tr_index],
                                                                  tr_type[tr_index])
                    字段占位符 += '%s,%s,%s,'
                    # 含量
                    字段值.append(tds[2].xpath('string()'))

                    # 同类排名
                    字段值.append(tds[3].xpath('string()'))

                    # 同类均值
                    字段值.append(tds[4].xpath('string()'))
                print('\t字段值', 字段值)
                sql = 'insert into 食物营养成分查询平台 (大分类名称,分类名称,食物名称,{}) value (%s,%s,%s,{})'.format(字段名称[:-1], 字段占位符[:-1])
                # print('sql', sql)
                cursor.execute(sql, tuple(字段值))
                # 提交
                db.commit()
    # 关闭游标
    cursor.close()
    # 关闭数据库连接
    db.close()
