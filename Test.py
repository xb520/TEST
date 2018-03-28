import requests
from lxml import etree
# url_str = 'https://cn.bing.com'
# response = requests.get(url=url_str)
# print(response.status_code)
# # print(response.text)
# print(response.headers)

print("\u767b\u5f55\u6210\u529f")


headers_base = {
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'
}
url_str = 'http://ershou.gandianli.com/'
response = requests.get(url=url_str, headers=headers_base)
print(response.status_code)

html = etree.HTML(response.text)
browse_time_list = html.xpath("//div[@class = 'goods_waper f_l g-clearfix']//div[@class='f_r']/text()")
browse_time_list = [one[2:-1] for one in browse_time_list]
print(browse_time_list)