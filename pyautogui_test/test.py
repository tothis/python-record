import platform
import time

import pyautogui


def run():
    system = platform.system()

    if system == 'Windows':
        pyautogui.alert(text='支持Windows运行', title='提示', button='确定', timeout=800)
    else:
        pyautogui.alert(text='程序只支持Windows', title='提示', button='确定')
        return

    confirm = pyautogui.confirm(text='启动自动化控制?', title='提示', buttons=['确认', '取消'])

    if confirm == '确认':
        # 点击Win键盘
        pyautogui.press('winleft')
        # 模拟输入信息
        pyautogui.typewrite(message='huatu \n', interval=.2)
        print('执行画图动作')
        # 睡眠2秒
        time.sleep(2)
        # 鼠标剧中
        m, n = pyautogui.size()
        pyautogui.moveTo(x=m / 2, y=n / 2)
        pyautogui.click()  # 点击屏幕并聚焦
        distance = 200
        while distance > 0:
            pyautogui.drag(distance, 0, duration=0.5)  # 像右移动
            distance -= 5
            pyautogui.drag(0, distance, duration=0.5)  # 向下移动
            pyautogui.drag(-distance, 0, duration=0.5)  # 向左移动
            distance -= 5
            pyautogui.drag(0, -distance, duration=0.5)  # 向上移动


if __name__ == '__main__':
    run()
