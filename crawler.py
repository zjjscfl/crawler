#!/usr/bin/env python3

from datetime import date
import sys
import re
import requests

basePattern = {
  'hzrb':'http://hzdaily.hangzhou.com.cn/hzrb/{:%Y/%m/%d/page_list_%Y%m%d}.html',
  'dskb':'http://hzdaily.hangzhou.com.cn/dskb/{:%Y/%m/%d/page_list_%Y%m%d}.html',
  'mrsb':'http://hzdaily.hangzhou.com.cn/mrsb/{:%Y/%m/%d/page_list_%Y%m%d}.html'
}

def getPageList( day ):
  url = basePattern['hzrb'].format(day)
  print( url )
  resp = requests.get(url)
  resp.encoding = 'utf-8'
  return re.findall( r'href="(http[^"]+\.pdf)".+href="([^"]+\.html)".+>(第[^<>]+)<', resp.text, re.MULTILINE )
  
if len(sys.argv)==1 :
  day = date.today()
else:
  groups = re.match( r'(\d{4})(\d{2})(\d{2})', sys.argv[1] )
  day = date( int(groups[0]), int(groups[1]), int(groups[2]) )
pagelist = getPageList( day )
print( pagelist )
