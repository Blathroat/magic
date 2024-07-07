import cv2
import os
import numpy as np


def gen_merge_pages():
    basepath = 'download'
    out_path = 'out_images'
    for filename in os.listdir(out_path):
        os.remove(os.path.join(out_path, filename))
    files = [os.path.join(basepath, v) for v in os.listdir(basepath)]
    img_h, img_w = 370, 265
    space = 2

    img_list = []
    for fname in files[:]:
        page_img = cv2.imdecode(np.fromfile(fname, np.uint8), cv2.IMREAD_UNCHANGED)  # 当文件路径包含中文时用imdecode读入
        page_img = cv2.cvtColor(page_img, cv2.COLOR_BGRA2BGR)
        page_img = cv2.resize(page_img, (img_w, img_h))
        print(fname, page_img.shape)
        img_list.append(page_img)

    result_pages = []
    rows, cols, channel = 3, 3, 3
    for page_start in range(0, len(img_list), rows * cols):
        page_img = np.ndarray((img_h * rows + space * (rows - 1), img_w * cols + space * (cols - 1), channel), np.uint8)
        page_img += 255
        print(page_start, page_img.shape)
        for r in range(rows):
            for c in range(cols):
                top = r * (img_h + space)
                bottom = top + img_h
                left = c * (img_w + space)
                righ = left + img_w
                cur_img_index = page_start + r * cols + c  # 按先行后列计算当前图像索引号
                if cur_img_index < len(img_list):
                    page_img[top:bottom, left:righ] = img_list[cur_img_index]
        result_pages.append(page_img)

    for idx, page_img in enumerate(result_pages):
        save_file_name = os.path.join(out_path, f'{idx}.png')
        cv2.imwrite(save_file_name, page_img)
        # cv2.imshow(f'{idx}', img)
        # cv2.waitKey()
        # cv2.destroyAllWindows()


if __name__ == '__main__':
    gen_merge_pages()
