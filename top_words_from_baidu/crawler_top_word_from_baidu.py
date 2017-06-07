#!usr/bin/python
# -*- coding: utf-8 -*-
import requests  
import re  
import xlrd  
import xlwt  
import time  
from bs4 import BeautifulSoup  
myfile=xlwt.Workbook()  
table1=myfile.add_sheet(u"电影",cell_overwrite_ok=True)  
table1.write(0,0,u"热搜关键词")  
table1.write(0,1,u"类别")  
  
table2=myfile.add_sheet(u"电视剧",cell_overwrite_ok=True)  
table2.write(0,0,u"热搜关键词")  
table2.write(0,1,u"类别")  
  
table3=myfile.add_sheet(u"综艺",cell_overwrite_ok=True)  
table3.write(0,0,u"热搜关键词")  
table3.write(0,1,u"类别")  
  
table4=myfile.add_sheet(u"动漫",cell_overwrite_ok=True)  
table4.write(0,0,u"热搜关键词")  
table4.write(0,1,u"类别")  

table5=myfile.add_sheet(u"人物",cell_overwrite_ok=True)  
table5.write(0,0,u"热搜关键词")  
table5.write(0,1,u"类别")  
  
table6=myfile.add_sheet(u"娱乐热点",cell_overwrite_ok=True)  
table6.write(0,0,u"热搜关键词")  
table6.write(0,1,u"类别")  
  
table7=myfile.add_sheet(u"体育热点",cell_overwrite_ok=True)  
table7.write(0,0,u"热搜关键词")  
table7.write(0,1,u"类别")  

table8=myfile.add_sheet(u"音乐",cell_overwrite_ok=True)  
table8.write(0,0,u"热搜关键词")  
table8.write(0,1,u"类别") 

class BaiduAnalyze(object):
    """docstring for BaiduAnalyze"""
    def __init__(self, url,table):
        super(BaiduAnalyze, self).__init__()
        self.url = url
        self.table = table

    def analyze(self):
        url = self.url
        r = requests.get(url)
        r.encoding = "gb2312"
        html = r.text

        soup = BeautifulSoup(html,'html.parser')
        # print soup.prettify()
        words_list = []
        tag_list = []
        for tag in soup.find_all('div','box-cont'):
            tag_name = tag.find(href=re.compile('./buzz')).string
            tag_list.append(tag_name)
        i = 0
        for word in soup.find_all(href=re.compile('cl=3&tn=SE'),target="_blank"):
            if word.string is not None:
                z = i/10
                print word.string+tag_list[z]
                words_list.append(word.string.encode('utf-8'))
                self.table.write(i,0,word.string)
                self.table.write(i,1,tag_list[z])
                i = i+1
        return words_list

    def analyze_music(self):
        url = self.url
        r = requests.get(url)
        r.encoding = "gb2312"
        html = r.text

        soup = BeautifulSoup(html,'html.parser')
        # print soup.prettify()
        words_list = []
        tag_list = []
        for tag in soup.find_all('div','box-cont'):
            tag_name = tag.find(href=re.compile('http://music.baidu.com')).string
            tag_list.append(tag_name)
        i = 0
        for word in soup.find_all(href=re.compile('http://music.baidu.com/song'),target="_blank"):
            if word.string is not None:
                z = i/10
                print z
                print word.string+tag_list[z]
                words_list.append(word.string.encode('utf-8'))
                self.table.write(i,0,word.string)
                self.table.write(i,1,tag_list[z])
                i = i+1
        return words_list


    def analyze_hot(self):
        url = self.url
        r = requests.get(url)
        r.encoding = "gb2312"
        html = r.text

        soup = BeautifulSoup(html,'html.parser')
        # print soup.prettify()
        words_list = []
        i = 0
        for tag in soup.find_all(href=re.compile('cl=3&tn=SE'),target="_blank"):
            if tag.string is not None:
                print tag.string
                words_list.append(tag.string.encode('utf-8'))
                self.table.write(i,0,tag.string)
                i+=1
        return words_list
def crawler_top_key_from_baidu():
    top_keys = []
    # ba = BaiduAnalyze('http://top.baidu.com/buzz?b=344&c=513&fr=topbuzz_b11_c513')#热点下的娱乐热点
    # top_keys = ba.analyze()
    b_y_music = BaiduAnalyze('http://top.baidu.com/category?c=33&fr=topcategory_c2',table8)#音乐
    b_y_music.analyze_music()

    b_entertainment_1 = BaiduAnalyze('http://top.baidu.com/category?c=1&fr=topcategory_c9',table1)#电影
    b_entertainment_1.analyze()
    b_entertainment_2 = BaiduAnalyze('http://top.baidu.com/category?c=2&fr=topcategory_c1',table2)#电视剧
    b_entertainment_2.analyze()
    b_entertainment_3 = BaiduAnalyze('http://top.baidu.com/category?c=3&fr=topcategory_c2',table3)#综艺
    b_entertainment_3.analyze()
    b_entertainment_5 = BaiduAnalyze('http://top.baidu.com/category?c=5&fr=topcategory_c33',table4)#动漫
    b_entertainment_5.analyze()

    b_entertainment_6 = BaiduAnalyze('http://top.baidu.com/category?c=9&fr=topbuzz_b258',table5)#人物
    b_entertainment_6.analyze()

    b_hot_en = BaiduAnalyze('http://top.baidu.com/buzz?b=344&c=513&fr=topcategory_c513',table6)#娱乐热点
    b_hot_en.analyze_hot()
    b_hot_pe = BaiduAnalyze('http://top.baidu.com/buzz?b=11&c=513&fr=topbuzz_b344_c513',table7)#体育热点
    b_hot_pe.analyze_hot()
    return top_keys

crawler_top_key_from_baidu()
filename=str(time.strftime('%Y%m%d%H%M%S',time.localtime()))+"baidu.xlsx"  
myfile.save(filename)  
