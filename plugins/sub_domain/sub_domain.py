# coding=utf-8
# Author: HSJ
# 2024/3/4 14:30
from bs4 import BeautifulSoup
import sys
import time
sys.path.append("../../")  # 由于common不在同一层，所以需要添加路径,才能找到对应的模块
from common import DoRequest
from common import File
from config import cache_base_path
class sub_domain:
    """
    找子域名有哪些方式？
    1.搜索引擎：百度，google, 网络空间搜索引擎：fofa, zoomeye, 鹰图
    2.layer子域名挖掘机
    3.在线网站： dns解析记录
    """
    def __init__(self):
        self.__domain = ''
        self.__domain_list = []



    def __get_sub_domain_crt(self):
        crt_url = 'https://crt.sh'
        # 发起请求
        params = {
            'q': self.__domain
        }
        res = DoRequest.do_get(url=crt_url, params=params)
        if res['status'] == 1000:
            print('被拦截了.......')
            time.sleep(20)
            self.__get_sub_domain_crt()
        if res['status'] == 200:
            content = res['content']
            #实例化beautifulsoup
            soup = BeautifulSoup(content, 'html.parser')
            tds = soup.find_all('td', attrs={'class': 'outer'})
            table = tds[1].find('table')
            trs = table.find_all('tr')
            del(trs[0])
            for tr in trs:
                td = tr.find_all('td')[4]
                domain = td.text
                self.__domain_list.append(domain)
            # 去重
            self.__domain_list = list(set(self.__domain_list))

    def __cache(self):
        """
        存储数据
        :return:
        """
        # save_path = ...sub_domain/wuyecao.net/20240304.txt/csv
        # 先获取日期的名字
        data_name = File.mkdatename()
        save_path = f"{cache_base_path}/sub_domain/{self.__domain}/{data_name}.txt"
        for d in self.__domain_list:
            File.data2txt(d, save_path)

    def start(self):
        domain = input("请输入域名:")
        self.__domain = domain
        # 获取子域名
        self.__get_sub_domain_crt()
        # 写文件： 写缓存的规则
        self.__cache()


