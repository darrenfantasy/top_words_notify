#coding=utf8  
import requests  
import re  
import xlrd  
import xlwt  
import time  
from bs4 import BeautifulSoup  
myfile=xlwt.Workbook()  
table1=myfile.add_sheet(u"实时热搜榜",cell_overwrite_ok=True)  
table1.write(0,0,u"热搜关键词")  
table1.write(0,1,u"热搜指数")  
  
table2=myfile.add_sheet(u"热点热搜榜",cell_overwrite_ok=True)  
table2.write(0,0,u"热搜关键词")  
table2.write(0,1,u"热搜指数")  
  
table3=myfile.add_sheet(u"名人热搜榜",cell_overwrite_ok=True)  
table3.write(0,0,u"热搜关键词")  
table3.write(0,1,u"热搜指数")  
  
table4=myfile.add_sheet(u"潮流热搜榜",cell_overwrite_ok=True)  
table4.write(0,0,u"热搜关键词")  
table4.write(0,1,u"热搜指数")  
  
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'  
headers = { 'User-Agent' : user_agent }  
#print soup.prettify()  
class sousuo():  
    def __init__(self,url,table):  
        self.url=url  
        self.table=table  
          
    def chaxun(self):  
        url = self.url  
        r=requests.get(url,headers=headers)  
        html=r.text  
  
        soup=BeautifulSoup(html)  
        #print soup.prettify()  
        #获取热搜名称  
        i=1  
        for tag in soup.find_all(href=re.compile("Refer=top"),target="_blank"):  
            if tag.string is not None:  
                print tag.string  
                self.table.write(i,0,tag.string)  
                i+=1  
  
        #获取热搜关注数  
        j=1  
        for tag in soup.find_all(class_="star_num"):  
            if tag.string is not None:  
                print tag.string  
                self.table.write(j,1,tag.string)  
                j+=1  
  
s1=sousuo('http://s.weibo.com/top/summary?cate=realtimehot',table1)  
s1.chaxun()  
s2=sousuo('http://s.weibo.com/top/summary?cate=total&key=all',table2)  
s2.chaxun()  
s3=sousuo('http://s.weibo.com/top/summary?cate=total&key=person',table3)  
s3.chaxun()  
s4=sousuo('http://s.weibo.com/top/summary?cate=total&key=films',table4)  
s4.chaxun()  
filename=str(time.strftime('%Y%m%d%H%M%S',time.localtime()))+"weibo.xlsx"  
myfile.save(filename)  
print u"完成%s的微博热搜备份"%time.strftime('%Y%m%d%H%M%S',time.localtime())