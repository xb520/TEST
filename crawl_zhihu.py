import requests
import time
from lxml import etree
def auto_login():
    url = "https://www.zhihu.com/signup?next=%2F"
    hearders_base = {
        'Host': 'www.zhihu.com',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        # 'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }
    cookies = {
        'q_c1': '4f460c63827e4a33ae1263b9718dc6cd|1520332184000|1520332184000',
        '_zap': '5812f606-1ee2-450a-9dfd-19938ffd0b14',
        '__DAYU_PP': 'FF3YNJ66nbJMii7eie3v2962c24d61ed',
        '_xsrf': '483a950e-1945-4a54-8472-529faf4d50b8',
        'd_c0': 'AGBvmiPcWQ2PTno6dnONRNgdFH69jGrX7fA=|1522148696',
        'l_cap_id': 'ZmJkMDU4YjVhM2U3NDFhZjkxY2I4YzZjYjU4ZmFmY2Y=|1522150238|7f21c134443704db10205c1114f559f69158c56b',
        'r_cap_id': 'OWUzZGRhMzZhNGM2NDU0ZThjY2QzNDI1MmJiMGZlYTM=|1522150238|6b872f2271ac719c713f3d1bae0464d05711a548',
        'cap_id': 'NmZlNjJmOTVhMmRmNGYyZjllN2U1NmFlNDA0ODliYmU=|1522150238|1ae72670bda06ebc76b6dcbe919b8676b0db2844',
        'capsion_ticket': '2|1:0|10:1522152953|14:capsion_ticket|44:ZmQyOGFjNTBhMzZlNDEyOGExYmY1ZjE0OGEyZjc1NGM=|fdda2cd98eba582eb9a6e9be3cdf0e33c1a971dbbad1d3d814018dce6f4c692b',
        'z_c0': '2|1:0|10:1522152965|4:z_c0|92:Mi4xMFZHOUFBQUFBQUFBWUctYUk5eFpEU1lBQUFCZ0FsVk5CWVNuV3dBMXBtaFBpc21hVzk4Zk1FLUJLVWlpM1FpYkF3|69673393ee5d0cd7d4ab6772927bbf9cf9ec7d14973638061acefe42143797b7',
    }
    url2 = "https://www.zhihu.com/api/v3/feed/topstory?action_feed=True&limit=7&session_token=d23fc5358de5396ab56f181867b8c48d&action=down&after_id=20&desktop=true"
    s = requests.session()
    response = s.get(url=url2, headers=hearders_base)


    for k,v in cookies.items():
        s.cookies[k] = v

    print(response.text)
    # print(s.cookies)

    # # print(response.content)
    # response = s.get(url = "https://www.zhihu.com/",headers = hearders_base)
    # html = etree.HTML(response.text)
    # data = html.xpath('//div[@itemprop="zhihu:question"]/a/text()')
    # print(data)
    # # print(response.text)
    # # with open('zhihu.html',"w",encoding='utf-8') as f:
    # #     f.write(response.text)
    print("\u672a\u8bbe\u7f6e\u9a8c\u8bc1\u65b9\u5f0f")


if __name__ == '__main__':
    auto_login()
