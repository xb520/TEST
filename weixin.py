import requests
import re
import json
import html
import time




# 爬取文章

def crawl():

    url = "https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=MjM5MDQ4MzU5NQ==&scene=124&devicetype=android-24&version=26060533&lang=zh_CN&nettype=WIFI&a8scene=3&pass_ticket=JWwsKLW87oJCEs1RxNMJLjdQLVOt0Txlh%2BFKAQWPiTDupmJvENgmAe3CRfqQc8LW&wx_header=1"
    hearders = {
        'Host': 'mp.weixin.qq.com',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 7.0; MI 5s Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/043909 Mobile Safari/537.36 MicroMessenger/6.6.5.1280(0x26060533) NetType/WIFI Language/zh_CN',
        'x-wechat-key': 'cc8a902ad2445ef58b9c3d25b99fdcbc81bae3abc394d6deb2e252519a847ad004249a5d219457254fbb5fb66bfe53647c5def8686fb715578ff2a956db2526bc223028e8802a5da034c85fee386a0c4',
        'x-wechat-uin': 'MTY0NzUzODU2MQ%3D%3D',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,image/wxpic,image/sharpp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,en-US;q=0.8',
        'Cookie': 'sd_userid=89911512988871597; sd_cookie_crttime=1512988871597; tvfe_boss_uuid=423ad3b23a3d7d62; pgv_pvid=4694704320; rewardsn=; wxtokenkey=777; wxuin=1647538561; devicetype=android-24; version=26060533; lang=zh_CN; pass_ticket=JWwsKLW87oJCEs1RxNMJLjdQLVOt0Txlh+FKAQWPiTDupmJvENgmAe3CRfqQc8LW; wap_sid2=CIHjzZEGElxEU3RSSjNFSkEtb3JmSExhTWxxT0FlQThnYi1NaUlUOG1jcGE0QVhnVlNrcmZzWUx4WWY2SE1oejlJZVYyQUxlREIxOFpsUDlod0diZWRZbHNnVTVJYlVEQUFBfjCWvefVBTgNQJVO',
        'Q-UA2': 'QV=3&PL=ADR&PR=WX&PP=com.tencent.mm&PPVN=6.6.5&TBSVC=43603&CO=BK&COVC=043909&PB=GE&VE=GA&DE=PHONE&CHID=0&LCID=9422&MO= MI5s &RL=1080*1920&OS=7.0&API=24',
        'Q-GUID': '08c26776e4c9e02bbcdfd5c611ab88cb',
        'Q-Auth': '31045b957cf33acf31e40be2f3e71c5217597676a9729f1b',
    }
    # requests.packages.urllib3.disable_warnings()
    response = requests.get(url=url,headers=hearders,verify = False)
    print(response.text)
    data = find_data(response.text)
    for item in data:
        print(item)

    # with open("kejimeixue.html",'w',encoding='utf-8') as f:
    #     f.write(response.text)
    # print(response.text)

    # print("ok")
# 正则抓取数据


def find_data(html_content):
    patterns = re.compile("msgList = '({.*?})'", flags=re.S)
    match = patterns.search(html_content)
    if match:
        data = match.group(1)
        data = html.unescape(data)
        data = json.loads(data)
        articles = data.get("list")
        for item in articles:
            print(item)
        return articles

# html_content = 'kejimeixue.html'
# html_content = crawl()
# find_data(html_content)
crawl()


