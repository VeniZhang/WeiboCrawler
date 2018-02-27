#coding=utf-8
import json
import base64
import requests
import sys
import io
from configparser import ConfigParser

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

class WeiboCrawler():
    def __init__(self, file_="config.private"):
        with open(file_) as f:
           cfg = ConfigParser()
           cfg.read(file_)
           print(cfg.sections())
           self.account = cfg.get('account', 'account')
           self.passwd = cfg.get('account', 'passwd')
        self.cookie = ""
    
    def login(self):
        loginURL = r'https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.19)'
        username = base64.b64encode(self.account.encode('utf8'))
        postData = {
            "entry": "sso",
            "gateway": "1",
            "from": "null",
            "savestate": "30",
            "useticket": "0",
            "pagerefer": "",
            "vsnf": "1",
            "su": username,
            "service": "sso",
            "sp": self.passwd,
            "sr": "1440*900",
            "encoding": "UTF-8",
            "cdult": "3",
            "domain": "sina.com.cn",
            "prelt": "0",
            "returntype": "TEXT",
        }
        session = requests.Session()
        r = session.post(loginURL, data=postData)
        jsonStr = r.content.decode('utf8')
        info = json.loads(jsonStr)
        if info["retcode"] == "0":
            print("Get Cookie Success!( Account:%s )" % self.account)
            self.cookie = session.cookies.get_dict()
        else:
            print("Failed!( Reason:%s )" % info['reason'])
            self.cookie = None

if __name__ == "__main__":
    weibo = WeiboCrawler()
    cookie = weibo.login()
