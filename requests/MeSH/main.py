#!/usr/bin/env python
# coding: utf8
import time

import requests
from lxml import etree

base_url = 'https://www.ncbi.nlm.nih.gov'


def 获取某页面主节点(mesh_url):
    time.sleep(2)
    page_html = etree.HTML(requests.get(base_url + mesh_url).content)
    名称 = page_html.xpath('//*[@class="title"]/text()')[0]
    return page_html.xpath('//b[text()="' + 名称 + '"]')[0]


# 递归获取某节点下的子节点
def 递归(节点, node_data):
    mesh_list = 节点.xpath('following-sibling::ul')
    node_child = []
    for mesh_item in mesh_list:
        node_child_data = {}
        a_text = mesh_item.xpath('a/text()')[0]
        a_url = mesh_item.xpath('a/@href')[0]
        node_child_data['text'] = a_text
        node_child_data['url'] = a_url
        print('node_child_data', a_text, a_url)
        # 子节点
        uls = mesh_item.xpath('ul')
        if uls:
            _node_child = []
            for ul in uls:
                _node_child_data = {}
                _a_url = ul.xpath('a/@href')[0]
                _a_text = ul.xpath('a/text()')[0]
                _node_child_data['text'] = _a_text
                _node_child_data['url'] = _a_url
                # 此子节点存在下级节点
                if ul.xpath('text()'):  # 为空:[] 不为空:[' +']
                    递归(获取某页面主节点(_a_url), _node_child_data)
                print('\t_node_child_data', _a_text, _a_url)
                _node_child.append(_node_child_data)
            node_child_data['child'] = _node_child
        node_child.append(node_child_data)
    node_data['child'] = node_child


def append_data(data, index='1'):
    target_url = data['url']
    data['index'] = index

    time.sleep(2)
    page_html = etree.HTML(requests.get(base_url + target_url).content)

    # Entry Terms 根据文本内容定位节点
    entry_terms = page_html.xpath('//p[text()="Entry Terms:"]/following-sibling::ul[1]//text()')
    data['entryTerms'] = entry_terms

    # Tree Number 和 MeSH Unique ID
    texts = page_html.xpath('//*[@class="rprt abstract"]/p/text()')
    if texts:
        for text in texts:
            replace_keys = ['Tree Number(s): ', 'MeSH Unique ID: ']
            for replace_key in replace_keys:
                if replace_key in text:
                    data[replace_key] = text.replace(replace_key, '')
        print('已处理', data['text'])
    if 'child' in data:
        for target_index, target_item in enumerate(data['child']):
            append_data(target_item, index + '-' + str(target_index + 1))


if __name__ == '__main__':
    mesh_url = '/mesh/68002318'
    result_data = {'text': 'Cardiovascular Diseases', 'url': mesh_url}
    递归(获取某页面主节点(mesh_url), result_data)
    print('result_data', result_data)

    # 此处保留URL备份
    # result_data = eval(open('url.txt').read())
    append_data(result_data)
    # 保存数据至文件
    file = open('data.txt', 'w', encoding='utf8')
    file.write(str(result_data))
    file.close()
