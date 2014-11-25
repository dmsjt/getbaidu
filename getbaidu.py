#!/usr/bin/python
#coding:utf-8
#支持多线程
#usage:python getbaidu.py
__author__ = 'dmst'

import sys
import re
import urllib2
import urllib
import requests
import random
import threading
import os
reload(sys)
sys.setdefaultencoding('gbk')

from BeautifulSoup import BeautifulSoup

class MySearch(threading.Thread):
    def __init__(self,func,args):
        threading.Thread.__init__(self)
        self.func = func
        self.args = args
    def run(self):
        apply(self.func, self.args)
        
def search(key,file,pgnum1,pgnum2):
    user_agents = ['Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20130406 Firefox/23.0', \
                    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:18.0) Gecko/20100101 Firefox/18.0', \
                    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.26', \
                    'IBM WebExplorer /v0.94', 'Galaxy/1.0 [en] (Mac OS X 10.5.6; U; en)', \
                    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)', \
                    'Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14', \
                    'Mozilla/4.0 (compatible; MSIE 6.0; X11; Linux i686; de) Opera 10.10', \
                    'Mozilla/4.0 (compatible; MSIE 6.0; X11; Linux x86_64; en) Opera 9.60', \
                    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0; TheWorld)']    
    keyword = {'wd':key.encode("utf8")}
    key = urllib.urlencode(keyword)
    print key
    search_url = 'http://www.baidu.com/s?ie=UTF-8&word'
    '''s_url = search_url.replace('word', key)
    print "%s" % (s_url)
    req = urllib2.urlopen(s_url)'''
    path = os.path.split(os.path.realpath(__file__))[0]
    
    for count in range(int(pgnum1),int(pgnum2)):
	s_url = search_url.replace('word', key)+'&pn='+str(count*10)
        print "%s" % (s_url)
	domain = urllib2.Request(s_url)
	r = random.randint(0,7)
	domain.add_header('User-agent', user_agents[r])
	domain.add_header('connection','keep-alive')	
	req = urllib2.urlopen(s_url)	
	html=req.read()  
	soup=BeautifulSoup(html)  
	htmltxt=soup.findAll('h3')
	num = len(htmltxt)  
	print "page=%d" % (count+1)
		
	for i in range(num):  
	    p_str = htmltxt[i].contents[0]
	    try:
		u=p_str.get('href')
		r = requests.get(u.strip())
		print r.url
		res=r.url + "\n"
		file.write(res)
	    except:
		continue
        
def main():
    filename = 'url.txt'
    mode = 'w+'
    
    threads = []
    key = raw_input('input key word:')
    pgnum = raw_input("How much pages number do you want get(default=10):")
    thread = raw_input("input threads:")
    
    try:
	f = open(filename,mode)
	if pgnum == "":
	    pgnum = 10    
	if int(thread):
	    thread = int(thread)
	if thread > pgnum:
	    print '线程数最好小于页面数'	
	if pgnum % thread !=0:
	    num = pgnum / thread +1
    except:
        print 'wtire url.txt failed'
    finally:
        f.close()
        
if __name__ == '__main__':
    main()