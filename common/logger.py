#!/usr/bin/env python
# coding: utf-8
import logging
from logging import handlers


class Logger(object):
    # 日志关系映射
    level_relations = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'critical': logging.CRITICAL
    }

    def __init__(self, filename, level='info', back_count=10,
                 fmt='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'):
        self.logger = logging.getLogger(filename)
        format_str = logging.Formatter(fmt)  # 设置日志格式
        self.logger.setLevel(self.level_relations.get(level))  # 设置日志级别

        sh = logging.StreamHandler()  # 往屏幕上输出
        sh.setFormatter(format_str)  # 设置屏幕上显示的格式
        self.logger.addHandler(sh)  # 把对象加到logger里

        # 按照文件大小分割日志文件
        fh = handlers.RotatingFileHandler(filename=filename, maxBytes=10485760, backupCount=back_count)
        fh.setLevel(self.level_relations.get(level))
        fh.setFormatter(format_str)  # 设置文件里写入的格式
        self.logger.addHandler(fh)


if __name__ == '__main__':
    log = Logger('run.log', level='debug').logger
    log.debug('--- debug ---')
    log.info('--- info ---')
    log.warning('--- warning ---')
    log.error('--- error ---')
    log.critical('--- critical ---')
