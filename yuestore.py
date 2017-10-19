from flask import Flask, render_template
from flask_bootstrap import Bootstrap
import gevent
from gevent.pywsgi import WSGIServer
import random
import tool
import os
import sys
import json
import time
import threading

RESOUCE_VERSION = "2017-10-21"
app = Flask(__name__)
Bootstrap(app)


class Commodity(object):
    def __init__(self):
        name = ''  # 商品标题
        cover_path = ''  # 封面路径
        price = 0.00  # 价格
        url = ''


def createsumpage(typename):
    datas = []
    for dirpath, dirnames, filenames in os.walk('./static/素材'):
        if typename not in dirpath:
            continue
        jsonpath = os.path.join(dirpath, 'describe.txt')
        if os.path.exists(os.path.join(dirpath, 'cover.jpg')) and os.path.exists(jsonpath):
            jdata = json.loads(open(jsonpath, encoding='utf8').read())
            o = Commodity()
            o.cover_path = os.path.join(dirpath, 'cover.jpg?ver={}'.format(RESOUCE_VERSION))
            o.name = jdata["name"]
            o.price = jdata["price"]
            o.url = 'product' + os.path.basename(dirpath) + '.html'
            datas.append(o)

    page = render_template('home.html', title="首页", commoditys=datas)
    # open('E:\private\cloud_develop\yuestore\index.html', 'wb').write(page.encode('utf8'))
    return page


@app.route('/')
@app.route('/all.html')
def home():
    return createsumpage('')


@app.route('/manabove.html')
def manabove():
    return createsumpage('男上')


@app.route('/manbelow.html')
def manbelow():
    return createsumpage('男下')


@app.route('/belt.html')
def belt():
    return createsumpage('皮带')


@app.route('/shoe.html')
def shoe():
    return createsumpage('鞋子')


@app.route('/product<productname>.html')
def product(productname):
    imgpaths = []
    for i in range(1, 10):
        imgpath = os.path.join('./static/素材', productname) + '/{}.jpg'.format(i)
        if os.path.exists(imgpath):
            imgpaths.append(imgpath.replace('./', '/'))
        else:
            break
    jsonpath = os.path.join('./static/素材', productname) + '/describe.txt'
    jdata = json.loads(open(jsonpath, encoding='utf8').read())
    page = render_template('product.html', imgpaths=imgpaths, xname=jdata["name"], xprice=jdata["price"])
    return page


def build():
    time.sleep(2)
    import requests
    from lxml import etree
    r = requests.get('http://192.168.199.195:8000', timeout=5)
    assert r.status_code == 200
    page = r.content
    root = etree.HTML(page)
    for url in root.xpath('//a[@href]'):
        if 'html' in url.get('href'):
            page = requests.get(u'http://192.168.199.195:8000/{}'.format(url.get('href')).encode('utf8'))
            pagename = url.get('href')
            print(pagename)
            open('E:\private\cloud_develop\yuestore\\{}'.format(pagename), 'wb').write(page.content)
            if pagename == '/all.html':
                open('E:\private\cloud_develop\yuestore\\{}'.format('index.html'), 'wb').write(page.content)

    print('build finish')


if __name__ == '__main__':
    workdir = os.path.dirname(os.path.abspath(sys.argv[0]))
    os.chdir(workdir)

    threading.Thread(target=build).start()
    WSGIServer(('0.0.0.0', 8000), app).serve_forever()  # 选项log=None可关闭日志功能
