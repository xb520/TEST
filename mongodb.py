from datetime import datetime

from mongoengine import DateTimeField
from mongoengine import Document
from mongoengine import IntField
from mongoengine import StringField
from mongoengine import URLField
from mongoengine import connect
import html
import logging
import json



# 连接 mongodb
connect('weixin3', host='localhost', port=27017)


class Post(Document):
    """
    文章信息
    """
    title = StringField()  # 文章标题
    content_url = StringField()  # 文章链接
    content = StringField()  # 文章内容
    source_url = StringField()  # 原文链接
    digest = StringField()  # 文章摘要
    cover = URLField(validation=None)  # 封面图
    p_date = DateTimeField()  # 推送时间

    read_num = IntField(default=0)  # 阅读数
    like_num = IntField(default=0)  # 点赞数
    comment_num = IntField(default=0)  # 评论数
    reward_num = IntField(default=0)  # 赞赏数
    author = StringField()  # 作者

    c_date = DateTimeField(default=datetime.now)  # 数据生成时间
    u_date = DateTimeField(default=datetime.now)  # 最后更新时间...

    import html
    def sub_dict(d, keys):
        return {k: html.unescape(d[k]) for k in d if k in keys}

    d = {"a": "1", "b": 2, "c": 3}
    sub_dict(d, ["a", "b"])  # {"a":"1", "b": "2"}

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
                multi_msg_info = msg_info.get("multi_app_msg_item_list")  # 多图文推送，把第二条第三条也保存
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

