#!/usr/bin/env python
# coding: utf-8
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

driver = webdriver.Chrome('/app/chromedriver')
driver.get('https://www.baidu.com')

# 通过id定位搜索框 输入内容
driver.find_element_by_id('kw').send_keys('高血压')
# 定位提交按钮 模拟点击事件
driver.find_element_by_css_selector('input[value=百度一下]').click()

# driver 驱动
# timeout 最长超时时间 单位:秒
# poll_frequency 检测的间隔步长 默认0.5秒
# ignored_exceptions 超时后抛出的异常 默认抛出NoSuchElementException异常
wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.ID, 'content_left')), message='加载超时')

try:
    selector = driver.find_element_by_css_selector('.c-container.result').click()
except NoSuchElementException:
    pass
driver.close()
