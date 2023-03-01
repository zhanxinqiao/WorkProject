import pymysql

if __name__ == '__main__':
    db = pymysql.connect(user='root', password='123456', host='localhost', port=3306, db='weather')
    cursor = db.cursor()
    # ==========================①=======================================
    # weather00 13~17年每天八点的测量值  用多年的总和中和掉不同年份可能存在的误差
    #目的  计算一年中各天的相应环境数据均值
    with open("F:\\input\\OutWeather\\part-r-00000", "r", encoding='utf-8') as f:  # 打开文本
        data = f.readlines()  # 读取文本
        for i in data:
            mon_day_value=i.split('\t')
            mon_day=mon_day_value[0].split('-')
            mon=mon_day[0]
            day=mon_day[1]
            value=mon_day_value[1].split(',')
            cursor.execute("insert into w01(mon,day,PM2_5,PM10,SO2,NO2,CO,O3,Dewp,Rain)"
                           "values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
             (mon,day,value[0],value[1],value[2],value[3],value[4],value[5],value[6],value[7])
                           )
            db.commit()


    # ==========================②=======================================
    # 每年的各环境指标的均值，来计算出这几年环境变化
    with open("F:\\input\\OutWeather1\\part-r-00000", "r", encoding='utf-8') as f:  # 打开文本
        data = f.readlines()  # 读取文本
        for i in data:
            year_value = i.split('\t')
            year= year_value[0]
            value = year_value[1].split(',')
            cursor.execute("insert into w02(year,PM2_5,PM10,SO2,NO2,CO,O3,Dewp,Rain)"
                           "values(%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                           (year, value[0], value[1], value[2], value[3], value[4], value[5], value[6], value[7])
                           )
            db.commit()


    # ==========================③=======================================
    # // 每年_月的环境指标，可以来计算同比环比
    with open("F:\\input\\OutWeather2\\part-r-00000", "r", encoding='utf-8') as f:  # 打开文本
        data = f.readlines()  # 读取文本
        for i in data:
            year_mon_value=i.split('\t')
            year_mon=year_mon_value[0].split('-')
            year=year_mon[0]
            mon=year_mon[1]
            value=year_mon_value[1].split(',')
            cursor.execute("insert into w03(year,mon,PM2_5,PM10,SO2,NO2,CO,O3,Dewp,Rain)"
                           "values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
             (year,mon,value[0],value[1],value[2],value[3],value[4],value[5],value[6],value[7])
                           )
            db.commit()
    cursor.close()
    db.close()

