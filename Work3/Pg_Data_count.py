# -*- coding: utf-8 -*-
"""
Created on Tue Jun  8 23:36:38 2021
@Software: Spyder
@author: 盲区行者王
"""
from operator import concat

import pandas as pd
from re import sub
import psycopg2 ##导入

## 通过connect方法，创建连接对象 conn
## 这里连接的是本地的数据库
conn = psycopg2.connect(database="brain_of_tongji", user="brain_of_tongji", password="StBrain#6091GP", host="59.202.45.171", port="4545")
## 执行之后不报错，就表示连接成功了！
print('postgreSQL数据库“db_test”连接成功!')
# 获得游标对象
cursor = conn.cursor()
# sql语句
sql = """select oid, a.TABLE_NAME,a.rowCounts,a.counts_all,b.count_m from (select oid, relname as TABLE_NAME, reltuples as rowCounts,relnatts as counts_all from pg_class where relkind = 'r' and relname like 'ods_ytb_v_8%' order by oid  ) a left join (select attrelid,count(attname) as count_m from pg_attribute where attname like 'm%' group by attrelid order by attrelid) b on a.oid= b.attrelid;"""
# 执行语句
cursor.execute(sql)
# 抓取
rows = cursor.fetchall()

for index,name in enumerate(rows):
#i:下标，j:下标对应的值
    print('rows[{}] = {}'.format(index,name))
#print(rows)
# 事物提交
conn.commit()
# 关闭数据库连接
#cursor.close()
#conn.close()

data = pd.read_sql(sql,conn)
#def get_df_from_db_1(sql):
print(data)
table_name = data['table_name']
print(table_name)


df_new_all = pd.DataFrame()
for i in range(0, len(data)):  # df.shape[0]表示行数也可以
    table_name_one = table_name.iloc[i]
#   print(table_name.iloc[i])
    sql2 = """select p_day,count(*) as counts from  table_name_one group by p_day order by counts desc limit 1;"""
    #data_one = pd.read_sql(("table_name_one",'table_name_one',sql2), conn)
    data_one = pd.read_sql(sub("table_name_one", table_name_one, sql2), conn)
    print(data_one)
    data_one1 = data_one['counts']
    #df2 = pd.DataFrame({'table_name': ['a', 'b', 'd'],
    #                    'data2': range(3)})
    print(data_one1)
    df_new_all = df_new_all.append(data_one1)
    #data_all = concat([df1, data_one1])

df_new_all.index = range(len(df_new_all))
print(df_new_all)

datas = data.join(df_new_all)
print(datas)
datas.to_csv("./data.csv")
datas['counts_all']=datas['0']

datas['counts_all']=datas['count_all']*datas['counts_all']
datas['counts_m']=datas['count_m']*datas['counts_m']
value_m=datas['counts_all'].count()
value_all=datas['counts_m'].count()
print(value_all)
print(value_m)

#    return pd.read_sql(sql,conn)

#print(get_df_from_db_1(sql))
# 关闭数据库连接
cursor.close()
conn.close()

