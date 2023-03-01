# -*-coding:utf-8-*-
from flask import Flask, request, Response, abort, render_template, jsonify
from flask_cors import CORS
# from ast import literal_eval
import sys
import json
import traceback
from gevent import pywsgi
import random
import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.action_chains import ActionChains
import random
import requests
import re
from lxml import etree

def random_sleep(mu=4, sigma=1):
    '''正态分布随机睡眠

    :param mu: 平均值

    :param sigma: 标准差，决定波动范围

    '''
    # a = time.time()
    secs = random.normalvariate(mu, sigma)

    if secs <= 0:

        secs = mu  # 太小则重置为平均值

    time.sleep(secs)
# 打开网络，登录，获取driver


def get_driver(url):
    options = Options()
#     options.headless = True
    # 此步骤很重要，设置为开发者模式，防止被各大网站识别出来使用了Selenium
    # options.add_experimental_option('excludeSwitches', ['enable-logging']) #禁止打印日志
    options.add_experimental_option(
        'excludeSwitches', ['enable-automation'])  # 跟上面只能选一个
#     options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})  # 不加载图片,加快访问速度
    # options.add_argument('--incognito')  # 无痕隐身模式
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--headless')
    options.add_argument("disable-cache")  # 禁用缓存
    options.add_argument('disable-infobars')  # 禁用“chrome正受到自动测试软件的控制”提示
    # INFO = 0 WARNING = 1 LOG_ERROR = 2 LOG_FATAL = 3 default is 0
    options.add_argument('log-level=3')
    options.add_argument("--headless")  # 无头模式--静默运行
    # options.add_argument("--window-size=1920,1080")  # 使用无头模式，需设置初始窗口大小
    options.add_argument("--test-type")
    # 与上面一条合并使用；忽略 Chrome 浏览器证书错误报警提示
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--disable-gpu")  # 禁用GPU加速
    options.add_argument("--no-first-run")  # 不打开首页
    options.add_argument("--no-default-browser-check")  # 不检查默认浏览器
    options.add_argument('--start-maximized')  # 最大化
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument(
        'User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36')
    options.add_argument("--remote-debugging-port=9222")
    # 这里需要修改 改为 driver 具体的位置
    # driver_path = r"./chromedriver"
    s = Service(r"./chromedriver")
    # driver_path = r"./usr/bin/chromedriver"
#     driver = webdriver.Chrome(executable_path=driver_path, options=options)
#     driver = webdriver.Chrome(options=options, executable_path=driver_path)
    driver = webdriver.Chrome(options=options,service=s)
    # driver = webdriver.Chrome()
    driver.get(url)
    return driver


def judge_if_register(number):
    url = "https://www.linkedin.cn/incareer/home"
    driver = get_driver(url)
    driver.find_element_by_xpath(
        "//input[@name='session_key']").send_keys(number)
    # random_sleep(1, 1)
    driver.find_element_by_xpath(
        "//input[@name='session_password']").send_keys("abcd123456")
    # random_sleep(1, 1)
    driver.find_element_by_xpath("//button[@class='login-button']").click()
    # time.sleep(1)
    ss=driver.find_element_by_xpath("//div[@class='form__input--floating mt-24']//div[@id='error-for-password']").text
    if "抱歉，密码不正确" in ss:
        code = "Yes"
    else:
        code = "No"
    # else:
    #     code = "OTHER PROBLEMS"
    # driver.get(url=url)
    # driver.close()
    driver.stop_client()
    driver.close()
    driver.quit()
    return number+"----"+code+","


# if __name__ == '__main__':
#     print(judge_if_register("+8618382643421"))
app = Flask(__name__)
CORS(app)  # 允许所有路由上所有域使用CORS


@app.route("/", methods=['POST', 'GET'])
def inedx():
    return '领英账号检测程序正在运行中'


@app.route("/linkedin_check", methods=['POST', 'GET'])
def get_result():
    if request.method == 'POST':
        text = request.form.get('text')
    else:
        text = request.args['text']
    try:
        print("输入参数", text)
        arg = text.split(',')
        num = (len(arg))
        # 传过来的号码切分之后遍历，每个检测逻辑写在下面的for循环里
        res = []
        for i in range(num):
            # 状态值
            state = judge_if_register(arg[i])
            res.append(state)
        result = {"code": "200", "msg": "响应成功", "data": res}
    except Exception as e:
        print(e)
        result_error = {'errcode': -1}
        result = json.dumps(result_error, indent=4, ensure_ascii=False)
        # 这里用于捕获更详细的异常信息
        exc_type, exc_value, exc_traceback = sys.exc_info()
        lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
        # 提前退出请求
        abort(Response("Failed!\n" + '\n\r\n'.join('' + line for line in lines)))
    return Response(str(result), mimetype='application/json')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=1316, threaded=False)
    # server = pywsgi.WSGIServer(('0.0.0.0', 1315), app)
    # server.serve_forever()
