# -*- coding:utf-8 -*-

import os
import pandas as pd
import sqlite3


def create_table():
    connect = sqlite3.connect('../db.sqlite3')
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

def insert(file_list):
    connect = sqlite3.connect('../db.sqlite3')
    cursor = connect.cursor()  # 获取数据库游标

    for file in file_list:
        df = pd.read_csv(file, skiprows=1, encoding='gb18030')
        for i in range(len(df)):
            row = df.iloc[i].values  # 返回一个list
            channel = row[0]
            k_date = row[1][:10]
            k_hour = row[1][10:13]
            in_num = int(row[2])
            out_num = int(row[3])
            k_status = 1 if row[4] == '成功' else 0
            print(row)

            sql = "insert into keliu (channel, k_date, k_hour, in_num, out_num, k_status) VALUES (?,?,?,?,?,?)"
            cursor.execute(sql, (channel, k_date, k_hour, in_num, out_num, k_status))  # 执行sql语句，用游标的execute()方法

    connect.commit()  # 提交事务
    cursor.close()  # 关闭游标
    connect.close()  # 关闭数据库


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(ROOT_DIR, 'data')

for root,dirs,files in os.walk(DATA_DIR):
    file_list = []
    for file in files:
        path = './data/' + file
        file_list.append(path)

if __name__ == "__main__":
    # create_table()  #创建表
    insert(file_list)