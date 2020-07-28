#_*_ coding:utf-8_*_

from sqlalchemy import create_engine
from datetime import datetime, timedelta
from keliu.settings import BASE_DIR
import pandas as pd
import warnings
warnings.filterwarnings("ignore")


sqlite_file = 'sqlite:///' + BASE_DIR + '\db.sqlite3'

def read(k_date):
    '''
    该函数负责从数据库查询数据
    :param k_date: 日期
    :return: 该日期下的客流数据
    '''
    engine = create_engine(sqlite_file)
    sql = "select * from keliu where k_date = '" + str(k_date) + "'"

    # read_sql_query的两个参数: sql语句， 数据库连接
    df = pd.read_sql_query(sql,con=engine)
    return df

def newest_record():
    '''
    返回数据库中最新数据的日期
    :return:
    '''
    engine = create_engine(sqlite_file)
    sql = "select k_date from keliu GROUP BY k_date ORDER BY k_date desc LIMIT 1"
    df = pd.read_sql_query(sql,con=engine)
    k_date = df['k_date'].at[0]
    return k_date

def increase(k_date):
    '''

    :param k_date: 日期
    :return: 三个列表，分别为本周7天、上周7天、本周与上周的客流增幅数据
    '''
    k_date = datetime.strptime(k_date, "%Y/%m/%d")
    dayOfWeek = k_date.isoweekday()  ###返回数字1-7代表周一到周日
    num = dayOfWeek + 7
    temp = []
    for i in range(num-1 ,-1 ,-1):
        d = k_date + timedelta(days = -i)
        keliu_data = str(d.date()).replace('-', '/')
        x,y,s = channel(keliu_data)
        if s == 0:
            continue
        temp.append(s)
    last_week = temp[:7]
    this_week = temp[7:]

    #计算本周与上周数据增幅
    week_increase = map(lambda x,y: (x-y)/y*100, this_week, last_week)  #计算增幅
    week_increase = map(lambda x: "%.2f%%" % x, week_increase) #转换为百分比
    week_increase = list(week_increase)

    #不满7个元素，补充空字符
    if len(this_week) != 7:
        n = len(this_week)
        for i in range(7-n):
            this_week.append(' ')
            week_increase.append(' ')
    return this_week,last_week,week_increase

def percent(k_date):
    '''
    计算各方位客流人数
    :param k_date:
    :return: 字典，各层对应的客流人数
    '''
    df = read(k_date)
    df = df.loc[:, ['channel', 'in_num']]

    df.channel[df.channel.str.contains('西南')] = "西边"
    df.channel[df.channel.str.contains('西北')] = "西边"
    df.channel[df.channel.str.contains('西入口')] = "西边"
    df.channel[df.channel.str.contains('南入口')] = "南边"
    df.channel[df.channel.str.contains('东入口')] = "东边"
    df.channel[df.channel.str.contains('东北')] = "东边"
    df.channel[df.channel.str.contains('北入口')] = "北边"

    df = df.groupby(['channel'], as_index=False).sum()
    label = df['channel'].values.tolist()
    value = df['in_num'].values.tolist()
    pie_dict = zip(label, value)
    return pie_dict

def hour(k_date=newest_record()):
    '''

    :param k_date:
    :return: 两个列表，x：小时, y:每小时人数
    '''
    df = read(k_date)
    df = df.loc[:, ['channel', 'k_hour', 'in_num', 'out_num']]
    df = df.groupby(['k_hour'], as_index=False).sum()

    x = df['k_hour'].values.tolist()
    y = df['in_num'].values.tolist()
    return x,y

def channel(k_date):
    '''
    计算每个通道入口进入人数
    :param k_date:
    :return: x：各通道名称，y：各通道人数, s：总人数
    '''
    df = read(k_date)
    df = df.loc[:, ['channel', 'in_num', 'out_num']]

    df.channel[df.channel.str.contains('1F-JK-01')] = "货梯厅出入口"
    df.channel[df.channel.str.contains('1F-JK-04')] = "东南门出入口"
    df.channel[df.channel.str.contains('1F-JK-05')] = "东边5.6.7客梯厅"
    df.channel[df.channel.str.contains('1F-JK-11')] = "东中庭出入口"
    df.channel[df.channel.str.contains('1F-JK-15')] = "北门出入口"
    df.channel[df.channel.str.contains('1F-JK-19')] = "公寓服务台"
    df.channel[df.channel.str.contains('1F-JK-43')] = "西边3.4客梯厅"
    df.channel[df.channel.str.contains('1F-JK-45')] = "西南门出入口"
    df.channel[df.channel.str.contains('1F-JK-88')] = "卜蜂西出口"
    df.channel[df.channel.str.contains('1F-JK-89')] = "鹅咏稻香门口"
    df.channel[df.channel.str.contains('1F-JK-90')] = "1·2货梯边走廊"
    df.channel[df.channel.str.contains('2F-JK-18')] = "西边上下扶梯"
    df.channel[df.channel.str.contains('B1F-JK-05')] = "南步行街步梯"
    df.channel[df.channel.str.contains('B1F-JK-09')] = "东边5.6.7客梯厅"
    df.channel[df.channel.str.contains('B1F-JK-16')] = "步行街至停车场"
    df.channel[df.channel.str.contains('B1F-JK-36')] = "1.2号客梯厅"
    df.channel[df.channel.str.contains('B1F-JK-52')] = "西北步行街扶梯"
    df.channel[df.channel.str.contains('B1F-JK-53')] = "西北步行街步梯"
    df.channel[df.channel.str.contains('B1F-JK-65')] = "西边进负1停车场"
    df.channel[df.channel.str.contains('B1F-JK-92')] = "西边3.4客梯厅"
    df.channel[df.channel.str.contains('B2F-JK-22')] = "西边3.4客梯厅"
    df.channel[df.channel.str.contains('B3F-JK-10')] = "东边5.6.7客梯厅"
    df.channel[df.channel.str.contains('B3F-JK-11')] = "东南边上下扶梯"
    df.channel[df.channel.str.contains('B3F-JK--25')] = "北1.2号客梯厅"
    df.channel[df.channel.str.contains('B3F-JK-46')] = "西边3.4客梯厅"
    df.channel[df.channel.str.contains('B3F-JK-48')] = "卜蜂西边扶梯"
    df.channel[df.channel.str.contains('B3F-JK-56')] = "卜蜂东南扶梯"

    df = df.groupby(['channel'], as_index=False).sum()
    df = df[df['in_num'] >= 300]
    df = df.sort_values(by='in_num', ascending=True)
    x = df['channel'].values.tolist()
    y = df['in_num'].values.tolist()
    s = df['in_num'].sum()
    return x,y,s

if __name__ == '__main__':
    pass
    #k_date = newest_record()
    # x,y = hour(k_date)
    #print(x,y)
    # file = 'sqlite:///'+ BASE_DIR + '\db.sqlite3'
    # print(file)
