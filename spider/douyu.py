#!/usr/bin/env python
# -*- coding:utf-8 -*-

from selenium.webdriver import Firefox
from bs4 import BeautifulSoup as bs
import sys


class Douyu():
    
    def __init__(self):
        self.driver = Firefox()
        self.img_count = 0
        self.num = 0
        self.count = 0

    def douyuSpider(self):
        self.driver.get("https://www.douyu.com/directory/all")
        f = open('douyu.txt','w')
        f2 = open('fenlei.txt','a')
        while True:
            soup = bs(self.driver.page_source, "lxml")
            # 主播名, 返回列表
            names = soup.find_all("span", {"class" : "dy-name ellipsis fl"})
            # 观众人数, 返回列表
            numbers = soup.find_all("span", {"class" :"dy-num fr"})
            # 房间名
            titles = soup.find_all("h3",{"class":"ellipsis"})
            # 封面地址
            imgs = soup.find_all("img",{"class":"JS_listthumb"})
            dtypes = soup.find_all('span',{"class":"tag ellipsis"})
            for img in imgs:
                if not img.get("alt"):
                    imgs.remove(img)
                    continue
                print(img.get("data-original"))
            for name, number ,title ,img ,dtype in zip(names, numbers,titles,imgs,dtypes):
                f.write(u"观众人数:\t" + number.get_text().strip() + u"-\t主播名: " + name.get_text().strip()+' ')
                f.write(u'房间标题:\t' + title.get_text().strip()+' ')
                f.write(u'封面链接：\t' + img.get("data-original")+' ')
                f.write(u'分类：\t' + dtype.get_text().strip())
                f.write(u'\n')
                self.num += 1
                count = number.get_text().strip()
                if count[-1]=="万":
                    countNum = float(count[:-1])*10000
                else:
                    countNum = float(count)
                self.count += countNum
                f2.write(u'%s#'%dtype.get_text().strip())
            # 一直点击下一页
            self.driver.find_element_by_class_name("shark-pager-next").click()
            # 如果在页面源码里找到"下一页"为隐藏的标签，就退出循环
            if self.driver.page_source.find("shark-pager-disable-next") != -1:
                f.close()
                f2.close()
                break
        print("当前直播人数:%s" % self.num)
        print("当前观众人数:%s" % self.count)


if __name__ == "__main__":
    d = Douyu()
    d.douyuSpider()