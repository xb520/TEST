import logging
# import utils
import requests
import time
import html
from model import Post
from datetime import datetime
import json
import utils

logging.basicConfig(level=logging.INFO)
requests.packages.urllib3.disable_warnings()

logger = logging.getLogger(__name__)



class WeiXinCrawler:

    def crawl(self,offset=0):
        """
        爬取更多文章

        """

        # url = "https://mp.weixin.qq.com/mp/profile_ext?action=getmsg&__biz=MjM5MDQ4MzU5NQ==&f=json&offset={offset}&count=10&is_ok=1&scene=124&uin=777&key=777&pass_ticket=p7LkGA%2FEVGnRySKVksMK0UjsFNhWtirCr5IqxnTPiXRLBkWBDV6RrRxfHcvXn9mJ&wxtoken=&appmsg_token=949_OkA5HnJUNZe9Dsn3cma2Mowwwh7fPHdtFRxztA~~&x5=1&f=json".format(offset=offset)
        url ="https://mp.weixin.qq.com/mp/profile_ext?action=getmsg&__biz=MjM5MDQ4MzU5NQ==&f=json&offset={offset}&count=10&is_ok=1&scene=124&uin=777&key=777&pass_ticket=JWwsKLW87oJCEs1RxNMJLjdQLVOt0Txlh%2BFKAQWPiTDupmJvENgmAe3CRfqQc8LW&wxtoken=&appmsg_token=949_2MNs5LaTCWGQaTBLDx2ydzhg9F-Fm2BCYxJ-QA~~&x5=1&f=json" .format(offset=offset)
        print(url)
        headers = {
            'Host': 'mp.weixin.qq.com',
            'Connection': 'keep-alive',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 7.0; MI 5s Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/043909 Mobile Safari/537.36 MicroMessenger/6.6.5.1280(0x26060533) NetType/WIFI Language/zh_CN',
            'Accept': '*/*',
            'Referer': 'https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=MjM5MDQ4MzU5NQ==&scene=124&devicetype=android-24&version=26060533&lang=zh_CN&nettype=WIFI&a8scene=3&pass_ticket=JWwsKLW87oJCEs1RxNMJLjdQLVOt0Txlh%2BFKAQWPiTDupmJvENgmAe3CRfqQc8LW&wx_header=1',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,en-US;q=0.8',
            'Cookie': 'sd_userid=89911512988871597; sd_cookie_crttime=1512988871597; tvfe_boss_uuid=423ad3b23a3d7d62; pgv_pvid=4694704320; rewardsn=; wxtokenkey=777; wxuin=1647538561; devicetype=android-24; version=26060533; lang=zh_CN; pass_ticket=JWwsKLW87oJCEs1RxNMJLjdQLVOt0Txlh+FKAQWPiTDupmJvENgmAe3CRfqQc8LW; wap_sid2=CIHjzZEGElxEU3RSSjNFSkEtb3JmSExhTWxxT0FlQThnYi1NaUlUOG1jcGE0QVhnVlNrcmZzWUx4WWY2SE1oejlJZVYyQUxlREIxOFpsUDlod0diZWRZbHNnVTVJYlVEQUFBfjCWvefVBTgNQJVO',
            'Q-UA2': 'QV=3&PL=ADR&PR=WX&PP=com.tencent.mm&PPVN=6.6.5&TBSVC=43603&CO=BK&COVC=043909&PB=GE&VE=GA&DE=PHONE&CHID=0&LCID=9422&MO= MI5s &RL=1080*1920&OS=7.0&API=24',
            'Q-GUID': '08c26776e4c9e02bbcdfd5c611ab88cb',
            'Q-Auth': '31045b957cf33acf31e40be2f3e71c5217597676a9729f1b',
        }


        response = requests.get(url=url, headers=headers, verify=False)
        result = response.json()
        if result.get("ret") == 0:
            msg_list = result.get("general_msg_list")
            logger.info("抓取数据：offset=%s, data=%s" % (offset, msg_list))
            # 递归调用
            self.save(msg_list)
            has_next = result.get("can_msg_continue")
            if has_next == 1:
                next_offset = result.get("next_offset")
                # print(next_offset)

                print(next_offset)
                time.sleep(2)
                self.crawl(next_offset)


        else:
            # 错误消息
            # {"ret":-3,"errmsg":"no session","cookie_count":1}
            logger.error("无法正确获取内容，请重新从Fiddler获取请求参数和请求头")
            exit()

    # import html
    # def sub_dict(d, keys):
    #     return {k: html.unescape(d[k]) for k in d if k in keys}
    #
    # d = {"a": "1", "b": 2, "c": 3}
    # sub_dict(d, ["a", "b"])  # {"a":"1", "b": "2"}

    @staticmethod
    def save(msg_list):

        msg_list = msg_list.replace("\/", "/")
        data = json.loads(msg_list)
        msg_list = data.get("list")
        for msg in msg_list:
            p_date = msg.get("comm_msg_info").get("datetime")
            msg_info = msg.get("app_msg_ext_info")  # 非图文消息没有此字段
            if msg_info:
                WeiXinCrawler._insert(msg_info, p_date)
                multi_msg_info = msg_info.get("multi_app_msg_item_list")
                for msg_item in multi_msg_info:
                    WeiXinCrawler._insert(msg_item, p_date)
            else:
                logger.warning(u"此消息不是图文推送，data=%s" % json.dumps(msg.get("comm_msg_info")))

    @staticmethod
    def _insert(item, p_date):
        keys = ('title', 'author', 'content_url', 'digest', 'cover', 'source_url')
        sub_data = utils.sub_dict(item, keys)
        post = Post(**sub_data)
        p_date = datetime.fromtimestamp(p_date)
        post["p_date"] = p_date
        logger.info('save data %s ' % post.title)
        try:
            post.save()
        except Exception as e:
            logger.error("保存失败 data=%s" % post.to_json(), exc_info=True)





if __name__ == '__main__':
    crawler = WeiXinCrawler()
    crawler.crawl()