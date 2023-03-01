import json

from flask import render_template, Flask, Response

app = Flask(__name__)
import pymysql

conn = pymysql.connect(host='10.33.16.12', user='root', password='1q2w1q@W', database='mlp_mdp', charset='utf8')
cursor = conn.cursor()

# @app.route('/index', methods=['GET','post'])
@app.route('/index', methods=['GET'])
def hello_world():
    sql = "select  a.ID,a.name as mdp_name,b.name as type_name from mdp_apptopic a left join MDP_APPTOPIC_TYPE b on a.type_id=b.id"
    cursor.execute(sql)
    result = cursor.fetchall()
    fields = cursor.description #返回字段名称

    # cursor.close()
    # conn.close()
    # 数据格式化 fields 字段名，result 结果集
    # 字段数组 ['id', 'name', 'password']
    field = []
    for i in fields:
        print(i)
        field.append(i[0])
    field2=[]
    for i in reversed(field):
        field2.append(i)
    print(field2)
    # 返回的数组集合 ('62c0f7a2adbe1d000a5d16f8', '发布_GDP_影响因素模型预测date', '建模大赛')
    jieguo=[]
    a = []
    for j in result:
        b=[]
        for i in range(len(j)-1,-1,-1):
            b.append(j[i])
        a.append(b)
        print(a)
    for jjj in a:
        line_data = {}
        for ii,jj in zip(field2,jjj):
            line_data[ii]=jj
        jieguo.append(line_data)
    # print(a)
    print(jieguo)
    # 判断type_name名字是否相同，相同的塞进同一个mod列表
    oldname=None
    newname=None
    zuihou=[]
    for d in jieguo:
        p3 = {}
        mod = []
        p2={}
        newname=d['type_name']
       # if newname==oldname:
       #     tech_names = {'mdp_name', 'ID'}
       #     p2 = {key: value for key, value in d.items() if key in tech_names}
       #     print(p2)
        zui={}
       # if p2!=None:
       #      zui['mdp_name']=p2['mdp_name']
       #      zui['ID']=p2['ID']
       #      mod.append(zui)
       # else:
        zui['mdp_name'] = d['mdp_name']
        zui['ID'] = d['ID']
        mod.append(zui)

        p3['type_name']=newname
        p3['mod']=mod
        print(p3)
        zuihou.append(p3)
        # oldnamee=newname
    print(zuihou)
    str_json=json.dumps(zuihou,ensure_ascii=False,indent=2)


    # aa='发布_GDP_生产函数模型预测date'
    # aa=Response(result)

    return str_json

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=8090)
   # hello_world