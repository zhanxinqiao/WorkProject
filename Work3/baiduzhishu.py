import requests
import json
from datetime import date, timedelta
import pandas as pd


class DownloadBaiDuIndex(object):
    def __init__(self, cookie):
        self.cookie = cookie
        self.headers = {
            "Connection": "keep-alive",
            "Accept": "application/json, text/plain, */*",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": "https://index.baidu.com/v2/main/index.html",
            "Accept-Language": "zh-CN,zh;q=0.9",
            'Cookie': self.cookie,
            "Host": "index.baidu.com",
            "X-Requested-With": "XMLHttpRequest",
            "Cipher-Text": "1656572408684_1656582701256_Nvm1pABkNsfD7V9VhZSzzFiFKylr3l5NR3YDrmHmH9yfFicm+Z9kmmwKVqVV6unvzAEh5hgXmgelP+OyOeaK8F21LyRVX1BDjxm+ezsglwoe1yfp6lEpuvu5Iggg1dz3PLF8e2II0e80ocXeU0jQFBhSbnB2wjhKl57JggTej12CzuL+h9eeVWdaMO4DSBWU2XX6PfbN8pv9+cdfFhVRHCzb0BJBU3iccoFczwNQUvzLn0nZsu0YPtG5DxDkGlRlZrCfKMtqKAe1tXQhg3+Oww4N3CQUM+6A/tKZA7jfRE6CGTFetC7QQyKlD7nxabkQ5CReAhFYAFAVYJ+sEqmY5pke8s3+RZ6jR7ASOih6Afl35EArbJzzLpnNPgrPCHoJiDUlECJveul7P5vvXl/O/Q==",

        }

    def decrypt(self, ptbk, index_data):
        n = len(ptbk) // 2
        a = dict(zip(ptbk[:n], ptbk[n:]))
        return "".join([a[s] for s in index_data])

    def get_index_data_json(self, keys, start=None, end=None):
        words = [[{"name": key, "wordType": 1}] for key in keys]
        words = str(words).replace(" ", "").replace("'", "\"")

        url = f'http://index.baidu.com/api/SearchApi/index?area=0&word={words}&area=0&startDate={start}&endDate={end}'
        print(words, start, end)
        res = requests.get(url, headers=self.headers)
        data = res.json()['data']
        uniqid = data['uniqid']
        url = f'http://index.baidu.com/Interface/ptbk?uniqid={uniqid}'
        res = requests.get(url, headers=self.headers)
        ptbk = res.json()['data']
        result = {}
        result["startDate"] = start
        result["endDate"] = end
        for userIndexe in data['userIndexes']:
            name = userIndexe['word'][0]['name']
            tmp = {}
            index_all = userIndexe['all']['data']
            index_all_data = [int(e) for e in self.decrypt(ptbk, index_all).split(",")]
            tmp["all"] = index_all_data
            index_pc = userIndexe['pc']['data']
            index_pc_data = [int(e) for e in self.decrypt(ptbk, index_pc).split(",")]
            tmp["pc"] = index_pc_data
            index_wise = userIndexe['wise']['data']
            index_wise_data = [int(e)
                               for e in self.decrypt(ptbk, index_wise).split(",")]
            tmp["wise"] = index_wise_data
            result[name] = tmp
        return result

    def GetIndex(self, keys, start=None, end=None):
        today = date.today()
        if start is None:
            start = str(today - timedelta(days=8))
        if end is None:
            end = str(today - timedelta(days=2))

        try:
            raw_data = self.get_index_data_json(keys=keys, start=start, end=end)
            raw_data = pd.DataFrame(raw_data[keys[0]])
            raw_data.index = pd.date_range(start=start, end=end)

        except Exception as e:
            print(e)
            raw_data = pd.DataFrame({'all': [], 'pc': [], 'wise': []})

        finally:
            return raw_data


cookie = 'ariaDefaultTheme=default; ariaFixed=true; ariaReadtype=1; ariaoldFixedStatus=false; ariaStatus=false; BDUSS=kFwNG9uOEJUakpKSVBNY0ZEZmlEbkhkS0xiTHloRTN3NnM3MzdGSjJuNGZzYjVpRVFBQUFBJCQAAAAAAAAAAAEAAAA2hFTQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAB8kl2IfJJdie; Hm_lvt_246a5e7d3670cfba258184e42d902b31=1663559009; Hm_up_d101ea4d2a5c67dab98251f0b5de24dc=%7B%22uid_%22%3A%7B%22value%22%3A%223495199798%22%2C%22scope%22%3A1%7D%7D; ZD_ENTRY=bing; BAIDUID=9786531971661D417944BC7EE0C44274:FG=1; Hm_lvt_d101ea4d2a5c67dab98251f0b5de24dc=1666056507,1666168424; bdindexid=ni89kscva0oko0f26kr2oobdl7; SIGNIN_UC=70a2711cf1d3d9b1a82d2f87d633bd8a041618087337jxTMgtJU0TsYvMy3IpPpVbfkCPGRPzZixVVn84eD1bcypKINVtwUKC36KUkxDSy8PiEF567yXfhbY7AGlJiT1Xk2TKzppOGcLKNdFB3BhjJAenBc%2Fy9ACZ4UDK7Ns3m3ElOGVdZrNIzml92f%2B1SNsz4g7EHy5hu%2FSlq6WQBAew%2FA4OCGdzQeHFYR7lxwN3JMU4M%2BkAoSNMXO5etKspTRAFled6jltEHgZQR50MdC9qY5g9xIRo5IcKsTbvoYC%2BvUNIUhzt43CApIEtVFnqJ9LiFZllYVU%2BBtpL2MZNiccE%3D75550403353425188441679776028556; __cas__rn__=416180873; __cas__st__212=03ac792ee694e52d7f3b1ec8f10df21d12f087c8280aa727d0a15c86ac4829bd3cc8bd4f058ca5e9f3cbcf58; __cas__id__212=43088718; CPID_212=43088718; CPTK_212=1403913403; RT="z=1&dm=baidu.com&si=3892c7c0-8350-4f88-b07c-e0f17004947b&ss=l9fdnpvv&sl=b&tt=ewi&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf"; Hm_lpvt_d101ea4d2a5c67dab98251f0b5de24dc=1666172377'

# 初始化一个类
downloadbaiduindex = DownloadBaiDuIndex(cookie=cookie)

data = downloadbaiduindex.GetIndex(keys=['python'], start='2021-01-01', end='2021-11-12')

print(data)
