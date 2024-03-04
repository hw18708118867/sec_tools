# coding=utf-8
# Author: HSJ
# 2024/3/4 10:40
# 主入口
import os

def plugin_list():
    path = "./plugins"
    file_list = os.listdir(path)
    file_list = list(filter(lambda f: os.path.isdir(os.path.join(path, f)), file_list))
    plugin_list = []
    index = 1
    for f in file_list:
        plugin_list.append({index: f})
        index += 1
    return plugin_list

if __name__ == '__main__':
    print("欢迎使用sec-tools工具包！")
    plugin_list = plugin_list()
    for p in plugin_list:
        for k in p.keys():
            print("\t"+str(k), ":", p[k])
    index = int(input("请输入模块编号："))
    # 遍历取模块名字
    plugin_name = ""
    for p in plugin_list:
        if index == list(p.keys())[0]:
            plugin_name = p[index]
    # 动态引入对应的模块
    tmp = f"plugins.{plugin_name}.{plugin_name}"
    import_script = f'from {tmp} import {plugin_name}'
    # 让python去解析字符串
    exec(import_script)
    obj = eval(f"{plugin_name}()")
    obj.start()

