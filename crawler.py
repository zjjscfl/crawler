#!/usr/bin/env python3

from datetime import date
import sys
import os
import re
import requests

def getPageList( day, code ):
  url = 'http://hzdaily.hangzhou.com.cn/{}/{:%Y/%m/%d/page_list_%Y%m%d}.html'.format(code, day)
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
  return

def saveJPG( day, imgurl, bc ):
  imgdir = 'JPG/{:%Y/%Y%m%d}/{}'.format(day, bc)
  if not os.path.exists( imgdir ):
    os.makedirs( imgdir )
  imgname = imgurl.split('/')[-1].split('?')[0]
  with open(os.path.join(imgdir, imgname), 'wb') as of:
    of.write( requests.get(imgurl).content)
  return

if len(sys.argv)==1 :
  day = date.today()
else:
  groups = re.match( r'(\d{4})(\d{2})(\d{2})', sys.argv[1] ).groups()
  day = date( int(groups[0]), int(groups[1]), int(groups[2]) )
code = 'hzrb'
pagelist = getPageList( day, code )
for i in range(len(pagelist)):
  BC = pagelist[i][2]
  BM = pagelist[i][3]
  savePDF( day, pagelist[i][0], BC )
  
  detail = requests.get( 'http://hzdaily.hangzhou.com.cn/{}/{:%Y/%m/%d}/{}'.format( code, day, pagelist[i][1] ) )
  detail.encoding = 'utf-8'
  viewpage = re.search( r'src="(page_view[^"]*\.html)"', detail.text ).group(1)
  view = requests.get( 'http://hzdaily.hangzhou.com.cn/{}/{:%Y/%m/%d}/{}'.format( code, day, viewpage ) )
  view.encoding = 'utf-8'
  imgurl = re.search( r'<img src="([^"]+)".*>', view.text ).group(1)
  saveJPG( day, imgurl, BC )
  
  titlelist = re.findall( r'<area.+coords="(.*)".+href="([^"]+)">', view.text, re.MULTILINE )
  for title in titlelist:
    ZB = title[0]
    article = request.get( 'http://hzdaily.hangzhou.com.cn/{}/{:%Y/%m/%d}/{}'.format( code, day, title[1] ) )
    article.encoding = 'utf-8'
  
  

