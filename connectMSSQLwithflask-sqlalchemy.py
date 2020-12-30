"""
使用flask_sqlalchemy连接MS SQL server数据库的方法
2020-12-30
"""

from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

DBUser = 'flask'
DBPassword = '123' #yufengcun123*
DBHost = '192.168.100.5'
DBName = 'filehost2017'
app.config['SQLALCHEMY_DATABASE_URI'] = f'mssql+pymssql://{DBUser}:{DBPassword}@{DBHost}/{DBName}'
db= SQLAlchemy(app)


# 具体映射类
class Flaskdemo(db.Model):
    # 指定映射表名
    __tablename__ = 'flaskdemo'
    # id 设置为主键
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 指定 name 映射到 name 字段
    content = db.Column('content', db.String(200))
    date_created = db.Column('date_created', db.DateTime, default=datetime.utcnow()) # datetime.today().strftime("%Y-%m-%d")
    def __repr__(self):
        return '<Task %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Flaskdemo(content=task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'
    else:
        tasks = Flaskdemo.query.order_by(Flaskdemo.date_created).all()
        return render_template('index.html', tasks=tasks)


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Flaskdemo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    # task = Flaskdemo.query.get_or_404(id)
    task = Flaskdemo.query.filter_by(id=id).first_or_404()
    if request.method == 'POST':
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('update.html', task=task)


if __name__ == "__main__":
    app.run(port=3000, debug=True)
