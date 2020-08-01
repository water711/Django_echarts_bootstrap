# django + echarts + bootstrap 客流数据图表展示
### 一、目录结构  
* init目录：客流数据初始化  
    - create_virtual_data.py （创建虚拟数据）  
    - init_data.py （将data目录下的csv文件的客流数据写入数据库）
* keliu目录：客流数据处理及返回
    - views.py (django视图文件)
    - urls.py (django路由文件)
    - get_data.py (使用pandas进行数据处理)
* api目录：微信小程序端的API接口

### 二、环境
    - Python 3.8
    - Django 2.0

```python
#安装第三方库
pip3 install django==2.0 sqlalchemy pandas
```

### 三、运行
```python
python .init/create_virtual.py  #创建虚拟数据
python manage.py runserver
```

### 三、前端展示效果
<img src="http://qiniu.caizhenwei.top/demo2020-07-28.gif" />

### 四、可能出现的问题  
1、Linxu环境下，出现No module named '_bz2'  
```python
yum install bzip2-devel ，并重新编译python
```
