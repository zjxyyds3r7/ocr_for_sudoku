import cv2
from paddleocr import PaddleOCR
import logging

logging.disable(logging.DEBUG)  # 关闭DEBUG日志的打印
logging.disable(logging.WARNING)  # 关闭WARNING日志的打印

ocr_ch = PaddleOCR(use_angle_cls=True, lang="ch", use_gpu=True)
ocr_en = PaddleOCR(use_angle_cls=True, lang="en", use_gpu=True)


def getroi(path):
    """
    标准板子 找出最大矩形
    :param path: 要读取图片的路径
    :return: 最大矩形的图像
    """
    image = cv2.imread(path)  # 读图片
    if image is None:
        # 没读到就返回
        return
    img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # 转灰度图

    ret, thresh = cv2.threshold(img, 230, 255, cv2.THRESH_BINARY_INV)
    # 二值化

    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # 找轮廓

    dot = []
    for c in contours:
        min_list = []
        x, y, w, h = cv2.boundingRect(c)
        # 找出能包裹这个轮廓的最小矩形

        min_list.append(x)
        min_list.append(y)
        min_list.append(w)
        min_list.append(h)
        min_list.append(w * h)
        # 计算面积
        dot.append(min_list)

    max_area = dot[0][4]
    for inlist in dot:
        area = inlist[4]
        if area >= max_area:
            # 找出最大面积
            x = inlist[0]
            y = inlist[1]
            w = inlist[2]
            h = inlist[3]
            # 取出对应的xywh
            max_area = area

    # cv2.rectangle(image, (x, y), (x + w, y + h), (255, 255, 0), 1)

    cv2.imwrite('out.jpg', image[y:y + h, x:x + w])
    # 用numpy的语法糖把这部分图像抠出来
    return image[y:y + h, x:x + w]


def roi2list(img, t):
    """
    图像转列表
    :param img: roi图像
    :param t: 识别类型,中文识别和英文识别
    :return: rlist:结果数组     need:空格坐标
    """
    if t == 'ch':
        ocr = ocr_ch
    else:
        ocr = ocr_en

    print(img.shape)
    h, w, _ = img.shape
    th, tw = h // 9, w // 9
    # 因为一个数独有9*9 所以长宽都分成9份 要用整除 因为后面用numpy截取

    rlist = []
    need = []
    for i in range(1, 10):
        rl = []
        for j in range(1, 10):
            timg = img[th * (i - 1):th * i, tw * (j - 1):tw * j]
            # 扣出要识别的部分

            cv2.imwrite(f'temp/({i},{j}).jpg', timg)
            res = ocr.ocr(timg)
            # 调用ocr识别
            r = '.'
            try:
                r = res[0][0][-1][0]
                # 飞桨的ocr的结果就让人膈应 建议自己print一下理一理
                # 如果没有结果就会爆出索引越界 所以直接try一下
                # 不建议这么用吧反正
            except:
                pass
            if r == '.':
                # 如果这个位置没识别出东西就把这个位置加入到need列表里
                need.append((i, j))
            rl.append(r)
            # 在当前行里加这个格子的结果
        print(rl)
        # 在大数组里加当前行的结果
        rlist.append(rl)
    return rlist, need


def list2pic(img, res, need):
    """
    列表画图
    :param img:图像
    :param res: 结果列表
    :param need: 空白部分
    :return: 画好的图
    """
    h, w, _ = img.shape
    th, tw = h // 9, w // 9
    # th * (i - 1):th * i, tw * (j - 1):tw * j
    for i in range(1, 10):
        for j in range(1, 10):
            if (i, j) in need:
                # 如果需要画
                # 但是这里应该写成for i,j in need:
                # 但是数据量小 没什么关系

                c = res[i - 1][j - 1]
                # ij都是1开始的 数组下标0开始的 所以-1

                cv2.putText(img, str(c), (int(tw * (j-0.7)), int(th * (i-0.1))),
                            cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), 2)
                # putText直接画 0.7和0.1是控制文字在格子中的位置的 可以自己调整下试试

    cv2.imwrite('text.jpg', img)
    return img
