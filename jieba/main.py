#!/usr/bin/env python
# coding: utf-8
# 原文 https://www.bilibili.com/video/av46929001
import jieba.posseg as psg

import numpy as np
from PIL import Image
from wordcloud import WordCloud, STOPWORDS


# 根据词频降序排序
def word_sort(lst):
    word_frequency = {}
    for word in lst:
        if word in word_frequency:
            word_frequency[word] += 1
        else:
            word_frequency[word] = 1

    word_sort = sorted(word_frequency.items(), key=lambda x: x[1], reverse=True)
    return word_sort


# 生成词云
def create_word_cloud(lst):
    words_space_split = " ".join(lst)

    # 设置停用词
    sw = set(STOPWORDS)
    sw.add("的")
    sw.add("嗯")
    sw.add("吗")

    # 图片模板和字体
    image = np.array(Image.open('layout.jpg'))
    font = r'./font.ttf'

    # 生成词云
    my_wordcloud = WordCloud(scale=4, font_path=font, mask=image, stopwords=sw, background_color='white',
                             max_words=100, max_font_size=60, random_state=20).generate(words_space_split)

    # 保存生成的图片
    my_wordcloud.to_file('词云.jpg')


if __name__ == "__main__":

    # 打开存放项目名称的txt文件
    with open('text.txt', encoding='utf8') as f:
        content = (f.read())
        f.close()

    # 分离出感兴趣的名词 放在 lst_words 里
    lst_words = []
    for x in psg.cut(content):
        # 保留名词 人名 地名 长度至少两个字
        if x.flag in ['n', 'nr', 'ns'] and len(x.word) > 1:
            lst_words.append(x.word)

    # 按照词频由大到小排序 放在 lst_sorted 里
    lst_sorted = word_sort(lst_words)

    # 打印TOP10
    print('\n序号\t名词\t词频\t柱图\n')
    for i in range(10):
        print('{}\t{}\t{}\t{}\n'.format(i + 1, lst_sorted[i][0], lst_sorted[i][1], '▂' * (lst_sorted[i][1] // 100)))

    create_word_cloud([x[0] for x in lst_sorted])
