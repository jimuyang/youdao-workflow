#!/usr/local/bin/python3

import requests
from urllib.parse import quote, unquote
from string import Template
from urllib import request
from http import cookiejar
import time
import hashlib
import json
import sys

url = "http://fanyi.youdao.com/translate_o"


def get_cookie(url):
    # 声明一个CookieJar对象实例来保存cookie
    cookieJar = cookiejar.CookieJar()
    # 利用urllib.request库的HTTPCookieProcessor对象来创建cookie处理器,也就CookieHandler
    handler = request.HTTPCookieProcessor(cookieJar)
    # 通过CookieHandler创建opener
    opener = request.build_opener(handler)
    # 此处的open方法打开网页
    response = opener.open(url)
    # 打印cookie信息
    cookie = ""
    for item in cookieJar:
        tem = Template("${name}=${value};")
        cookie += tem.substitute(name=item.name, value=item.value)
    # print(cookie)
    return cookie


def md5(source):
    m = hashlib.md5()
    b = source.encode(encoding='utf-8')
    m.update(b)
    return m.hexdigest()


def translate_by_youdao(needTrans):
    # var r = function(e) {
    #     var t = n.md5(navigator.appVersion)
    #       , r = "" + (new Date).getTime()
    #       , i = r + parseInt(10 * Math.random(), 10);
    #     return {
    #         ts: r,
    #         bv: t,
    #         salt: i,
    #         sign: n.md5("fanyideskweb" + e + i + "n%A-rKaT5fb[Gy?;N5@Tj")
    #     }
    # };
    def get_salt(needTrans):
        # appVersion md5
        t = "9ed1df12e1ecacf0048d2b29195a0070"
        r = str(int(time.time() * 1000))
        i = r + "1"
        return (r, t, i, md5("fanyideskweb" + needTrans + i + "n%A-rKaT5fb[Gy?;N5@Tj"))

    cookie = get_cookie("http://fanyi.youdao.com")
    ts, bv, salt, sign = get_salt(needTrans)

    template = Template(
        "i=${needTrans}&from=AUTO&to=AUTO&smartresult=dict&client=fanyideskweb&salt=${salt}&sign=${sign}&ts=${ts}&bv=${bv}&doctype=json&version=2.1&keyfrom=fanyi.web&action=FY_BY_REALTlME")
    payload = template.substitute(needTrans=quote(
        needTrans, 'utf-8'), salt=salt, sign=sign, ts=ts, bv=bv)
    # print(payload)
    headers = {
        'Accept': "application/json, text/javascript, */*; q=0.01",
        'Origin': "http://fanyi.youdao.com",
        'X-Requested-With': "XMLHttpRequest",
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
        'Content-Type': "application/x-www-form-urlencoded",
        'Referer': "http://fanyi.youdao.com/",
        'Accept-Encoding': "gzip, deflate",
        'Accept-Language': "zh-CN,zh;q=0.9",
        'Cookie': cookie,
        'Cache-Control': "no-cache",
        'Host': "fanyi.youdao.com",
        'cache-control': "no-cache"
    }

    response = requests.request(
        "POST", url, data=payload.encode('utf-8'), headers=headers, params={"smartresult": ["dict", "rule"]})

    data = json.loads(response.text)
    result = []
    if ('translateResult' in data):
        result.append(data['translateResult'][0][0]['tgt'])
    if ('smartResult' in data):
        for o in data['smartResult']['entries']:
            if o.strip() != '':
                result.append(o.replace('\r\n', ''))
    return result


if __name__ == "__main__":
    print(translate_by_youdao(sys.argv[1]))
