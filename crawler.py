#!/usr/bin/env python3

from datetime import date
import sys
import os
import re
import requests

dictCode = {
  'hzrb': {
    'name': '杭州日报',
    'pattern': 'http://hzdaily.hangzhou.com.cn/hzrb/{:%Y/%m/%d/page_list_%Y%m%d}.html',
    'WH' : '644*1024'
  }
}

def getPageList( day, code ):
  url = dictCode[code]['pattern'].format(day)
  resp = requests.get(url)
  resp.encoding = 'utf-8'
  return re.findall( r'href="(http[^"]+\.pdf)".+href="([^"]+\.html)".+>第([^<>]+)版：([^<>]+)<', resp.text, re.MULTILINE )

def savePDF( day, pdfurl, bc ):
  pdfdir = 'PDF/{:%Y/%Y%m%d}/{}'.format(day, bc)
  if not os.path.exists( pdfdir ):
    os.makedirs( pdfdir )
  pdfname = pdfurl.split('/')[-1]
# 目前不支持下载
#  with open(os.path.join(pdfdir, pdfname), 'wb') as of:
#    of.write(requests.get(pdfurl).content)
#  return pdfname
  return ''

def saveJPG( day, imgurl, bc ):
  imgdir = 'JPG/{:%Y/%Y%m%d}/{}'.format(day, bc)
  if not os.path.exists( imgdir ):
    os.makedirs( imgdir )
  imgname = imgurl.split('/')[-1].split('?')[0]
  with open(os.path.join(imgdir, imgname), 'wb') as of:
    of.write( requests.get(imgurl).content)
  return imgname

def getZBdict( html ):
  list = re.findall( r'<area .*?coords="(.*?)" href="(.+?)">', html )
  dict = {}
  for item in list:
    dict[item[1]] = item[0]
  return dict

def getMatch( text, pattern ):
  result = re.search(pattern, text, re.MULTILINE|re.DOTALL )
  if( result ):
    return result.group(1)
  else:
    return ''

def getContent( html ):
  c1 = getMatch( html, r'<div class="content">(.*?)</div>' )
  clist = re.findall( r'<p>(.*?)</p>', c1 )
  content = ''
  for c2 in clist:
    content = content + c2 + '\n'
  return content

def getImages( html ):
  c1 = getMatch( html, r'<div class="content">(.*?)</div>' )
  imglist = re.findall( r'<img src="(.*?)"/>', c1 )
  return imglist

if len(sys.argv)==1 :
  day = date.today()
else:
  groups = re.match( r'(\d{4})(\d{2})(\d{2})', sys.argv[1] ).groups()
  day = date( int(groups[0]), int(groups[1]), int(groups[2]) )
code = 'hzrb'
pagelist = getPageList( day, code ) # 获得版面页面列表
for i in range(len(pagelist)):
  BC = pagelist[i][2]
  BM = pagelist[i][3]
  PD = savePDF( day, pagelist[i][0], BC )
  
  # page_detail_...
  detail = requests.get( 'http://hzdaily.hangzhou.com.cn/{}/{:%Y/%m/%d}/{}'.format( code, day, pagelist[i][1] ) )
  detail.encoding = 'utf-8'
  viewpage = re.search( r'src="(page_view.*?\.html)"', detail.text ).group(1)
  view = requests.get( 'http://hzdaily.hangzhou.com.cn/{}/{:%Y/%m/%d}/{}'.format( code, day, viewpage ) )
  view.encoding = 'utf-8'
  imgurl = re.search( r'<img src="([^"]+)".*>', view.text ).group(1)
  JP = saveJPG( day, imgurl, BC )
  dictZB = getZBdict( view.text ) #获取Url与坐标的映射
  # article_list_...
  articlelistfile = getMatch( detail.text, r'src="(article_list_.*?\.html)"' )
  articlelist = requests.get( 'http://hzdaily.hangzhou.com.cn/{}/{:%Y/%m/%d}/{}'.format( code, day, articlelistfile ) )
  articlelist.encoding = 'utf-8'
  titlelist = re.findall( r'<li><a href="(.+?)".*?>(.+?)</a></li>', articlelist.text, re.MULTILINE )
  
  print(articlelistfile)
  for title in titlelist:
    ZB = dictZB[title[0]] # 还需要处理
    Url = 'http://hzdaily.hangzhou.com.cn/{}/{:%Y/%m/%d}/{}'.format( code, day, title[0] )
    article = requests.get( Url )
    article.encoding = 'utf-8'
    BT = getMatch( article.text, r'<h1>(.*?)</h1>' )
    FB = getMatch( article.text, r'<h2>(.*?)</h2>' )
    YT = getMatch( article.text, r'<h3>(.*?)</h3>' )
    WH = dictCode[code]['WH']
    TX = getContent( article.text )
    images = getImages( article.text )
    

