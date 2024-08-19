

import requests
from lxml import html

url = "https://tuoitre.vn//tin-tuc-gia-xe-nhieu-o-to-ban-cham-giam-gia-thang-co-hon-20240811125825489.htm"
response = requests.get(url)
response.encoding = "utf-8"
response = html.fromstring(response.content)

result = ""
list_ele = response.xpath("//*[@class = 'detail__cmain']/*[@class = 'detail-title article-title']")
for ele in list_ele:
    temp = ' '.join(ele.itertext()) # trich xuat text cua phan tu
    result += temp + "\n"
print(result.strip())


