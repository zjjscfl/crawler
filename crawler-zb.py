#!/usr/bin/env python3

from datetime import date
import sys
import os
import re
import requests
import uuid
import xml.etree.ElementTree as ET
import time

dictCode = {
    'zjrb': {
        'name': '浙江日报',
        'pageurl': 'node_18.htm',
        'WH': '300*478',
        'host': 'http://zjrb.zjol.com.cn/'

    },
    'qjwb': {
        'name': '钱江晚报',
        'pageurl': 'node_77.htm',
        'WH': '300*488',
        'host': 'http://qjwb.thehour.cn/'
    }
}


def getPage(day, code, pageurl):
    url = dictCode[code]['host'] + 'html/{:%Y-%m/%d}/{}'.format(day, pageurl)
    resp = requests.get(url)
    resp.encoding = 'utf-8'
    return resp.text


def savePDF(code, day, pdfurl, bc):
    pdfdir = '{}/PDF/{:%Y/%Y%m%d}/{}'.format(code, day, bc)
    if not os.path.exists(pdfdir):
        os.makedirs(pdfdir)


    pdfurl = dictCode[code]['host'] + \
             re.search(r'<li id="down-edpdf" ><a target=_blank href=../../../([\s\S]*?)>下载PDF文件</a></li>', getPage(day, code, pdfurl),
                      re.M | re.I).group(1)

    pdfname = pdfurl.split('/')[-1]
    # 目前不支持下载
    with open(os.path.join(pdfdir, pdfname), 'wb') as of:
        of.write(requests.get(pdfurl).content)
    return pdfname
    # return ''


def saveJPG(code, day, imgurl, bc, prefix):
    imgdir = '{}/{}/{:%Y/%Y%m%d}/{}'.format(code, prefix, day, bc)
    if not os.path.exists(imgdir):
        os.makedirs(imgdir)
    imgname = imgurl.split('/')[-1].split('?')[0]
    with open(os.path.join(imgdir, imgname), 'wb') as of:
        of.write(requests.get(imgurl).content)
    return imgname


def saveXML(code, day, bc, et):
    xmldir = '{}/xml/{:%Y/%Y%m%d}/{}'.format(code, day, bc)
    if not os.path.exists(xmldir):
        os.makedirs(xmldir)
    xmlname = '{}{:%Y%m%d}{}v01h.xml'.format(code.upper(), day, bc)
    et.write(os.path.join(xmldir, xmlname), encoding='gb2312', xml_declaration=True)
    return xmlname


def getPageImgList(html):
    return re.findall(r'shape="polygon" href="(.+?)">', html)


def getZBdict(html):
    list = re.findall(r'<Area .*?coords="(.*?)" shape="polygon" href="(.+?)">', html)
    dict = {}
    for item in list:
        dict[item[1]] = item[0]
    return dict


def getZB(dictZB, WH):
<<<<<<< HEAD
    ZB = ''
    listZB = dictZB.split(',', -1)
    listWH = WH.split('*', -1)
    w = float(listWH[0])
    h = float(listWH[1])
    n = len(listZB)
    counter = 0
    while counter < n:
        ZB = ZB + "<{}%,{}%>".format(round(float(listZB[counter]) * 100 / w, 2),
                                     round(float(listZB[counter + 1]) * 100 / h, 2))
        counter += 2
    return ZB
=======
     ZB =''
     listZB=  dictZB.split(',',-1)
     listWH=  WH.split('*',-1)
     w=float(listWH[0])
     h=float(listWH[1])
     n=len(listZB)
     counter = 0
     while counter < n:
       ZB=ZB+"<{}%,{}%>".format(round(float(listZB[counter])*100/w,2),round(float(listZB[counter+1])*100/h,2))
       counter += 2
     return ZB

def getMatch( text, pattern ):
  result = re.search(pattern, text, re.MULTILINE|re.DOTALL )
  if( result ):
    return result.group(1)
  else:
    return ''

def getContent( html ):
  content = ''
  result = re.search(r'<founder-content>([\s\S]+?)</founder-content>', html, re.MULTILINE|re.DOTALL )
  if( result ):
    c1=result.group(1)
    clist = re.findall( r'<P>([\s\S]*?)</P>', c1 )
  
    for c2 in clist:
      content = content + c2 + '\n'
  return content

