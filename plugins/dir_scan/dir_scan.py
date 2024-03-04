# coding=utf-8
# Author: HSJ
# 2024/3/1 15:54
import requests
import queue
import sys
sys.path.append("../../")
from common import File
from config import dict_path
from config import cache_base_path
import os
import threading

# 进度条： 是个比例
# 怎么算这个比例？
# 队列有个长度： 总数  / 取一个就少一个
# 1 - (队列的剩余长度 / 总数)

class dir_scan:

    def __init__(self):
        # 扫描的网址
        self.__url = ""
        # 线程的数量
        self.__thread_count = 10
        # 字典的路径
        self.__dict_path = ""
        # 队列
        self.__queue = queue.Queue()
        # 字典内容
        self.__dict_list = []
        # 线程池
        self.__threads = []
        # 队列总长度
        self.__queue_length = 0
        # 结果列表
        self.__res = []

    @property
    def queue_length(self):
        return self.__queue_length

    @property
    def res(self):
        return self.__res
    def __get_dict_list(self):
        """
        获取字典列表
        :return:
        """
        # 判断字典的位置是否正确
        if not os.path.exists(self.__dict_path):
            self.__dict_path = dict_path
        self.__dict_list = File.txt2list(self.__dict_path)


    def __cache(self):
        """
        存储数据
        :return:
        """
        # save_path = ...sub_domain/wuyecao.net/20240304.txt/csv
        # 获取域名
        domain = self.__url.split("://")[1]
        # 先获取日期的名字
        data_name = File.mkdatename()
        save_path = f"{cache_base_path}/dir_scan/{domain}/{data_name}.txt"
        for d in self.__res:
            File.data2txt(d, save_path)
    def start(self):
        url = input("请输入url:")
        self.__url = url
        dict_path = input("请输入字典路径:")
        self.__dict_path = dict_path

        print(f"开始：{self.__url}的扫描：........")
        # 先读取字典
        self.__get_dict_list()
        # 处理url
        if self.__url[-1] != '/':
            self.__url += "/"
        # 生产者： 生产url
        for d in self.__dict_list:
            url_p = f"{self.__url}{d}"
            self.__queue.put(url_p)
        # 记录总长度
        self.__queue_length = self.__queue.qsize()
        # 消费者： 线程
        for i in range(self.__thread_count):
            t = dir_scan.Scan(self.__queue, self, self.__res)
            self.__threads.append(t)
        # 启动
        for t in self.__threads:
            t.start()
        # 等待子线程结束
        for t in self.__threads:
            t.join()

        print("扫描结束！")
        # 存储数据
        self.__cache()

    class Scan(threading.Thread):
        def __init__(self, q, obj, res, name=None):
            self.__q = q
            self.__obj = obj
            self.__res = res
            super().__init__(name=name)
            self.__status_list = [200, 302, 403]
        def __process_bar(self):
            """
            进度条
            :return:
            """
            # 进度条
            # 1 - (队列的剩余长度 / 总数)
            # 跑了多少
            persent = 1-(self.__q.qsize() / self.__obj.queue_length)
            bar = "="*int(persent*100)+">"
            sys.stdout.write("\r"+f"{bar}【{persent:.2%}】")

        def run(self):
            while not self.__q.empty():
                url = self.__q.get()
                try:
                    r = requests.get(url)
                    if r.status_code in self.__status_list:
                        self.__res.append(f"【*】{url}【{r.status_code}】")
                    # 更新进度条
                    threading.Thread(target=self.__process_bar).start()
                except Exception as e:
                    pass


# if __name__ == '__main__':
#     dir_scan = dir_scan("http://www.pikachu.com/", "../../dict/php.txt", 50)
#     dir_scan.start()
#     for u in dir_scan.res:
#         print(u)