# 随机生成手机号码
import random


# 生成随机手机号
def phone_number():
    second = [3, 4, 5, 7, 8][random.randint(0, 4)]
    # 第三个数字
    third = {
        3: random.randint(0, 9)
        , 4: [5, 7, 9][random.randint(0, 2)]
        , 5: [i for i in range(10) if i != 4][random.randint(0, 8)]
        , 7: [i for i in range(10) if i not in [4, 9]][random.randint(0, 7)]
        , 8: random.randint(0, 9)
    }[second]
    # 最后8位数字
    suffix = random.randint(9999999, 100000000)
    # 拼接手机号
    return "1{}{}{}".format(second, third, suffix)


if __name__ == '__main__':
    print(phone_number())