def getImages( html ):
  return re.findall( r'<IMG src="(.*?)">', html)
  # result = re.search(r'<div class="main_ar_pic_text">([\s\S]+?)</div>', html, re.MULTILINE|re.DOTALL )
  # if( result ):
  #   c1=result.group(1)
  #   imglist =re.findall( r'<IMG src="(.*?)">', c1 )
  #   return imglist
  # else:
  #   return ''
>>>>>>> a70a4ea41a8ea3398f51e2fbf612a9245f7991cd


def getMatch(text, pattern):
    result = re.search(pattern, text, re.MULTILINE | re.DOTALL)
    if (result):
        return result.group(0)
    else:
        return ''


def getContent(html):
    content = ''
    result = re.search(r'<founder-content>([\s\S]+?)</founder-content>', html, re.MULTILINE | re.DOTALL)
    if (result):
        c1 = result.group(1)
        clist = re.findall(r'<P>([\s\S]*?)</P>', c1)

        for c2 in clist:
            content = content + c2 + '\n'
    return content


def getImages(html):
    return re.findall(r'<IMG src="(.*?)">', html)
    # result = re.search(r'<div class="main_ar_pic_text">([\s\S]+?)</div>', html, re.MULTILINE|re.DOTALL )
    # if( result ):
    #   c1=result.group(1)
    #   imglist =re.findall( r'<IMG src="(.*?)">', c1 )
    #   return imglist
    # else:
    #   return ''


def dealBC(code, day, bc, bm, pageurl, pagetext, pageimage):
    Dayinfo = ET.Element("Dayinfo")
    DescriptionMetaGroup = ET.SubElement(Dayinfo, "DescriptionMetaGroup")
    RQ = ET.SubElement(DescriptionMetaGroup, 'RQ')
    RQ.text = '{:%Y-%m-%d}'.format(day)
    MC = ET.SubElement(DescriptionMetaGroup, 'MC')
    MC.text = dictCode[code]['name']
    NQ = ET.SubElement(DescriptionMetaGroup, 'NQ')
    QS = ET.SubElement(DescriptionMetaGroup, 'QS')
    item = ET.SubElement(Dayinfo, "item")

    pdfname = savePDF(code, day, pageurl, bc)

    jpgname = saveJPG(code, day, dictCode[code]['host'] + pageimage.replace('../../../', ''), bc, 'JPG')

    dtxt = getPage(day, code, pageurl)
    dictZB = getZBdict(dtxt)  # 获取Url与坐标的映射

    # pageImgList=getPageImgList(dtxt) # 遍历获取图片列表
    # for page in pageImgList:
    #   pageImg=getImages(getPage( day, code,page))
    #   for img in pageImg:
    #     saveJPG(code, day,dictCode[code]['host']+img.replace('../../../',''), bc, 'xml' )

    titlelist = re.findall(r'<li id=mp.*><a href=(.+?)>([\s\S]*?)</a>([\s\S]*?)</li>', dtxt, re.MULTILINE)

    for title in titlelist:
        MetaInfo = ET.SubElement(item, "MetaInfo")
        KY = ET.SubElement(MetaInfo, "KY")
        KY.text = str(uuid.uuid4())
        GJID = ET.SubElement(MetaInfo, "GJID")
        GJID.text = str(uuid.uuid4())
        BC = ET.SubElement(MetaInfo, "BC")
        BC.text = bc
        BM = ET.SubElement(MetaInfo, "BM")
        BM.text = bm
        ZB = ET.SubElement(MetaInfo, "ZB")
        #  ZB.text = dictZB[title[0]] # 还需要处理
        Url = ET.SubElement(MetaInfo, "Url")
        Url.text = dictCode[code]['host'] + 'html/{:%Y-%m/%d}/{}'.format(day, title[0].replace('./', ''))
        article = requests.get(Url.text)
        article.encoding = 'utf-8'
        BT = ET.SubElement(MetaInfo, "BT")
        BT.text = getMatch(article.text, r'<h1 class="main-article-title">(.*?)</h1>')
        FB = ET.SubElement(MetaInfo, "FB")
        FB.text = getMatch(article.text, r'<h3 class="main-article-subtitle">(.*?)</h3>')
        YT = ET.SubElement(MetaInfo, "YT")
        YT.text = getMatch(article.text, r'<h3 class="main-article-pretitle">(.*?)</h3>')
        XB = ET.SubElement(MetaInfo, "XB")
        TX = ET.SubElement(MetaInfo, "TX")
        TX.text = getContent(article.text)
        ZY = ET.SubElement(MetaInfo, "ZY")
        QY = ET.SubElement(MetaInfo, "QY")
        HJ = ET.SubElement(MetaInfo, "HJ")
        ZZ = ET.SubElement(MetaInfo, "ZZ")
        CBZZ = ET.SubElement(MetaInfo, "CBZZ")
        BJ = ET.SubElement(MetaInfo, "BJ")
        FL = ET.SubElement(MetaInfo, "FL")
        FBLX = ET.SubElement(MetaInfo, "FBLX")
        WZBJ = ET.SubElement(MetaInfo, "WZBJ")
        TC = ET.SubElement(MetaInfo, "TC")
        LM = ET.SubElement(MetaInfo, "LM")
        CBBM = ET.SubElement(MetaInfo, "CBBM")
        BJBM = ET.SubElement(MetaInfo, "BJBM")
        WJLX = ET.SubElement(MetaInfo, "WJLX")
        QYR = ET.SubElement(MetaInfo, "QYR")
        GG = ET.SubElement(MetaInfo, "GG")
        GGLX = ET.SubElement(MetaInfo, "GGLX")
        TP = ET.SubElement(MetaInfo, "TP")
        TPinfo = ET.SubElement(MetaInfo, "TPinfo")
        Source = ET.SubElement(TPinfo, "Source")
        Target = ET.SubElement(TPinfo, "Target")
        JP = ET.SubElement(Source, "JP")
        JP.text = jpgname
        PD = ET.SubElement(Source, "PD")
        PD.text = pdfname
        WH = ET.SubElement(Source, "WH")
        ZB.text = getZB(dictZB[title[0]], dictCode[code]['WH'])
        WH.text = dictCode[code]['WH']
        Imageinfo = ET.SubElement(MetaInfo, "Imageinfo")
        images = getImages(article.text)

        for image in images:
            name = saveJPG(code, day, dictCode[code]['host'] + image.replace('../../../', ''), bc, 'xml')
            Contnet = ET.SubElement(Imageinfo, "Contnet")  # 拼写有错？？？
            CT = ET.SubElement(Contnet, "CT")
            CT.text = name
            TS = ET.SubElement(Contnet, "TS")
            TZ = ET.SubElement(Contnet, "TZ")

    saveXML(code, day, bc, ET.ElementTree(Dayinfo))


