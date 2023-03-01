#!/usr/bin/env python
# -*-coding:utf-8 -*-
# ***************************************************************************
# 文件名称：ai_mdp_apptopic_linux.py
# 功能描述：AI平台应用模型列表接口
# 输 入 表：
# 输 出 表：
# 创 建 者：ww
# 创建日期：20220712
# 修改日志：
# 修改日期：
# ***************************************************************************
# 程序调用格式：nohup python ai_mdp_apptopic_linux.py &
# ***************************************************************************

import json

from flask import render_template, Flask, Response

app = Flask(__name__)
import pymysql


# @app.route('/index', methods=['GET','post'])
@app.route('/mod_list', methods=['GET'])
def hello_world():
    result, fields = conn_db()

    # 数据格式化 fields 字段名，result 结果集
    # 字段数组 ['id', 'name', 'password']
    field = []
    for i in fields:
        # print(i)
        field.append(i[0])
    field2 = []
    for i in reversed(field):
        field2.append(i)
    # print(field2)
    # 返回的数组集合 ('62c0f7a2adbe1d000a5d16f8', '发布_GDP_影响因素模型预测date', '建模大赛')
    jieguo = []
    a = []
    for j in result:
        b = []
        for i in range(len(j) - 1, -1, -1):
            b.append(j[i])
        a.append(b)
        # print(a)
    for jjj in a:
        line_data = {}
        for ii, jj in zip(field2, jjj):
            print(ii, "-->", jj)
            line_data[ii] = jj
        jieguo.append(line_data)
    print(jieguo)
    jieguo = get_rownumber(jieguo)
    # 判断type_name名字是否相同，相同的塞进同一个mod列表
    names = []
    zuihou = []
    for d in jieguo:
        newname = d['type_name']
        if newname in names:
            for z in zuihou:
                if z['type_name'] == d['type_name']:
                    zui = {}
                    zui['mdp_name'] = d['mdp_name']
                    zui['ID'] = d['ID']
                    zui['predict_date'] = d['predict_date']
                    zui['source_date'] = d['source_date']
                    zui['predict_count'] = d['predict_count']
                    z['mod'].append(zui)
        else:
            names.append(newname)
            p3 = {}
            mod = []
            zui = {}
            zui['mdp_name'] = d['mdp_name']
            zui['ID'] = d['ID']
            zui['predict_date'] = d['predict_date']
            zui['source_date'] = d['source_date']
            zui['predict_count'] = d['predict_count']
            mod.append(zui)
            p3['type_name'] = newname
            p3['mod'] = mod
            zuihou.append(p3)
    print(zuihou)
    str_json = json.dumps(zuihou, ensure_ascii=False, indent=2)
    return str_json


def get_rownumber(jieguo):
    conn = pymysql.connect(host='10.33.16.18', user='root', password='1q2w1q@W', database='hive', charset='utf8')
    cursor = conn.cursor()
    jieguo2 = []
    for i in jieguo:
        data = i['predict_date'].lower()
        sql="select PARAM_VALUE from TABLE_PARAMS a where TBL_ID in (select TBL_ID from TBLS where TBL_NAME ='"+data+"') and PARAM_KEY ='numRows'"
        cursor.execute(sql)
        rownumber = cursor.fetchall()
        if len(rownumber) == 0:
           i['predict_count'] = None
        else:
           i['predict_count'] = int(rownumber[0][0])
        #print(int(rownumber[0][0]))
        jieguo2.append(i)
    cursor.close()
    conn.close()
    return jieguo2


def conn_db():
    conn = pymysql.connect(host='10.33.16.12', user='root', password='1q2w1q@W', database='mlp_mdp', charset='utf8')
    cursor = conn.cursor()

    sql = " select  a.ID,a.name as mdp_name,b.name as type_name , concat(concat('ds_',ds_id),concat('_',ds_cycle)) as source_date ,concat(concat(out_filename_rule,'_'),ds_cycle) as predict_date from mdp_apptopic a left join MDP_APPTOPIC_TYPE b on a.type_id=b.id "

    cursor.execute(sql)
    result = cursor.fetchall()
    fields = cursor.description  # 返回字段名称

    cursor.close()
    conn.close()

    return result, fields


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8090)

