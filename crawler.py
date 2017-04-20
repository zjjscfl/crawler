#!/usr/bin/env python3

from datetime import date
import sys
import re
import requests

baseurl = 'http://hzdaily.hangzhou.com.cn/hzrb/'

def getPageList( day ):
  url = '{}{:%Y/%m/%d/page_list_%Y%m%d.html}'.format(baseurl,day)
  resp = requests.get(url)
  return resp.text
#  return re.match( r'href=\"(.+)\"', resp.text ).groups;
  
if len(sys.argv)==1 :
  day = date.today()
else:
  groups = re.match( r'(\d{4})(\d{2})(\d{2})', sys.argv[1] )
  day = date( int(groups[0]), int(groups[1]), int(groups[2]) )
pagelist = getPageList( day )
print( pagelist )