def main():
    if len(sys.argv) == 1:
        day = date.today()
    else:
        groups = re.match(r'(\d{4})(\d{2})(\d{2})', sys.argv[1]).groups()
        day = date(int(groups[0]), int(groups[1]), int(groups[2]))

    newspaper = ['zjrb', 'qjwb']
    for code in newspaper:
        log_mark = False
        if os.path.exists('log.txt'):
            f = open('log.txt', 'r')  # 以读方式打开文件
            for line in f.readlines():  # 依次读取每行
                line = line.strip()  # 去掉每行头尾空白
                if not len(line) or line.startswith('#'):  # 判断是否是空行或注释行
                    continue  # 是的话，跳过不处理
                elif line == (code + str(day)):
                    log_mark = True
            f.close()

        if not log_mark:
            pagetext = getPage(day, code, dictCode[code]['pageurl'])  # 获得版面页面
            pagelist = re.findall(r'href=(.+\.htm).*>([^<>]+)版：([^<>]+)<', pagetext, re.MULTILINE)
            pageimage = re.findall(r'filepath="(.*.jpg)"', pagetext, re.MULTILINE)
            pagelist_len = len(pagelist)
            for i in range(pagelist_len):
                BC = pagelist[i][1].replace('\n', '').replace('\r', '')
                BM = pagelist[i][2]
                dealBC(code, day, BC, BM, pagelist[i][0].replace('./', ''), pagetext, pageimage[i])
                # time.sleep(1)
                if i == (pagelist_len - 1):
                    f = open('log.txt', 'a')
                    f.write(code + str(day) + '\n')
                    f.close()


main()
