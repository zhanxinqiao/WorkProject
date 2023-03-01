import requests
from lxml import etree
import demjson


class Login:
    def __init__(self):
        # 输入用户名和密码
        self.username = "+86"+"17671057127"
        self.password = "adgfgfhhhfgs"

    def get_index_csrf_and_cookie(self):
        session = requests.Session()
        url = "https://www.linkedin.com/"
        querystring = {"trk": "brandpage_baidu_pc-mainlink"}
        headers = {
            'authority': "www.linkedin.com",
            'cache-control': "max-age=0",
            'upgrade-insecure-requests': "1",
            'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36",
            'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            'referer': "https://www.baidu.com/s?ie=UTF-8&wd=%E9%A2%86%E8%8B%B1",
           'accept-encoding': "gzip, deflate, br",
            'accept-language': "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        }
        response = session.request("GET", url, headers=headers, params=querystring)
        cookie = ""
        csrf_token = ""
        for c in session.cookies:
            if c.name in "JSESSIONID":
                csrf_token = c.value
            cookie = cookie + c.name + "=" + c.value + "; "
        html = etree.HTML(response.text)
        # html = etree.HTML(response.read()).decode('utf‐8')
        # print(html)
        csrf = html.xpath('//input[@name="loginCsrfParam"]/@value')[0]
        index_login_data = {
            "cookie": cookie,
            "csrf": csrf,
            "csrf_token": csrf_token
        }
        with open("cookie.json", "w") as f:
            f.write(str(index_login_data))

    def login(self):
        with open("cookie.json", "r") as f:
            index_cookie = f.read()
        json_cookie = demjson.decode(index_cookie)
        csrf = json_cookie.get("csrf")
        cookie = json_cookie.get("cookie")

        s = requests.session()

        url = "https://www.linkedin.com/uas/login-submit"

        querystring = {"loginSubmitSource": "GUEST_HOME"}

        payload = "session_key={0}&session_password={1}&isJsEnabled=false&loginCsrfParam={2}&fp_data=default&undefined=".format(
            self.username, self.password, csrf)
        headers = {
            'authority': "www.linkedin.com",
            'cache-control': "max-age=0,no-cache",
            'origin': "https://www.linkedin.com",
            'upgrade-insecure-requests': "1",
            'content-type': "application/x-www-form-urlencoded",
            'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36",
            'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            'referer': "https://www.linkedin.com/",
            'accept-encoding': "gzip, deflate, br",
            'accept-language': "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            'cookie': cookie
        }

        s.request("POST", url, data=payload, headers=headers, params=querystring)

        cookie = ""
        csrf_token = ""
        for c in s.cookies:
            if c.name == "JSESSIONID":
                csrf_token = c.value
            cookie = cookie + c.name + "=" + c.value + "; "

        cookie_data = {
            "cookie": cookie,
            "csrf_token": csrf_token
        }
        with open("cookie.json", "w") as f:
            f.write(str(cookie_data))

    def test_login(self):
        with open("cookie.json", "r") as f:
            cookie_text = f.read()
        json_cookie = demjson.decode(cookie_text)
        csrf_token = json_cookie['csrf_token']
        cookie = json_cookie['cookie']

        headers1 = {
            'x-li-track': '{"clientVersion":"1.2.7373","osName":"web","timezoneOffset":8,"deviceFormFactor":"DESKTOP","mpName":"voyager-web"}',
            'cookie': cookie,

            'accept-encoding': "gzip, deflate, br",
            'x-li-lang': "zh_CN",
            'accept-language': "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36",
            'x-li-page-instance': "urn:li:page:d_flagship3_feed;LvtQ1iY2QeGSOhIoA8jaQQ==",
            'accept': "application/vnd.linkedin.normalized+json+2.1",
            'csrf-token': csrf_token.replace('"', ""),
            'x-restli-protocol-version': "2.0.0",
            'authority': "www.linkedin.com",
            'referer': "https://www.linkedin.com/feed/",
            'cache-control': "no-cache",
        }

        url = "https://www.linkedin.com/feed/"

        response = requests.request("GET", url, headers=headers1)
        response.encoding = "utf-8"
        print(response.text)
        # u = "https://www.linkedin.com/voyager/api/onboarding/launchpadCard"
        # querystring = {"context": "FEED", "q": "context"}
        # r = requests.get(u, headers=headers1, params=querystring)
        # print(r.text)


if __name__ == "__main__":
    login = Login()
    login.get_index_csrf_and_cookie()
    login.login()
    with open("cookie.json", "r") as f:
        session = f.read()
        se = demjson.decode(session)
    print(se.get("csrf_token"))

    with open("cookie.json", "r") as f:
        cookie = f.read()
        json_cookie = demjson.decode(cookie)
    print(json_cookie['cookie'])

    login.test_login()