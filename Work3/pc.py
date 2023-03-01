import csv
import re
import urllib.request
from random import randint
import pandas as pd
import numpy as np
import requests
from lxml import etree

def data_get(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
    }
    request = urllib.request.Request(url=url, headers=headers)
    response = urllib.request.urlopen(request)
    content = response.read().decode('utf-8')
    return content
    #查看源代码
    # html = requests.get(url=url, headers=headers)
    # html.encoding = 'utf-8'  # 这一行是将编码转为utf-8否则中文会显示乱码。
    # print(html.text)


def XPath(name,content):
    html = etree.HTML(content)
    # print(html)
    #//table[@class="TJNw016"][1]//tr/td/a/text()
    yf=html.xpath('//*[@id="main"]/div/div[3]/div[2]/div/table[1]//tr/td/a/text()')
    link = html.xpath('//*[@id="main"]/div/div[3]/div[2]/div/table[1]//tr/td/a/@href')
    for m,n in zip(yf, link):
        print(m + "," + 'http://tjj.ningbo.gov.cn/' + n)
        link_list='http://tjj.ningbo.gov.cn/'+n
        contents = data_get(link_list)
        html = etree.HTML(contents)
        if name == '工业':
            value=[]
            zbm1=html.xpath('//ul[@id="ivs_content"]//div//table//tr[19]/td/text()')
            value.append(zbm1)
            zbz1=html.xpath('//ul[@id="ivs_content"]//div//table//tr[20]/td/text()')
            value.append(zbz1)
            zbm2 = html.xpath('//ul[@id="ivs_content"]//div//table//tr[32]/td/text()')
            value.append(zbm2)
            zbz2 = html.xpath('//ul[@id="ivs_content"]//div//table//tr[35]/td/text()')
            value.append(zbz2)
            f = open("./data/工业.csv", 'a+', newline='', encoding='utf-8')
            for i in value:
                writer = csv.writer(f)
                text=[]
                for j in range(len(i)):
                    b = i[j].replace(u'\xa0', '')
                    text.append(b)
                writer.writerow(text)
            f.close()
        if name == '综合数据':
            value = []
            zbm = html.xpath('//ul[@id="ivs_content"]//div//table//tr[1]/td/text()')
            value.append(zbm)
            zbz1 = html.xpath('//ul[@id="ivs_content"]//div//table//tr[6]/td/text()')
            value.append(zbz1)
            zbz2 = html.xpath('//ul[@id="ivs_content"]//div//table//tr[7]/td/text()')
            value.append(zbz2)
            zbz3 = html.xpath('//ul[@id="ivs_content"]//div//table//tr[8]/td/text()')
            value.append(zbz3)
            zbz4 = html.xpath('//ul[@id="ivs_content"]//div//table//tr[9]/td/text()')
            value.append(zbz4)
            zbz5 = html.xpath('//ul[@id="ivs_content"]//div//table//tr[10]/td/text()')
            value.append(zbz5)
            f = open("./data/综合数据.csv", 'a+', newline='', encoding='utf-8')
            for i in value:
                writer = csv.writer(f)
                text = []
                for j in range(len(i)):
                    b = i[j].replace(u'\xa0', '')
                    text.append(b)
                writer.writerow(text)
            f.close()
        if name == '交通运输与港口':
            value = []
            zbm = html.xpath('//ul[@id="ivs_content"]//div//table//tr[1]/td/text()')
            value.append(zbm)
            zbz = html.xpath('//ul[@id="ivs_content"]//div//table//tr[7]/td/text()')
            value.append(zbz)
            f = open("./data/交通运输与港口.csv", 'a+', newline='', encoding='utf-8')
            for i in value:
                writer = csv.writer(f)
                text = []
                for j in range(len(i)):
                    b = i[j].replace(u'\xa0', '')
                    text.append(b)
                writer.writerow(text)
            f.close()


def tocsv():
    #工业
    data = pd.read_csv('./data/工业.csv', header=None)
    data1=pd.DataFrame()
    for i in range(int(len(data) / 4)):
        j = i * 4
        if j == 0:
            data1 = data.iloc[j:j + 4, :]
        else:
            data2 = data.iloc[j:j + 4, 1:]
            data2.index = [0,1,2,3]
            data1 = pd.concat([data1, data2], axis=1)
    data1.to_csv('./data/工业.csv', header=False, index=False)
    #综合数据
    data = pd.read_csv('./data/综合数据.csv', header=None)
    data11=pd.DataFrame()
    for i in range(int(len(data) / 6)):
        j = i * 6
        if j == 0:
            data11 = data.iloc[j:j + 6, :]
        else:
            data2 = data.iloc[j:j + 6, 1:]
            data2.index = [0,1,2,3,4,5]
            data11 = pd.concat([data11, data2], axis=1)
    data11.to_csv('./data/综合数据.csv', header=False, index=False)
    #交通运输与港口
    data = pd.read_csv('./data/交通运输与港口.csv', header=None)
    data111=pd.DataFrame()
    for i in range(int(len(data) / 2)):
        j = i * 2
        if j == 0:
            data111 = data.iloc[j:j + 2, :]
        else:
            data2 = data.iloc[j:j + 2, 1:]
            data2.index = [0, 1]
            data111 = pd.concat([data111, data2], axis=1)
    data111.to_csv('./data/交通运输与港口.csv', header=False, index=False)

if __name__ == '__main__':
    url = {'工业':'http://tjj.ningbo.gov.cn/col/col1229042830/index.html',
           '综合数据':'http://tjj.ningbo.gov.cn/col/col1229042827/index.html',
           '交通运输与港口':'http://tjj.ningbo.gov.cn/col/col1229042834/index.html'
           }
    for i,j in zip(url.keys(),url.values()):
        content = data_get(j)
        XPath(i,content)
    tocsv()

