import os
import cv2
import numpy as np


def draw_marker(basepath):
    # 定义一个叫cv_imread的函数来读取中文路径的图片，filePath是图片的完整路径
    def cv_imread(filePath):  # 读取中文路径的图片
        cv_img = cv2.imdecode(np.fromfile(filePath, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
        # imdecode读取的图像默认会按BGR通道来排列图像矩阵，如果后续需要RGB可以通过如下转换
        # cv_img=cv2.cvtColor(cv_img,cv2.COLOR_BGR2RGB)
        return cv_img

    # 定义一个叫cv_imwrite的函数来往中文路径写入img图片，filePathName是待写入的文件夹和图片名字组成的完整
    # 路径，如filePathName = C:\\user\\Desktop\\test.jpg
    def cv_imwrite(filePathName, img):
        try:
            _, cv_img = cv2.imencode(".jpg", img)[1].tofile(filePathName)
            return True
        except:
            return False

    download_path = basepath
    files = [os.path.join(download_path, v) for v in os.listdir(download_path) if str(v).startswith('备牌')]
    for filename in files:
        img = cv_imread(filename)
        h, w = img.shape[:2]
        cv2.putText(img, '0', (w // 2, h // 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 3)
        cv_imwrite(filename, img)
        # cv2.imshow('aaa', img)
        # cv2.waitKey()
        # cv2.destroyAllWindows()


if __name__ == '__main__':
    draw_marker('download')
