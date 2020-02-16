import cv2

capture = cv2.VideoCapture(0)  # 创建一个 VideoCapture 对象

flag = 1  # 设置一个标志 用来输出视频信息
num = 1  # 递增 用来保存文件名
while capture.isOpened():  # 循环读取每一帧
    # 返回两个参数 第一个是bool是否正常打开 第二个是照片数组 如使用单个变量接收则返回一个tumple包含bool和图片
    open_flag, show = capture.read()
    if open_flag:
        cv2.imshow('capture', show)
        # 每帧数据延时 1ms 延时不能为 0 否则读取的结果会是静态帧
        k = cv2.waitKey(1) & 0xFF
        if k == ord('s'):  # 若检测到按键s 进行拍照并打印字符串
            image = str(num) + '.jpg'
            cv2.imwrite('face/' + image, show)
            print(capture.get(3))  # 得到长宽
            print(capture.get(4))
            print('保存成功 ' + image)
            num += 1
        elif k == ord('q'):  # 若检测到按键q退出
            break
capture.release()  # 释放摄像头
cv2.destroyAllWindows()  # 删除建立的全部窗口
