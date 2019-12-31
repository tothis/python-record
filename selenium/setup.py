#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = '李磊'

from cx_Freeze import setup, Executable

setup(name='test',
      version='1.0',
      description='test',
      executables=[Executable("test.py")]
      )
# 执行python setup.py build 会在项目build\exe.win-amd64-3.7目录下生成exe文件
