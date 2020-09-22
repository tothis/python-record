#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = '李磊'

import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

# 淘宝镜像http://npm.taobao.org/mirrors/chromedriver/ 选择与chrome相同或老一点的版本
# chrome地址栏输入chrome://version/可查看版本

# 把chromedriver.exe放在与python脚本同目录会自动查找
driver = webdriver.Chrome('/Users/lilei/project/webdriver/chromedriver')

# 将浏览器最大化显示
driver.maximize_window()

# 将浏览器最小化显示
# driver.minimize_window()

# 浏览器设置窗口大小
# 设置浏览器宽480 高800显示
# driver.set_window_size(480, 800)

url = 'http://www.baidu.com/'
driver.get(url)

# 浏览器后退
# driver.back()

# 浏览器前进
# driver.forword()

# id定位 find_element_by_id()
# name定位 find_element_by_name()
# class定位 find_element_by_class_name()
# link定位 find_element_by_link_text()
# partial link定位 find_element_by_partial_link_text()
# tag定位 find_element_by_tag_name()
# xpath定位 find_element_by_xpath()
# css定位 find_element_by_css_selector()
# 输入内容
driver.find_element_by_id('kw').send_keys('磊真的帅吗？')
# 定位提交按钮 模拟点击事件
driver.find_element_by_css_selector('''input[value=百度一下]''').click()

time.sleep(3)  # 强制等待3秒再执行下一步

# 隐形等待 设置最长等待时间 在规定时间内网页加载完成(包含页面引入的js和css) 则继续执行
driver.implicitly_wait(30)

# 显式等待 固定时间判断条件 成立继续执行 否则等待 超过设置最长时间时抛出TimeoutException
# webdriver.support.wait.WebDriverWait(driver, 超时时长, 调用频率, 忽略异常).until(可执行方法, 超时时返回的信息)

# from selenium.webdriver.common.keys import Keys通过 send_keys()调用按键
# send_keys(Keys.TAB) # tab
# send_keys(Keys.ENTER) # 回车

# if driver.get_screenshot_as_file('D:/data/test.png'):
#     print('截图成功')

driver.close()
