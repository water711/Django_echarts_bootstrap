# -*- coding:utf-8 -*-

from django.shortcuts import render, redirect
import keliu.get_data as get_data
import os
import sqlite3
import pandas as pd

def index(request):
    if request.method == 'GET':
        k_date = get_data.newest_record()
    else:
        k_date = request.POST.get('date')
        k_date = k_date.replace('-','/')

    x1,y1 = get_data.hour(k_date)  #每小时进入人数

    x2,y2,s = get_data.channel(k_date)   #各通道进入人数

    pie_dict = get_data.percent(k_date)  # 各楼层进入人数

    # 本周与上周增幅数据
    this_week, last_week, week_increase = get_data.increase(k_date)

    k = k_date.split('/')
    title = "%s年%s月%s日 XX商业综合体客流数据（总人数：%s）"%(k[0], k[1], k[2], s)

    return render(request, 'index.html',{ 'title': title,
                                         'x1':x1, 'y1':y1,
                                         'x2':x2, 'y2':y2,
                                         'pie_dict':pie_dict,
                                         'last_week':last_week, 'this_week':this_week, 'week_increase':week_increase})

def calc(request):
    if request.method == 'GET':
        return render(request, 'calc.html')
    if request.method == 'POST':
        print(request.POST)
        return render(request, 'calc.html')

def upload(request):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if request.method == 'POST':
        obj = request.FILES.get('data')
        path = os.path.join(BASE_DIR, 'upload', obj.name)
        with open(path, 'wb') as f:
            for i in obj.readlines():
                f.write(i)

        connect = sqlite3.connect('db.sqlite3')
        cursor = connect.cursor()  # 获取数据库游标
        df = pd.read_csv(path, skiprows=1, encoding='gb18030')
        print(df)
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
    return redirect('/index/')