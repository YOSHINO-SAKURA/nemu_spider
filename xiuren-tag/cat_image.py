import random
import re
import time
import os
import requests
from fake_useragent import UserAgent


# https://www.xiurenb.cc/plus/search/index.asp?keyword=


class Cat_Search_XiuRen_Image():
    def __init__(self, search):
        self.headers = {"User-Agent": UserAgent(verify_ssl=False).random}
        self.http = 'https://www.xiurenb.cc/'
        self.search_url = "https://www.xiurenb.cc/plus/search/index.asp?keyword="  # XiuRen/10309
        self.search = search
        self.name = ''
        self.list_url1 = []
        self.num = 0
        # ['IMiss/10324', 'MFStar/10322']
        self.list_img1 = []
        self.count = 0
        self.url_pgnum = 1
        self.img_pgnum = 1

    def mk_img_dir(self):
        if os.path.exists("img"):
            return print("img文件夹已存在")
        else:
            os.mkdir("img")
            return print("已创建img文件夹")

    # 获取这搜索页面并且将获得的网址丢到列表里：
    # 获得名字
    def cat_url_list(self, url):
        try:
            for j in range(15):
                html = requests.get(url=url, headers=self.headers, timeout=20)
                html.encoding = 'utf-8'
                html = html.text

                time.sleep(random.uniform(0, 2))
                regex = '<h2><a href="/(.*?).html"'
                pattern = re.compile(regex, re.S)
                r_list = pattern.findall(html)
                if r_list:
                    for i in r_list:
                        self.list_url1.append(i)
                        print('正在填装搜索后的单个网址' + i)
                else:
                    self.num = 1
                break
        except Exception as e:
            print(e)
            print('Retry')

    # 获得单个网址的图片并加载到列表里：
    def get_image_url(self, url):
        try:
            for z in range(15):
                html = requests.get(url=url, headers=self.headers, timeout=20)
                html.encoding = 'utf-8'
                html = html.text
                time.sleep(random.uniform(1, 3))
                regex2 = 'src="/uploadfile/(.*?)" /><br />'
                pattern = re.compile(regex2, re.S)
                r_list = pattern.findall(html)
                r_name = '<h1>(.*?)</h1>'
                p_name = re.compile(r_name, re.S)
                p_name = p_name.findall(html)
                if not p_name:
                    print('名字未获取，网页超出页数')
                elif p_name:
                    p_name = p_name[0]
                    self.name = p_name
                    print('名字已获取' + self.name)
                else:
                    continue
                if r_list:
                    for j in r_list:
                        self.list_img1.append(j)
                        print('正在填装单个网址里的图片地址' + j)
                else:
                    self.num = 1
                break
        except Exception as e:
            print(e)
            print('Retry')

    # 下载图片：


    def down_image(self, image, tags):
            # https://p.xiurenb.cc/uploadfile/202210/12/9F164738753.jpg
            http = 'https://p.xiurenb.cc/uploadfile/'
            directory = "img/{}/".format(tags)
            if os.path.exists(directory):
                print("img/{}/已存在".format(tags))
            else:
                os.mkdir(directory)
                print("已创建img/{}/文件夹".format(tags))

            stri = http + image
            try:
                html = requests.get(
                    url=stri, headers=self.headers, timeout=10).content
                time.sleep(random.uniform(0, 1))
                filename = directory + stri[-14:].strip()
                with open(filename, "wb") as f:
                    self.count += 1
                    f.write(html)
                    print('已经下载了%s张,' % self.count + '时间', time.ctime())
                    print()
            except Exception as e:
                print(e)
                print('Retry3')

    def run(self):
        print("开始时间" + time.ctime())
        start_time = time.time()
        self.mk_img_dir()
        # 这循环是获得搜索后的所有页数的链接
        while True:
            url2 = self.search_url + self.search + \
                '&searchtype=title&p=' + str(self.url_pgnum)
            print('搜索第{}页'.format(self.url_pgnum))
            self.cat_url_list(url=url2)
            self.url_pgnum += 1
            time.sleep(random.uniform(1, 4))
            if self.num:
                self.num = 0
                self.url_pgnum = 1
                print('搜索页面所有的链接已收录')
                break

        for i in self.list_url1:
            url = self.http + i + '.html'
            self.get_image_url(url)
            self.num = 0
            # https://www.xiurenb.cc/plus/search/index.asp?keyword=黑丝&searchtype=title&p=1
            # 这个循环是获得一个图片链接中的所有图片链接
            while True:
                url3 = self.http + i + '_{}.html'.format(self.img_pgnum)
                self.get_image_url(url3)
                self.img_pgnum += 1
                print('单个链接第{}页'.format(self.img_pgnum))
                time.sleep(random.uniform(1, 4))
                if self.num:
                    self.num = 0
                    self.img_pgnum = 1
                    print('单个链接所有的图片已收录')
                    break
            
            print('单个链接中的所有图片地址')
            print(self.list_img1)

            for j in self.list_img1:
                print('开始下载'+self.name+'图片')
                self.down_image(image=j, tags=self.name)
                    
            self.list_img1 = []

        print("结束时间" + time.ctime())

        end_time = time.time()
        seconds = end_time - start_time
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        print("用时%d小时%02d分钟%02d秒" % (h, m, s))


if __name__ == '__main__':
    search = input('输入搜索目标：')
    run = Cat_Search_XiuRen_Image(search)
    run.run()
