import os
import random
import sqlite3
from datetime import datetime, timedelta

baes_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def create_table():
    connect = sqlite3.connect(baes_dir + '/db.sqlite3')
    cursor = connect.cursor()   # 获取数据库游标

    sql = 'CREATE TABLE "keliu"( \
        id INTEGER PRIMARY KEY AUTOINCREMENT, \
        channel TEXT, \
        k_date TEXT, \
        k_hour INTEGER, \
        in_num INTEGER, \
        out_num INTEGER, \
        k_status INTEGER)'

    cursor.execute(sql)  # 执行sql语句，用游标的execute()方法
    connect.commit()  # 提交事务
    cursor.close()  # 关闭游标
    connect.close()  # 关闭数据库

create_table()  #创建表

start_data = '2019/01/01'
start_data = datetime.strptime(start_data, "%Y/%m/%d")  #字符串转datatime类型
channel_list = ['东入口','南入口','北入口','西入口','西南入口','西北入口','东北入口']

connect = sqlite3.connect(baes_dir + '/db.sqlite3')
cursor = connect.cursor()   # 获取数据库游标
sql = 'insert into keliu (channel, k_date, k_hour, in_num, out_num, k_status) values (?,?,?,?,?,?)'

for i in range(545):
    k_date = start_data + timedelta(days = i)
    k_date = str(k_date).split(" ")[0].replace('-', '/')
    for channel in channel_list:
        for k_hour in range(9,24):
            in_num = random.randint(1,2500)
            out_num = random.randint(1,2500)
            data = (channel, k_date, k_hour, in_num, out_num, 1)
            cursor.execute(sql, data)  # 执行sql语句，用游标的execute()方法
            print(data)

connect.commit()  # 提交事务
cursor.close()  # 关闭游标
connect.close()  # 关闭数据库



