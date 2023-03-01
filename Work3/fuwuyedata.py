import numpy as np
import pandas as pd
import pymysql

#连数据库
con=pymysql.connect(host = '10.33.16.13' # 连接名称，默认127.0.0.1
,user = 'root' # 用户名
,passwd='1q2w1q@W' # 密码
,port= 3306 # 端口，默认为3306
,db='mysql_dp_dm' # 数据库名称
,charset='utf8' # 字符编码
)
cur = con.cursor()

cur.execute("select * from DM_AI_SERVICE_SUMMARY_MA") # 多少条记录
data  = cur.fetchall(  )
cols = cur.description
col = []
for i in cols:
    col.append(i[0])
data = list(map(list, data))
data = pd.DataFrame(data,columns=col)
cur.close()
con.close()

def rename_index(data):
    date=data.iloc[0:1,1:2].values[0][0]
    val = ['指标名称','TIMECODE',date+'年2月绝对值',date+'年2月增速',date+'年3月绝对值',date+'年3月增速',
                    date+'年4月绝对值',date+'年4月增速',date+'年5月绝对值',date+'年5月增速',date+'年6月绝对值',date+'年6月增速',
                    date+'年7月绝对值',date+'年7月增速', date+'年8月绝对值',date+'年8月增速', date+'年9月绝对值',date+'年9月增速',
                    date+'年10月绝对值',date+'年10月增速', date+'年11月绝对值',date+'年11月增速', date+'年12月绝对值',date+'年12月增速'
                   ]
    df2 = pd.DataFrame(np.insert(data.values, 0, values=val, axis=0))
    df2.columns= ['zbmc','TIMECODE',date+'n2yJDZ',date+'n2yZS',date+'n3yJDZ',date+'n3yZS',
                    date+'n4yJDZ',date+'n4yZS',date+'n5yJDZ',date+'n5yZS',date+'n6yJDZ',date+'n6yZS',
                    date+'n7yJDZ',date+'n7yZS', date+'n8yJDZ',date+'n8yZS', date+'n9yJDZ',date+'n9yZS',
                    date+'n10yJDZ',date+'n10yZS', date+'n11yJDZ',date+'n11yZS', date+'n12yJDZ',date+'n12yZS'
                   ]
    df2.drop('TIMECODE',axis = 1,inplace = True) #axis参数默认为0
    return df2

final_data=pd.DataFrame()
for i in range(len(data.groupby('TIMECODE').size())):
    data1=data.iloc[i*11:i*11+11,:]
    data1=rename_index(data1)
    if final_data.empty:
        final_data=data1
    else:
        final_data = pd.merge(final_data,data1,on='zbmc',how='inner')
print(final_data)

#将指标名称这一列切割留下
zbmc=[]
for i in final_data.iloc[:,0].values:
    if '&' in i:
        a=i.split('&')[-1]
        a=a.strip()
        zbmc.append(a)
    else:
        zbmc.append(i)
print(zbmc)
final_data.loc[:,('zbmc')]=zbmc
# final_data

# final_data = final_data.set_index(keys='zbmc')



csvdata=pd.read_csv('data/营收历史数据整理.csv')
# print(csvdata)
# csvdata = csvdata.set_index(keys='zbmc')

# csvdata_zbmc=[]
# for i in csvdata.index.values:
#     csvdata_zbmc.append(i)
# for i in csvdata_zbmc:
#     final_data = pd.concat([csvdata,final_data],axis = 1,ignore_index=False)
# final_data.to_csv('data/服务.csv',encoding='utf_8_sig')

final_data = pd.merge(csvdata,final_data,on='zbmc',how='left')
#替换2022年之后的增速算法
for i in data["TIMECODE"].unique():
    print(i)
    val = [i+'n2yZS',i+'n3yZS',i+'n4yZS',i+'n5yZS',i+'n6yZS',
           i+'n7yZS',i+'n8yZS',i+'n9yZS',i+'n10yZS', i+'n11yZS',i+'n12yZS']
    val_now = [i+'n2yJDZ',i+'n3yJDZ',i+'n4yJDZ',i+'n5yJDZ',i+'n6yJDZ',
           i+'n7yJDZ',i+'n8yJDZ',i+'n9yJDZ',i+'n10yJDZ', i+'n11yJDZ',i+'n12yJDZ']
    j=str(int(i)-1)
    val_last=[j+'n2yJDZ',j+'n3yJDZ',j+'n4yJDZ',j+'n5yJDZ',j+'n6yJDZ',
           j+'n7yJDZ',j+'n8yJDZ',j+'n9yJDZ',j+'n10yJDZ', j+'n11yJDZ',j+'n12yJDZ']
    for i,j,k in zip(val,val_now,val_last):
        if final_data.loc[1,j] !=0 or final_data.loc[1,j] is None:
            final_data.loc[1,i]= (float(final_data.loc[1,j])/ float(final_data.loc[1,k])-1)*100
        else:
            final_data.loc[1,i]=0

final_data.to_csv('data/服务.csv',index=0,encoding='utf_8_sig')