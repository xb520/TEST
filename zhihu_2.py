import requests
import http.cookiejar
import time

s = requests.session()

s.cookies = http.cookiejar.LWPCookieJar(filename="cookies.txt")
try:
    s.cookies.load(ignore_discard=True)
except:

    print("cookies未能加载")



headers = {
        'Host': 'www.zhihu.com',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        # 'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }
# 获取验证码
def captcha(captcha_data):
    with open("captcha.jpg","wb")as f:
        f.write(captcha_data)
    text = input("请输入验证码：")
    return text
# 获取cookies 后获取首页
def get_index():

    response = s.get(url='https://www.zhihu.com/',headers =headers )
    with open('cook_zhihu.html','w',encoding='utf-8') as f:
        f.write(response.text)
    print('ok')

def crawlzhihu(number,password):
    while True:
        try:
            url = 'https://www.zhihu.com/signup?next=%2F'
            response = s.get(url=url,headers=headers)
            dic = {}
            for i,j in response.cookies.items():
                dic[i] = j
            # print(dic)
            for k in dic:
                if k == "_xsrf":
                    print(type(dic[k]))
                    _xsrf = dic[k]

            print("手机号码登录")
            post_url= "https://www.zhihu.com/login/phone_num"
            # 验证码地址
            captcha_url = "https://www.zhihu.com/captcha.gif?r=%d&type=login" % (time.time() * 1000)

            captcha_data = s.get(captcha_url, headers=headers).content
            text = captcha(captcha_data)
            post_data = {
                "_xsrf":_xsrf,
                "phone_num":number,
                "password":password,
                "captcha": text
                }

            response_text = s.post(url=post_url,data=post_data,headers=headers)
            print(response_text.text.encode('utf-8'))
            get_response = s.get(url='https://www.zhihu.com/', headers=headers)

            print(get_response.text)
            # print(captcha_url)
            s.cookies.save()
            break
        except:
            time.sleep(5)

if __name__ == '__main__':
    # 输入手机号码,密码登录知乎
    crawlzhihu('phone','password')
    # 获取去cookies后可以使用cookies直接登录
    # get_index()
