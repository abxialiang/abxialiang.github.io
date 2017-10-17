# coding:cp936
from PIL import Image, ImageDraw, ImageFont
import os, sys, time, glob


def get_size(original_size, des_size):
    scale = min(float(des_size[0]) / original_size[0], float(des_size[1]) / original_size[1])
    print(scale)
    return (int(scale * original_size[0]), int(scale * original_size[1]))


def handle_img(img_path):
    img = Image.open(img_path)
    if img.size[0] == img.size[1] == 800:
        print('skip', img.size)
        return
    img_background = Image.new('RGB', (800, 800), 'white')
    print(img.size)
    img = img.resize(get_size(img.size, (800, 800)), Image.ANTIALIAS)
    print(img.size)
    box_x = (0 + img_background.size[0] - img.size[0]) / 2
    box_y = (0 + img_background.size[1] - img.size[1]) / 2
    box = (box_x, box_y, box_x + img.size[0], box_y + img.size[1])
    img_background.paste(img, box)
    # img_background.save('./out/{0}'.format(os.path.basename(img_path)))
    os.rename(img_path, img_path + '.old')
    img_background.save(img_path)


for dirpath, dirnames, filenames in os.walk('e:\private\cloud_develop\yuestore\static\素材'):
    for filename in filenames:
        if 'cover.jpg' == filename:
            print(os.path.join(dirpath, filename).decode('cp936'))
            handle_img(os.path.join(dirpath, filename))
raw_input('finish')
