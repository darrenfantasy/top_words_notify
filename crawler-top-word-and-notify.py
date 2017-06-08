# /usr/bin/python
# encoding:utf-8
import requests  
import time
import sys, os, re, urllib, urlparse  
import smtplib  
import traceback  
from email.mime.text import MIMEText  
from email.mime.multipart import MIMEMultipart  
reload(sys)   
sys.setdefaultencoding('utf8') 
from bs4 import BeautifulSoup

local_keyword_file = "local_keyword.txt"
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'  
headers = { 'User-Agent' : user_agent }  
class SinaAnalyze(object):
	"""docstring for SinaAnalyze"""
	def __init__(self, url):
		super(SinaAnalyze, self).__init__()
		self.url = url
	def analyze(self):
		url = self.url
		r = requests.get(url,headers=headers)
		html = r.text

		soup = BeautifulSoup(html)
		# print soup.prettify()
		words_list = []
		for tag in soup.find_all(href=re.compile("Refer=top"),target="_blank"):
			if tag.string is not None:
				words_list.append(tag.string.encode('utf-8'))
		return words_list


class BaiduAnalyze(object):
	"""docstring for BaiduAnalyze"""
	def __init__(self, url):
		super(BaiduAnalyze, self).__init__()
		self.url = url
	def analyze(self):
		url = self.url
		r = requests.get(url)
		r.encoding = "gb2312"
		html = r.text

		soup = BeautifulSoup(html,'html.parser')
		# print soup.prettify()
		words_list = []
		for tag in soup.find_all(href=re.compile('cl=3&tn=SE'),target="_blank"):
			if tag.string is not None:
				print tag.string
				words_list.append(tag.string.encode('utf-8'))
		return words_list


def crawler_top_key_from_sina():
	top_keys = []
	sa_timehot = SinaAnalyze('http://s.weibo.com/top/summary?cate=realtimehot')
	# hot_keys = sa_timehot.analyze()
	top_keys = list(set(top_keys).union(set(sa_timehot.analyze())))
	sa_all = SinaAnalyze('http://s.weibo.com/top/summary?cate=total&key=all')
	top_keys = list(set(top_keys).union(set(sa_all.analyze())))
	sa_person = SinaAnalyze('http://s.weibo.com/top/summary?cate=total&key=person')
	top_keys = list(set(top_keys).union(set(sa_person.analyze())))
	sa_films = SinaAnalyze('http://s.weibo.com/top/summary?cate=total&key=films')
	top_keys = list(set(top_keys).union(set(sa_films.analyze())))
	return top_keys


def crawler_top_key_from_baidu():
	top_keys = []
	ba = BaiduAnalyze('http://top.baidu.com/buzz?b=341&fr=topbuzz_b1')
	top_keys = ba.analyze()
	return top_keys

def get_old_keys_from_local_file():
    keywordsList = []
    if os.path.isfile(local_keyword_file)==False:
    	os.system("touch "+local_keyword_file) 
    f = open(local_keyword_file)
    lines = f.readlines()
    for x in xrange(len(lines)):
        # print lines[x].strip('\n')
        keywordsList.append(lines[x].strip('\n'))
    f.close()
    return keywordsList

def judge_is_new_key(top_keys):
	old_keys = get_old_keys_from_local_file()
	new_keys = list(set(top_keys).difference(set(old_keys)))
	add_new_key_to_local_file(new_keys)
	return new_keys


def add_new_key_to_local_file(new_keys):
    try:
    	f= open(local_keyword_file,'a+')
        for x in xrange(len(new_keys)):
        	# print(str(x)+":"+new_keys[x])
        	f.write(new_keys[x])
	        f.write('\n')
	f.close()
    except Exception, e:
        print e
    finally:
        pass

def get_new_key():
	pass

def sendmail(subject,msg,toaddrs,fromaddr,smtpaddr,password):  
    ''''' 
    @subject:邮件主题 
    @msg:邮件内容 
    @toaddrs:收信人的邮箱地址 
    @fromaddr:发信人的邮箱地址 
    @smtpaddr:smtp服务地址，可以在邮箱看，比如163邮箱为smtp.163.com 
    @password:发信人的邮箱密码 
    '''  
    mail_msg = MIMEMultipart()  
    if not isinstance(subject,unicode):  
        subject = unicode(subject, 'utf-8')  
    mail_msg['Subject'] = subject  
    mail_msg['From'] =fromaddr  
    mail_msg['To'] = ','.join(toaddrs)  
    mail_msg.attach(MIMEText(msg, 'html', 'utf-8'))  
    try:  
        s = smtplib.SMTP()  
        s.connect(smtpaddr)  #连接smtp服务器  
        s.login(fromaddr,password)  #登录邮箱  
        s.sendmail(fromaddr, toaddrs, mail_msg.as_string()) #发送邮件  
        s.quit()  
    except Exception,e:  
       print "Error: unable to send email"  
       print traceback.format_exc()
if __name__ == '__main__':
	crawler_top_key_from_baidu()
	fromaddr = "782107743@qq.com"  
	smtpaddr = "smtp.exmail.qq.com"
	toaddrs = ["xxxxx@qq.com"]  
	subject = "微博、百度热门关键词订阅"  
	password = ""
	sina_top_key_list = crawler_top_key_from_sina()
	new_key_list = judge_is_new_key(sina_top_key_list)
	baidu_top_key_list = crawler_top_key_from_baidu()
	baidu_new_key_list = judge_is_new_key(baidu_top_key_list)

	print '-------------------sina--top--------------------------'
	print len(new_key_list)
	for x in xrange(len(new_key_list)):
		print new_key_list[x]
	print '-------------------baidu--top-------------------------'
	print len(baidu_new_key_list)
	for x in xrange(len(baidu_new_key_list)):
		print baidu_new_key_list[x]
	
	if len(new_key_list)+len(baidu_new_key_list)>0:
		msg = "<h3>新浪微博热门关键词:</h3>"
		for x in xrange(len(new_key_list)):
			msg = msg+new_key_list[x]+'<br>'
		msg =msg+"<h3>百度热门关键词:</h3>"
		for x in xrange(len(baidu_new_key_list)):
			msg = msg+baidu_new_key_list[x]+'<br>'	
		sendmail(subject,msg,toaddrs,fromaddr,smtpaddr,password)
