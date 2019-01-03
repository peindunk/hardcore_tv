#!/usr/bin/env python
# -*- coding:utf-8 -*-

from selenium.webdriver import Firefox
from bs4 import BeautifulSoup as bs
import re


class Zhanqi():
    def __init__(self):
        self.driver = Firefox()
        self.img_count = 0
        self.num = 0
        self.count = 0

    def zhanqiSpider(self):
        self.driver.get("https://www.zhanqi.tv/lives")
        f = open('zhanqi.txt','w')
        f2 = open('fenlei.txt','a')
        for _ in range(5):
            jsCode = "var q=document.documentElement.scrollTop=100000"
            import time
            time.sleep(0.5)
            self.driver.execute_script(jsCode)
        soup = bs(self.driver.page_source, "lxml")
        # 主播名, 返回列表
        names = soup.find_all("span", {"class" : "anchor anchor-to-cut dv"})
        # 观众人数, 返回列表
        numbers = soup.find_all("span", {"class" :"dv"})
        # 房间名
        titles = soup.find_all("span",{"class":"name"})
        # 封面地址
        imgs = soup.find_all("img")
        # 分类
        dtypes = soup.find_all('span',{"class":"game-name dv"})
        # 房间id
        links = soup.find_all("a",{"class":"js-jump-link"})
        temp = []
        for img in imgs:
            if img.get("alt"):
                temp.append(img)
        imgs = temp
        temp = []
        for number in numbers:
            if len(number.get("class")) == 1 and ord(number.get_text().strip()[0])<=57:
                temp.append(number)
        numbers = temp
        temp = []
        for title in titles:
            if len(title.get("class")) == 1:
                temp.append(title)
        titles = temp
        print(len(names),len(numbers),len(titles),len(imgs),len(dtypes),len(links))

        for name, number ,title ,img ,dtype ,link in zip(names, numbers,titles,imgs,dtypes,links):
            url = "https://www.zhanqi.tv" + link.get("href")
            self.driver.get(url)
            soup = bs(self.driver.page_source, "lxml")
            scripts = soup.find_all("script")
            p = r'''"videoId":"(.*?)"'''
            for s in scripts:
                live_id = re.findall(p, s.get_text().strip())
                if live_id:
                    break
            host_img = soup.find_all('img',{"alt":name.get_text()})
            fans = soup.find('span',{"class":"dyue-mid js-room-follow-num"})
            f.write(number.get_text().strip()+'##'+name.get_text().strip()+'##'+title.get_text().strip()+'##'+
                    img.get("src")+'##'+dtype.get_text().strip()+'##'+link.get("href")+'##'+live_id[0]+'##'+
                    host_img[0].get('src')+"##"+fans.get_text())
            f.write(u'\n')
            self.num += 1

            count = number.get_text().strip()
            if count[-1]=="万":
                countNum = float(count[:-1])*10000
            else:
                countNum = float(count)
            self.count += countNum
            f2.write(u'%s#'%dtype.get_text().strip())
        print("当前直播人数:%s" % self.num)
        print("当前观众人数:%s" % self.count)

if __name__ == "__main__":
    d = Zhanqi()
    d.zhanqiSpider()

