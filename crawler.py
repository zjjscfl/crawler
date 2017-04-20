#!/usr/bin/env python3

from datetime import date
import sys
import os
import re
import requests

basePattern = {
  'hzrb':'http://hzdaily.hangzhou.com.cn/hzrb/{:%Y/%m/%d/page_list_%Y%m%d}.html',
  'dskb':'http://hzdaily.hangzhou.com.cn/dskb/{:%Y/%m/%d/page_list_%Y%m%d}.html',
  'mrsb':'http://hzdaily.hangzhou.com.cn/mrsb/{:%Y/%m/%d/page_list_%Y%m%d}.html'
}

def getPageList( day ):
  url = basePattern['hzrb'].format(day)
  resp = requests.get(url)
  resp.encoding = 'utf-8'
  return re.findall( r'href="(http[^"]+\.pdf)".+href="([^"]+\.html)".+>(第[^<>]+)<', resp.text, re.MULTILINE )

def savePDF( day, pdflist ):
  index = 0
  for pdf in pdflist:
    index += 1
    pdfdir = 'PDF/{:%Y/%Y%m%d}/{:02d}'.format(day, index)
    if not os.path.exists( pdfdir ):
      os.makedirs( pdfdir )
    pdfname = pdf.split('/')[-1]
# 目前不支持下载
#    with open(os.path.join(pdfdir, pdfname), 'wb') as of:
#      of.write(requests.get(pdf).content)
  return

if len(sys.argv)==1 :
  day = date.today()
else:
  groups = re.match( r'(\d{4})(\d{2})(\d{2})', sys.argv[1] ).groups()
  day = date( int(groups[0]), int(groups[1]), int(groups[2]) )
pagelist = getPageList( day )
savePDF( day, map((lambda x:x[0]), pagelist) )
