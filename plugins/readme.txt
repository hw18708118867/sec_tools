这个plugins下面的模块是需要给根下面的main.py调用
欢迎使用xxxx工具，请选择如下模块：
1.dir_scan
2.gen_pwd_dict
3.port_scan
4.sql_injection
5.sub_domain
6.xss_injection

选择： 5

必须让下面的所有的模块遵循同一个规则：
1. 文件夹的名字和类的名字一致
obj = sub_domain()
obj.start()