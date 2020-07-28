# django + echarts + bootstrap 客流数据图表展示
一、目录结构  
* init目录：客流数据初始化  
    - create_virtual_data.py （创建虚拟数据）  
    - init_data.py （将data目录下的csv文件的客流数据写入数据库）
* keliu目录：客流数据处理及返回
* api目录：微信小程序端的API接口

二、运行测试
```python
python .init/create_virtual.py  #创建虚拟数据
python manage.py runserver
```

三、前端展示效果
![](http://qiniu.caizhenwei.top/demo2020-07-28.gif)
