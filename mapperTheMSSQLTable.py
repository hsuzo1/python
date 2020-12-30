# -*- coding: utf-8 -*-
"""
表映射的方法连接MSSQL Server数据库
2020-12-30
"""
from flask import Flask, render_template, url_for, request, redirect
from sqlalchemy.dialects.mssql import \
    BIGINT, BINARY, BIT, CHAR, DATE, DATETIME, DATETIME2, \
    DATETIMEOFFSET, DECIMAL, FLOAT, IMAGE, INTEGER, MONEY, \
    NCHAR, NTEXT, NUMERIC, NVARCHAR, REAL, SMALLDATETIME, \
    SMALLINT, SMALLMONEY, SQL_VARIANT, TEXT, TIME, \
    TIMESTAMP, TINYINT, UNIQUEIDENTIFIER, VARBINARY, VARCHAR
from sqlalchemy import Table, MetaData, Column, Integer, String, ForeignKey
from sqlalchemy.orm import mapper, sessionmaker
from datetime import datetime
from config import Base, engine

app = Flask(__name__)


flaskdemo_metadata = MetaData()
demo = Table('flaskdemo', flaskdemo_metadata,
            Column('id', Integer, primary_key=True, autoincrement=True),
            Column('content', String(200)),
            Column('date_created', DATE, default=datetime.utcnow())
        )

class Flaskdemo(object):
    def __init__(self, id, content, date_created):
        self.id = id
        self.content = content
        self.date_created = date_created

mapper(Flaskdemo, demo)

# 创建表
Base.metadata.create_all(engine)
# 建立会话
Session = sessionmaker(bind=engine)
# 创建 Session 类实例
session = Session()


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Flaskdemo(content=task_content)
        try:
            session.add(new_task)
            session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'

    else:
        tasks = session.query(Flaskdemo).all()
        return render_template('index.html', tasks=tasks)


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = session.query(Flaskdemo).filter(Flaskdemo.id==id).one()
    try:
        session.delete(task_to_delete)
        session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = session.query(Flaskdemo).filter(Flaskdemo.id==id).one()
    if request.method == 'POST':
        task.content = request.form['content']
        try:
            session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('update.html', task=task)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000, debug=True)
    # 关闭
    session.close()



"""
config.py
# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
import pymssql


DBUser = 'flask'
DBPassword = '123' #yufengcun123*
DBHost = '192.168.100.5'
DBName = 'filehost2017'
engine = create_engine(f'mssql+pymssql://{DBUser}:{DBPassword}@{DBHost}/{DBName}', echo=False)

# 映射基类
Base = declarative_base()

# 关闭警告，否则会有警告提示
SQLALCHEMY_DATABASE_URI = False
SQLALCHEMY_TRACK_MODIFICATIONS = False
"""
