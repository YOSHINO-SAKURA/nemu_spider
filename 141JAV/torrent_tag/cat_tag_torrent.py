import random
import re
import time

import requests
from fake_useragent import UserAgent


class cat_torrent:
    def __init__(self):
        self.headers = {"User-Agent": UserAgent().random}
        self.url = "https://www.141jav.com/tag/{}"
        self.torrentlist = []
        self.list2 = []
        self.regex = '<a style="margin-top: auto;" .*? title="Magnet torrent" href="(.*?)" .*? fa-magnet"></i></a>'
        self.num = 1
        # self.url1 = purl
        # self.num = "https://www.141jav.com/tag/Pantyhose?page=2"

    # 开始爬取当前页面的torrent
    def spider_torrent(self, url):
        for i in range(10):
            try:
                for i in range(15):
                    html = requests.get(url=url, headers=self.headers, timeout=20).text
                    time.sleep(random.uniform(0, 2))
                    pattern = re.compile(self.regex, re.S)
                    r_list = pattern.findall(html)
                    for i in r_list:
                        self.torrentlist.append(i)
                    break
                break
            except Exception as e:
                print(e)
                print('Retry')

    # torrent写入txt
    def torrent_write_txt(self, tag):
        for i in self.torrentlist:
            with open('{}.txt'.format(tag), "a+") as f:
                f.write(i + '\n')

    def run(self, tag):
        print("开始时间" + time.ctime())
        start_time = time.time()
        while True:
            url = self.url.format(tag) + '?page={}'.format(self.num)
            # "https://www.141jav.com/tag/{search_url}" + ?page={num = 1 }
            # "https://www.141jav.com/tag/Pantyhose?page=1"
            self.spider_torrent(url)

            if not self.torrentlist:
                print("当前页面是空的")
                break
            elif self.torrentlist == self.list2:
                break
            else:
                self.torrent_write_txt(tag)
            print('爬取第{}页结束'.format(self.num))
            time.sleep(random.uniform(0, 5))
            self.num += 1
            self.list2 = self.torrentlist
            self.torrentlist = []

        print("结束时间" + time.ctime())

        end_time = time.time()
        math_time = end_time - start_time
        seconds = math_time
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        print("用时%d小时%02d分钟%02d秒" % (h, m, s))


if __name__ == '__main__':
    run = cat_torrent()
    tag = input(str("输入tag目标:"))
    run.run(tag)
