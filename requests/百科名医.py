#!/usr/bin/env python
# coding: utf-8
import time

import requests
import xlsxwriter
from lxml import html

data_file_path = 'data.txt'


def save_excel():
    excel = xlsxwriter.Workbook('data.xlsx')
    merge_format = excel.add_format({
        'bold': True,  # 字体加粗
        'border': 1,  # 单元格边框宽度
        'align': 'center',  # 水平居中
        'valign': 'vcenter',  # 垂直居中
        'fg_color': '#f4b084',  # 颜色填充
        'text_wrap': True  # 自动换行
    })
    sheet = excel.add_worksheet('Data')
    file = open(data_file_path, encoding='utf8')
    line = file.readline()
    i = 0
    while line:
        excel_row = eval(line)
        for j in range(len(excel_row)):
            # 连续两行的A单元格合并为一格 B单元格同理
            if i % 2:
                sheet.merge_range('A{}:A{}'.format(i, i + 1), excel_row[0], merge_format)
                sheet.merge_range('B{}:B{}'.format(i, i + 1), excel_row[1], merge_format)
            sheet.write(i, j, excel_row[j])
        i += 1
        line = file.readline()
    file.close()
    excel.close()


def parse_item(titles, item_type):
    result = []
    for title_index, title in enumerate(titles):
        # 标题
        title_text = title.xpath('string(.)')
        # 内容
        content_text = title.xpath('string(following-sibling::*)')
        result.extend([title_text, content_text])
        print('{} [{}]{} {} [{}]{}'.format(
            tab_name,
            index,
            item_name,
            '通俗版目录' if item_type else '专业版目录',
            title_index,
            title_text
        ))
    return result


if __name__ == '__main__':
    base_url = 'https://www.baikemy.com'

    # 标签
    page_tab = requests.get(base_url + '/disease/list/0/0').text
    tab_html = html.etree.HTML(page_tab)
    tabs = tab_html.xpath('//*[@class="nav_link"]/a')

    for tab_item in tabs:
        tab_name = tab_item.xpath('string(.)')
        tab_url = tab_item.xpath('@href')[0]
        page_text = requests.get(base_url + tab_url).text
        page_html = html.etree.HTML(page_text)
        # 类型
        type_infos = page_html.xpath('//*[@class="typeInfo_Li"]/a')
        for index, item in enumerate(type_infos):
            p_result_item = []
            s_result_item = []
            item_name = item.xpath('string(.)')
            if item_name != '更多':
                item_url = base_url + item.xpath('@href')[0]

                item_text = requests.get(item_url).text
                item_html = html.etree.HTML(item_text)

                p_result_item.extend([tab_name, item_name, item_url])
                s_result_item.extend([tab_name, item_name, item_url])

                # 通俗版目录标题列表
                p_titles = item_html.xpath('//*[@class="p_directory_flag"]')
                p_result_item.extend(parse_item(p_titles, 1))
                # 专业版目录标题列表
                s_titles = item_html.xpath('//*[@class="s_directory_flag"]')
                s_result_item.extend(parse_item(s_titles, 0))

                # 追加写入
                data_text = open(data_file_path, 'a', encoding='utf8')
                data_text.write(str(p_result_item) + '\n')
                data_text.write(str(s_result_item) + '\n')
                data_text.close()

                time.sleep(1)
    # 保存数据至Excel
    save_excel()
