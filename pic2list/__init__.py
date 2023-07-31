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
    image = cv2.imread(path)
    if image is None:
        return
    img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(img, 230, 255, cv2.THRESH_BINARY_INV)

    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    dot = []
    for c in contours:
        min_list = []
        x, y, w, h = cv2.boundingRect(c)
        min_list.append(x)
        min_list.append(y)
        min_list.append(w)
        min_list.append(h)
        min_list.append(w * h)
        dot.append(min_list)

    max_area = dot[0][4]
    for inlist in dot:
        area = inlist[4]
        if area >= max_area:
            x = inlist[0]
            y = inlist[1]
            w = inlist[2]
            h = inlist[3]
            max_area = area

    # cv2.rectangle(image, (x, y), (x + w, y + h), (255, 255, 0), 1)

    cv2.imwrite('out.jpg', image[y:y + h, x:x + w])
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

    rlist = []
    need = []
    for i in range(1, 10):
        rl = []
        for j in range(1, 10):
            timg = img[th * (i - 1):th * i, tw * (j - 1):tw * j]
            cv2.imwrite(f'temp/({i},{j}).jpg', timg)
            res = ocr.ocr(timg)
            r = '.'
            try:
                r = res[0][0][-1][0]
            except:
                pass
            if r == '.':
                need.append((i, j))
            rl.append(r)
        print(rl)
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
                c = res[i - 1][j - 1]
                cv2.putText(img, str(c), (int(tw * (j-0.7)), int(th * (i-0.1))),
                            cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), 2)
    cv2.imwrite('text.jpg', img)
    return img
