#!/usr/bin/env python
# coding: utf-8
import platform
import sys
from ctypes import CDLL

from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QMainWindow, QTextBrowser, QApplication, QMessageBox

# 动态链接库生成参考 https://github.com/tothis/cpp-record/tree/main/lib
if platform.system() == 'Windows':
    dll = CDLL('lib/test')
elif platform.system() == 'Linux':
    dll = CDLL('lib/test.so')
print('dll', dll.test_add(1, 2))


class Main(QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        # 窗口标题
        self.setWindowTitle('文件拖入')
        self.setWindowIcon(QIcon('favicon.ico'))
        # 窗口大小
        self.resize(500, 400)
        # 开启拖曳操作文本
        self.setAcceptDrops(True)

        # 设置字体
        font = QFont()
        font.setFamily("黑体")
        font.setPointSize(14)

        text_browser = QTextBrowser()
        text_browser.setFont(font)
        # 不换行
        text_browser.setLineWrapMode(0)
        self.text_browser = text_browser
        self.setCentralWidget(text_browser)

    def closeEvent(self, event):
        reply = QMessageBox.question(self, '提示', '确定关闭?', QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    # 拖曳开始触发
    def dragEnterEvent(self, event):
        print('--- --- 文本域拖曳开始 --- ---')
        # 检测拖曳进来的数据是否包含文本 如有则放行
        if event.mimeData().hasText():
            event.accept()
        else:
            event.ignore()

    # 拖曳结束触发
    def dropEvent(self, event):
        print('--- --- 文本域拖曳结束 --- ---')
        if event.mimeData().hasText():
            event.accept()
            file_path = event.mimeData().urls()[0].toLocalFile()
            file = open(file_path, encoding='utf8')
            file_context = file.read()
            self.text_browser.setText('path ' + file_path + '\n' + file_context)
        else:
            event.ignore()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec_())
