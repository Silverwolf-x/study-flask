# 第 3 章：模板
from flask import Flask, render_template
from sqlalchemy import create_engine,text
from flask_sqlalchemy import SQLAlchemy
import pandas as pd


app = Flask(__name__)

# engine = create_engine('mysql+pymysql://root:20190218@127.0.0.1:3306/test')
# sql = 'select * from jobs'
# print(pd.read_sql(sql, con))
db_name = 'flasktest'
app.config['SQLALCHEMY_DATABASE_URI'] = f'mssql+pymssql://sa:123456@DESKTOP-4KEIUAR/{db_name}?charset=utf8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控
db = SQLAlchemy(app) 

'''
创建外键后，要在原表关联起来 
'''

class User(db.Model):  # 表名将会是 user（自动生成，小写处理）
    # __tablename__ = "User"
    id = db.Column(db.Integer, primary_key=True)  # 主键
    name = db.Column(db.String(20))  # 名字

    movies = db.relationship("Movie", backref = "User")# 关联，不是表中col

class Movie(db.Model):  # 表名将会是 movie
    id = db.Column(db.Integer, primary_key=True)  # 主键
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)# 外键，用户id
    title = db.Column(db.String(60))  # 电影标题
    year = db.Column(db.String(4))  # 电影年份

def fake_data(refresh = False):
    if refresh:
        db.drop_all()
        db.create_all()
    name = 'Silverwolf-x'
    movies = [
        {'title': 'My Neighbor Totoro', 'year': '1988'},
        {'title': 'Dead Poets Society', 'year': '1989'},
        {'title': 'A Perfect World', 'year': '1993'},
        {'title': 'Leon', 'year': '1994'},
        {'title': 'Mahjong', 'year': '1996'},
        {'title': 'Swallowtail Butterfly', 'year': '1996'},
        {'title': 'King of Comedy', 'year': '1999'},
        {'title': 'Devils on the Doorstep', 'year': '1999'},
        {'title': 'WALL-E', 'year': '2008'},
        {'title': 'The Pork of Music', 'year': '2012'},
    ]

    user = User(name=name)
    db.session.add(user)
    db.session.commit()# 先commit这个表，自动生成主键id，然后再传到下一个表作为外键
    # print(user.id)

    for m in movies:
        movie = Movie(title=m['title'], year=m['year'],user_id = user.id)
        db.session.add(movie)
    db.session.commit()


@app.route('/')
def index():
    user = User.query.first()  # 读取用户记录
    movies = Movie.query.all()  # 读取所有电影记录
    return render_template('index.html', user=user, movies=movies)


if __name__ == "__main__":
    with app.app_context():
        fake_data(refresh=True)
    app.run()