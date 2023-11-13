# 测试ssms数据库连接
import pymssql
from sqlalchemy import create_engine,text
import pandas as pd
 
def conn():
    connect = pymssql.connect('DESKTOP-4KEIUAR', 'sa', '123456', 'master') #服务器名,账户,密码,数据库名
    if connect:
        print("连接到张瑞成功!")
    return connect
def get_mysql_engine():
    # '数据库类型+数据库驱动名称://用户名:口令@机器地址:端口号/数据库名'
    # 'mysql+pymysql://username:password@host:3306/dbname'(默认3306)
    # 初始化数据库连接，使用pymysql模块
    engine = create_engine('mysql+pymysql://root:20190218@127.0.0.1:3306/test')
    return engine
    
def get_mssql_engine():
    # '数据库类型+数据库驱动名称://用户名:口令@机器地址/数据库名',
    # 'mssql+pymssql://username:password@host/dbname'(无端口号)
    engine = create_engine('mssql+pymssql://sa:123456@DESKTOP-4KEIUAR/pubs?charset=utf8')
    return engine

if __name__ == '__main__':
    # conn()
    sql = 'select * from jobs'
    con = get_mssql_engine()
    connection = get_mssql_engine().connect()
    result = connection.execute(text(sql))
    # print(pd.read_sql(result,con=connection))
    # data = [dict(zip(r.keys(), r)) for r in result]
    print(result.all())
    # print(data)
    print(pd.read_sql(sql, con))
    connection.close()