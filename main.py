#!/usr/bin/env python
#-*-coding:utf-8-*-

import os,sys,re
import argparse,urllib,urllib2

def argParse():
    parser = argparse.ArgumentParser(description='scrapy picutres from certain websites.')
    parser.add_argument('-u', metavar='url', help='the url of the website')
    parser.add_argument('-b', metavar='begin page', default = 1, help='the begin of page')
    parser.add_argument('-e', metavar='end page', default = 10, help='the end of the page')
    args = parser.parse_args()
    return vars(args)

def getHtml(url):
    user_agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
    headers = {'User-Agent':user_agent}
    try:
        request = urllib2.Request(url,headers = headers)
        page = urllib2.urlopen(request)
        html = page.read()
        return html
    except urllib2.URLError, e:
        if hasattr(e,"code"):
            print e.code
        if hasattr(e,"reason"):
            print e.reason
 
def getLink(html):
    reg = r'a href="(view-.+?\.html)"'
    link_pattern = re.compile(reg)
    link_list = re.findall(link_pattern,html)
    return link_list
	
def getImg(html):
    name_reg = r'</span> (.+-\d+)'
    name_pattern = re.compile(name_reg)
    name_list = re.findall(name_pattern,html)

    img_reg = r'img src="(.+?\.jpg)"'
    img_pattern = re.compile(img_reg)
    img_list = re.findall(img_pattern,html)
    return name_list,img_list

def saveImg(name_list,img_list):
    main_dir = os.getcwd()
    pic_dir = os.path.join(main_dir, name_list[0])
    if not os.path.exists(pic_dir):os.makedirs(pic_dir)
    n = 1
    for imgUrl in img_list:
        if n > 2:break
        imageContents = getHtml(imgUrl)
        fp = open('%s/%s.jpg'%(pic_dir,n),'wb')
        fp.write(imageContents)
        fp.close()
        n += 1

def wrap():
    args = argParse()
    print args
    url_list = []
    for i in range(int(args['b']), int(args['e'])+1):
        url = re.sub(r'\d', str(i), args['u'])
        print url
        html = getHtml(url)
        link = getLink(html)
        tmp = re.findall(r'(https://.*?/).*?\.html', args['u'])
        print tmp
        print link
        flag = 1
        for j in link:
            #if flag > 2:break
            new_url = tmp[0] +j
            print new_url
            page = getHtml(new_url)
            name_list,img_list = getImg(page)
            saveImg(name_list,img_list)
            flag += 1			

if __name__ == '__main__':
     wrap()