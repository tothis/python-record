import ctypes
import sys

STD_INPUT_HANDLE = -10
STD_OUTPUT_HANDLE = -11
STD_ERROR_HANDLE = -12

# 定义字体颜色
FOREGROUND_BLUE = 0x09  # blue
FOREGROUND_GREEN = 0x0a  # green
FOREGROUND_RED = 0x0c  # red
FOREGROUND_YELLOW = 0x0e  # yellow

# 定义背景颜色
BACKGROUND_YELLOW = 0xe0  # yellow

std_out_handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)


def set_cmd_text_color(color, handle=std_out_handle):
    return ctypes.windll.kernel32.SetConsoleTextAttribute(handle, color)


def reset_color():
    set_cmd_text_color(FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_BLUE)


def print_green(mess):
    set_cmd_text_color(FOREGROUND_GREEN)
    sys.stdout.write(mess + '\n')
    reset_color()


def print_red(mess):
    set_cmd_text_color(FOREGROUND_RED)
    sys.stdout.write(mess + '\n')
    reset_color()


def print_yellow(mess):
    set_cmd_text_color(FOREGROUND_YELLOW)
    sys.stdout.write(mess + '\n')
    reset_color()


if __name__ == '__main__':
    print_green('print_green')
    print_red('print_red')
    print_yellow('print_yellow')
