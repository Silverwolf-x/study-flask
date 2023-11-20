# 第 3 章：模板
from flask import Flask, render_template
from flask import request, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# import pandas as pd
# engine = create_engine('mysql+pymysql://root:20190218@127.0.0.1:3306/test')
# sql = 'select * from jobs'
# print(pd.read_sql(sql, con))

db_name = 'flasktest'
app.config['SQLALCHEMY_DATABASE_URI'] = f'mssql+pymssql://sa:123456@DESKTOP-4KEIUAR/{db_name}?charset=utf8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控
db = SQLAlchemy(app) 

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

def fake_data(run = True, refresh = False):
    if not run:
        return 0
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


@app.context_processor
def inject_user():
    user = User.query.first()# 返回查询的第一条记录，如果未找到，则返回 None。（返回模型类实例）
    return dict(user=user)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

app.config['SECRET_KEY'] = 'dev'  # 等同于 app.secret_key = 'dev'
@app.route('/', methods=['GET', 'POST'])
def index():
    user = User.query.first()# 利用外键找到user的movie单
    # 这里先认为只有一个用户
    if request.method == 'POST':  # 判断是否是 POST 请求
        # 获取表单数据
        title = request.form.get('title')  # 传入表单对应输入字段的 name 值
        year = request.form.get('year')
        # 验证数据
        if not title or not year or len(year) > 4 or len(title) > 60:
            flash('Invalid input.')  # 显示错误提示
            return redirect(url_for('index'))  # 重定向回主页
        # 保存表单数据到数据库
        movie = Movie(title=title, year=year, user_id = user.id)  # 创建记录
        db.session.add(movie)  # 添加到数据库会话
        db.session.commit()  # 提交数据库会话
        flash('Item created.')  # 显示成功创建的提示
        return redirect(url_for('index'))  # 重定向回主页
    
    movies = Movie.query.filter_by(user_id = user.id).all()
    return render_template('index.html', movies=movies)

# 编辑电影条目
@app.route('/movie/edit/<int:movie_id>', methods=['GET', 'POST'])
def edit(movie_id):
    movie = Movie.query.get_or_404(movie_id)

    if request.method == 'POST':  # 处理编辑表单的提交请求
        title = request.form['title']
        year = request.form['year']

        if not title or not year or len(year) != 4 or len(title) > 60:
            flash('Invalid input.')
            return redirect(url_for('edit', movie_id=movie_id))  # 重定向回对应的编辑页面

        movie.title = title  # 更新标题
        movie.year = year  # 更新年份
        db.session.commit()  # 提交数据库会话
        flash('Item updated.')
        return redirect(url_for('index'))  # 重定向回主页

    return render_template('edit.html', movie=movie)  # 传入被编辑的电影记录

# 删除
@app.route('/movie/delete/<int:movie_id>', methods=['POST'])  # 限定只接受 POST 请求
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)  # 获取电影记录
    db.session.delete(movie)  # 删除对应的记录
    db.session.commit()  # 提交数据库会话
    flash('Item deleted.')
    return redirect(url_for('index'))  # 重定向回主页


if __name__ == "__main__":
    # with app.app_context():
    #     fake_data(refresh=True)
    fake_data(run=False)
    app.run()