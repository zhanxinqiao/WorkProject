#!/usr/bin/python3
#coding:utf-8
from selenium import webdriver
# ch_options = webdriver.ChromeOptions()
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

ch_options = Options()
#为Chrome配置无头模式
ch_options.add_argument("--headless")
ch_options.add_argument('--no-sandbox')
ch_options.add_argument('--disable-gpu')
ch_options.add_argument('--disable-dev-shm-usage')
ch_options.add_argument("--remote-debugging-port=9222")

# 在启动浏览器时加入配置

# dr = webdriver.Chrome(options=ch_options,executable_path=r"./chromedriver")
s = Service(r"./chromedriver")
dr = webdriver.Chrome(options=ch_options,service=s)
#这是测试网站
url = "https://www.baidu.com"
dr.get(url)
print(dr.title)
# dr.close()
