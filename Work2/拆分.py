import numpy as np
import pandas as pd

data=pd.read_excel("./data/数据源.xlsx",header=2)
print(data)  #查看data这个值 若显示查看失败请改成print(data)  下列一些值相同

print(data.columns)  #查看列名

          ### 计算产品类型统计
value1=pd.DataFrame()
value1["所属大区"]=data["所属省区"]
value1["自有产品许可类"]=data[["产品\n金额","服务金额"]].apply(lambda x:(x["产品\n金额"]+x["服务金额"])/10000,axis=1) #计算出自有产品许可类
value1["自有产品订阅类"]=data["云产品\n金额"]/10000
value1["交付类"]=data[["A金额\n","B金额\n","增值服务金额"]].apply(lambda x:(x["A金额\n"]+x["B金额\n"]+x["增值服务金额"])/10000,axis=1) #计算出自有产品交付类
value1["OEM产品"]=data["M产品金额"]/10000
value1["第三方产品"]=data["第三方产品\n金额"]/10000
print(value1)

value2=value1.groupby(value1["所属大区"]).sum()  #按照所属大区这一列分组合并
print(value2)

value2["小计"] = value2[['自有产品许可类','自有产品订阅类','交付类','OEM产品','第三方产品']].sum(axis =1)  #添加行级合并计算
value2.loc["总计"] = value2[['自有产品许可类','自有产品订阅类','交付类','OEM产品','第三方产品','小计']].sum(axis =0)  #添加列级合并计算
print(value2)
#增加序号一列，并且保存
df = value2.reset_index()
df.index=df.index+1
df.index.name="序号"
df.to_excel("./data/产品类型统计.xlsx")

      ### 计算亏损分段统计
value11=pd.DataFrame()
value11["所属大区"]=data["所属省区"]
value11["亏损金额"]=data["亏损金额"]/10000
print(value11)

cloumn=["所属大区","亏损额≥200万数量","亏损额≥200万金额","100万≤亏损额＜200万数量","100万≤亏损额＜200万金额","50万≤亏损额＜100万数量",
         "50万≤亏损额＜100万金额","10≤亏损额＜50数量","10≤亏损额＜50金额","亏损额＜10万数量","亏损额＜10万金额"]
value22=pd.DataFrame(columns=cloumn)
print(value22)

for i in range(len(value11)):
    value22.loc[i,"所属大区"]=value11.loc[i,"所属大区"]
    val=value11.loc[i,"亏损金额"]
    if val>=200:
        value22.loc[i,"亏损额≥200万数量"]=1
        value22.loc[i,"亏损额≥200万金额"]=val
    elif val>=100 and val<200:
        value22.loc[i,"100万≤亏损额＜200万数量"]=1
        value22.loc[i,"100万≤亏损额＜200万金额"]=val
    elif val>=50 and val<100:
        value22.loc[i,"50万≤亏损额＜100万数量"]=1
        value22.loc[i,"50万≤亏损额＜100万金额"]=val
    elif val>=10 and val<50:
        value22.loc[i,"10≤亏损额＜50万数量"]=1
        value22.loc[i,"10≤亏损额＜50万金额"]=val
    else:
        value22.loc[i,"亏损额＜10万数量"]=1
        value22.loc[i,"亏损额＜10万金额"]=val
print(value22)

#按所属大区的组合并   相同大区合在一起
value33=value22.groupby(value22["所属大区"]).sum()
print(value33)

#增加"累计亏损数量","累计亏损金额"两列，将所在行数量、金额的值分别求和
value33["累计亏损数量"] = value33[['亏损额≥200万数量','100万≤亏损额＜200万数量','50万≤亏损额＜100万数量','10≤亏损额＜50数量','亏损额＜10万数量']].sum(axis =1)
value33["累计亏损金额"] = value33[['亏损额≥200万金额','100万≤亏损额＜200万金额','50万≤亏损额＜100万金额','10≤亏损额＜50金额','亏损额＜10万金额']].sum(axis =1)
print(value33)

#增加总计一行，将所有一列的值求和
value33.loc["总计"] = value33[['亏损额≥200万数量','亏损额≥200万金额','100万≤亏损额＜200万数量','100万≤亏损额＜200万金额','50万≤亏损额＜100万数量',
'50万≤亏损额＜100万金额','10≤亏损额＜50数量','10≤亏损额＜50金额','亏损额＜10万数量','亏损额＜10万金额',"累计亏损数量","累计亏损金额"]].sum(axis =0)
print(value33)

#增加序号一列，并且保存
df1 = value33.reset_index()
df1.index=df1.index+1
df1.index.name="序号"
print(df1)
df1.to_excel("./data/亏损分段统计.xlsx")