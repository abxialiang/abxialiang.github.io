# coding:cp936
from PIL import Image, ImageDraw, ImageFont
import os, sys, time, glob
import json
import random
import mymodul


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
    # os.rename(img_path, img_path + '.old')
    img_background.save(img_path)


def tominiimg(imgpath):
    img = Image.open(imgpath)
    print(img.size)
    img.thumbnail((200, 200), Image.ANTIALIAS)
    img.save(os.path.join(os.path.dirname(imgpath), 'cover.jpg'), quality=88)


# 封面图片转换为800*800
# for dirpath, dirnames, filenames in os.walk('e:\private\cloud_develop\yuestore\static\素材'):
#     for filename in filenames:
#         if 'cover.jpg' == filename:
#             print(os.path.join(dirpath, filename).decode('cp936'))
#             handle_img(os.path.join(dirpath, filename))  # 调整封面图片尺寸为800*800
#             tominiimg(os.path.join(dirpath, filename).decode('cp936'))  # 创建封面图片缩略图
# raw_input('800 finish,start miniimg?')


# for dirpath, dirnames, filenames in os.walk('e:\private\cloud_develop\yuestore\static\素材'):
#     for filename in filenames:
#         if '1.jpg' == filename:
#             print(os.path.join(dirpath, filename).decode('cp936'))
#             tominiimg(os.path.join(dirpath, filename).decode('cp936'))  # 创建封面图片缩略图
# raw_input('miniimg finish')


# 自动化素材整理
while 1:
    time.sleep(0.5)
    import os

    basedir = u'e:\private\Desktop\衣服素材'
    jstr = open(u'e:\private\Desktop\衣服素材\cfg.txt'.encode('cp936'),'rb').read()
    print(jstr.decode('utf8'))
    jdata = json.loads(jstr.decode('utf8'))

    sondirpath = os.path.join(basedir, u'{}'.format(jdata[0]))
    sondirpath_random = sondirpath + u'{}'.format(random.randint(100, 9999))

    existdir = False
    for dirpath, dirnames, filenames in os.walk(basedir):
        print(555, os.path.basename(sondirpath), dirpath)
        if os.path.basename(sondirpath) in dirpath and u"完成" not in dirpath:
            print(dirpath)
            sondirpath = dirpath
            existdir = True

    if existdir:
        pass
    else:
        print('create dir:', sondirpath_random)
        os.mkdir(sondirpath_random)
        sondirpath = sondirpath_random

    # 自动创建描述文件
    open(os.path.join(sondirpath, 'describe.txt'), 'w').write(u'''
{{
"name":"{0}",
"price":"{1}",
"code":"{2}"
}}
    '''.format(jdata[0], jdata[1], u'货号').encode('utf8'))

    for path in mymodul.fordir_path(sondirpath,ext_filtration=u'jpg'):
        print(3334,path)
        if os.path.basename(path) not in ('1.jpg','2.jpg','3.jpg','4.jpg','cover.jpg'):
            if not os.path.exists(os.path.join(sondirpath,'1.jpg')):
                print(44,path ,os.path.join(sondirpath,'1.jpg'))
                os.rename(path ,os.path.join(sondirpath,'1.jpg'))
                handle_img(os.path.join(sondirpath,'1.jpg'))  # 调整封面图片尺寸为800*800
                tominiimg(os.path.join(sondirpath,'1.jpg'))  # 创建封面图片缩略图
                break
            if not os.path.exists(os.path.join(sondirpath,'2.jpg')):
                os.rename(path ,os.path.join(sondirpath,'2.jpg'))
                break
            if not os.path.exists(os.path.join(sondirpath,'3.jpg')):
                os.rename(path ,os.path.join(sondirpath,'3.jpg'))
                break