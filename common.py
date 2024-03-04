# coding=utf-8
# Author: HSJ
# 2024/3/4 10:41
# 公共文件(类库)
import os
from datetime import datetime
import requests
from config import *
from fake_useragent import UserAgent
import csv

class File:

    @classmethod
    def mkdatepath(cls):
        """
        创建日期的路径 2024/03/04
        :return:
        """
        now_path = datetime.now().strftime('/%Y/%m/%d/')
        return now_path

    @classmethod
    def mkdatename(cls):
        """
        创建日期的名字: 20240304
        :return:
        """
        now_path = datetime.now().strftime('%Y%m%d')
        return now_path

    @classmethod
    def data2txt(cls, data, save_path):
        """
        存储数据的方法
        :param data: 字符串
        :param save_path: 保存的路径
        :return:
        """
        # 判断路径是否存在
        dir_name = os.path.dirname(save_path)
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        with open(save_path, mode='a+') as f:
            f.write(data+'\n')


    @classmethod
    def txt2list(cls, path):
        """
        文本的内容，每一行一个元素， 转换成列表
        :param path:
        :return:
        """
        if not os.path.exists(path):
            return False
        dict_path = []
        with open(path, mode='r', encoding='utf-8') as f:
            for d in f:
                dict_path.append(d.rstrip("\n"))
        del dict_path[0]
        return dict_path

    @classmethod
    def data2csv_list(cls, header, data, save_path):
        """
        将数据存储到CSV的方法
        :param header: 表头
        :param data: 数据列表: 列表里面的元素也是列表
        :param save_path: 保存的路径
        :return:
        """
        # 判断路径是否存在, 不存在就创建
        dir_name = os.path.dirname(save_path)
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        with open(save_path, mode='a+', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(data)

    @classmethod
    def data2csv_dict(cls, header, data, save_path):
        """
        将数据存储到CSV的方法
        :param header: 表头
        :param data: 数据列表: 列表里面的元素是字典
        :param save_path: 保存的路径
        :return:
        """
        # 判断路径是否存在, 不存在就创建
        dir_name = os.path.dirname(save_path)
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        with open(save_path, mode='a+', newline='') as f:
            writer = csv.DictWriter(f, header)
            writer.writeheader()
            writer.writerows(data)

    @classmethod
    def csv2data(cls, data_path):
        """
        读取csv文件的方法
        :param data_path: 文件路径
        :return: 包含字典的列表
        """
        data = []
        if not os.path.exists(data_path):
            return data
        if not os.path.isfile(data_path):
            return data
        with open(data_path, mode='r', encoding='GBK') as f:
            reader = csv.DictReader(f)
            for row in reader:
               data.append(row)
        return data

class DoRequest:
    """
    发起请求的类
    """

    @classmethod
    def do_get(cls, url, params=None, headers=None, timeout=timeout):
        """
        发起get请求的方法
        :param url:
        :param params:
        :param headers:
        :param timeout:
        :return:
        """
        try:
            # 处理headers
            if headers is None:
                headers = {}
            # 判断headers里面是否有：User-Agent
            if 'User-Agent' not in headers.keys():
                # 随机ua
                ua = UserAgent()
                headers['User-Agent'] = ua.random
            res = requests.get(url=url, params=params, headers=headers, timeout=timeout)
            # 通常来说都是需要状态码和响应体，同时返回状态码和响应体，放在字典里面
            # 但是如果请求失败，那么就仅仅返回状态码
            if res.status_code == 200:
                return {
                    'status': res.status_code,
                    'content': res.content.decode('utf-8')
                }
            else:
                return {
                    'status': res.status_code,
                }
        except Exception as e:
            return {
                'status': 1000,
            }

    @classmethod
    def do_post(cls, url, params=None, headers=None, timeout=timeout):
        """
        发起post请求的方法
        :param url:
        :param params:
        :param headers:
        :param timeout:
        :return:
        """
        try:
            # 处理headers
            if headers is None:
                headers = {}
            # 判断headers里面是否有：User-Agent
            if 'User-Agent' not in headers.keys():
                # 随机ua
                ua = UserAgent()
                headers['User-Agent'] = ua.random
            res = requests.post(url=url, data=params, headers=headers, timeout=timeout)
            # 通常来说都是需要状态码和响应体，同时返回状态码和响应体，放在字典里面
            # 但是如果请求失败，那么就仅仅返回状态码
            if res.status_code == 200:
                return {
                    'status': res.status_code,
                    'content': res.content.decode('utf-8')
                }
            else:
                return {
                    'status': res.status_code,
                }
        except Exception as e:
            return {
                'status': 1000,
            }


