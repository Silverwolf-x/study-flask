# flask学习记录

[Flask 入门教程 3.0](https://helloflask.com/book/3/)

[TOC]

## http响应码

1. [信息响应](https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Status#信息响应) (`100`–`199`)
2. [成功响应](https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Status#成功响应) (`200`–`299`)
3. [重定向消息](https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Status#重定向消息) (`300`–`399`)
4. [客户端错误响应](https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Status#客户端错误响应) (`400`–`499`)
5. [服务端错误响应](https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Status#服务端错误响应) (`500`–`599`)

- 找不到文件`GET /static/style.css HTTP/1.1" 404 `

- 请求成功` "GET / HTTP/1.1" 200`
- 这是用于缓存的目的。它告诉客户端响应还没有被修改，因此客户端可以继续使用相同的缓存版本的响应。`"GET /static/images/totoro.gif HTTP/1.1" 304 -
  304`

## URL规则

```python
from flask import Flask
app = Flask(__name__)
@app.route('/')# 请求处理函数
def hello():
    return 'Hello'
```

## 模板 templates 

把包含变量和运算逻辑的 HTML 或其他格式的文本叫做**模板**，执行这些变量替换和逻辑计算工作的过程被称为**渲染**

1. 在 templates 目录下创建一个 index.html 

2. 使用Jinja2 的语法写html
   - `{{ ... }}` 用来标记变量。
   - `{% ... %}` 用来标记语句，比如 if 语句，for 语句等。
   - `{# ... #}` 用来写注释。

```html
<!DOCTYPE html>  <!-- 定义文档类型为HTML -->
<html lang="en">  <!-- 定义HTML文档的语言为英语 -->
<head>
    <meta charset="utf-8">  <!-- 设置字符集为UTF-8，支持各种字符，包括中文 -->
    <title>{{ name }}'s Watchlist</title>  <!-- 设置页面标题，使用变量 name 的值 -->
</head>
<body>
    <h2>{{ name }}'s Watchlist</h2>  <!-- 创建二级标题，显示 Watchlist 的所有者的名字 -->
    <!-- 使用 length 过滤器获取 movies 变量的长度 -->
    <p>{{ movies|length }} Titles</p>  <!-- 在段落中显示 movies 变量中电影的数量 -->
    <ul>
        {% for movie in movies %}  <!-- 迭代 movies 变量 -->
        <li>{{ movie.title }} - {{ movie.year }}</li>  <!-- 在列表中显示每部电影的标题和年份 -->
        {% endfor %}  <!-- 使用 endfor 标签结束 for 语句 -->
    </ul>
    <footer>
        <small>&copy; 2018 <a href="http://helloflask.com/book/3">HelloFlask</a></small>  <!-- 显示版权信息和链接到 HelloFlask 网站 -->
    </footer>
</body>
</html>
```

```html
<h1>这是一个标题</h1>
<p>这是一个段落。</p>
<a href="https://www.runoob.com">这是一个链接</a>
img src="/images/logo.png" width="258" height="39" />
<li>无序 HTML 列表</li>
<!DOCTYPE> 声明的目的是让浏览器能够正确地渲染页面
<meta name="viewport" content="width=device-width, initial-scale=1.0">设置页面的视口，让页面根据设备的宽度来自动缩放页面，这样会让移动设备拥有更好的浏览体验
```

## 静态文件 static

静态文件（static files）和我们的模板概念相反，指的是内容不需要动态生成的文件。比如图片、CSS 文件和 JavaScript 脚本等。

1. 创建一个 static 文件夹来保存静态文件

2. html使用`url_for()` 函数,返回给出资源所在的 URL

对于静态文件，需要传入的端点值是 `static`,使用 `filename`参数传入相对于 static 文件夹的文件路径。

```
<img src="{{ url_for('static', filename='foo.jpg') }}">
```

花括号部分的调用会返回 `/static/foo.jpg`。

## 添加css

为对应的元素设置 `class` 属性值，以便和对应的 CSS 定义关联起来：

```html
<ul class="movie-list">
<img alt="Avatar" class="avatar" src="{{ url_for('static', filename='images/avatar.png') }}">
```

在页面的 `<head>` 标签内引入这个 CSS 文件

## 数据库

```pip
pip install flask-sqlalchemy
```

SQLAlchemy需要使用其他的python的数据库驱动来连接数据库

如果使用mysql，安装pymysql包

如果使用SQL Server Management Studio，安装pymssql包

### SQL Server Management Studio连接

默认有一个初始sql server账户：sa，密码为123456

sql server配置管理器中，要启用`sql sever配置管理器（本地）--sql sever`和`sql server网络配置--TCP/IP`

```python
import pymssql
from sqlalchemy import create_engine
import pandas as pd
# '数据库类型+数据库驱动名称://用户名:口令@机器地址/数据库名',echo=True在终端输出日志
# 'mssql+pymssql://username:password@host/dbname'(无端口号)
con = create_engine('mssql+pymssql://sa:123456@DESKTOP-4KEIUAR/pubs?charset=utf8')
print(pd.read_sql('select * from jobs', con))
```

## 使用flask将虚拟数据存入数据库

1. 手动在ssms中创造flasktest数据库，然后初始化数据库

```python
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pymssql://sa:123456@DESKTOP-4KEIUAR/flasktest?charset=utf8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控
db = SQLAlchemy(app)
```

2. 初始化属性

```python
class User(db.Model):  # 表名将会是 user（自动生成，小写处理）
    id = db.Column(db.Integer, primary_key=True)  # 主键
    name = db.Column(db.String(20))  # 名字
    movies = db.relationship("Movie", backref = "User")# 关联下面的外鍵，不是表中col
class Movie(db.Model):  # 表名将会是 movie
    id = db.Column(db.Integer, primary_key=True)  # 主键
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)# 外键，用户id
    title = db.Column(db.String(60))  # 电影标题
    year = db.Column(db.String(4))  # 电影年份
```

- 表间一对多关联

先Movie表中设置col的外键属性，然后在User表中设置外键的关联

3. 载入数据函数

```python
def fake_data(refresh = False):
    if refresh:
        db.drop_all()# 清空database的所有表
        db.create_all()# 按照之前设置的类创建database的表
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

```

4. 在非db.Model类中调用db.session等命令（如def的函数），需要加上`with app.app_context()`

```python
with app.app_context():
    fake_data(refresh=True)
```

## 模板优化

1. 减少在 `render_template()` 函数里传入的关键字user参数，避免冗余

```python
@app.context_processor
def inject_user():  # 函数名可以随意修改
    user = User.query.first()
    return dict(user=user)  # 需要返回字典，等同于 return {'user': user}
```

这个函数返回的变量（以字典键值对的形式）将会统一注入到每一个模板的上下文环境中，因此可以在模板中直接使用 `user` 变量。

2. 基模板（base template）

- 基模板中包含完整的 HTML 结构和导航栏、页首、页脚等通用部分。在子模板里，我们可以使用 `extends` 标签来声明继承自某个基模板

- 基模板中需要在实际的子模板中追加或重写的部分则可以定义成块（block）。块使用 `block` 标签创建， `{% block 块名称 %}` 作为开始标记，`{% endblock %}` 或 `{% endblock 块名称 %}` 作为结束标记。通过在子模板里定义一个同样名称的块，你可以向基模板的对应块位置追加或重写内容。

- 默认的块重写行为是覆盖，如果你想向父块里追加内容，可以在子块中使用 `super()` 声明，即 `{{ super() }}`。

```html
{% extends 'base.html' %}

{% block content %}
<p>{{ movies|length }} Titles</p>
<ul class="movie-list">
    {% for movie in movies %}
    <li>{{ movie.title }} - {{ movie.year }}
        <span class="float-right">
            <a class="imdb" href="https://www.imdb.com/find?q={{ movie.title }}" target="_blank" title="Find this movie on IMDb">IMDb</a>
        </span>
    </li>
    {% endfor %}
</ul>
<img alt="Walking Totoro" class="totoro" src="{{ url_for('static', filename='images/totoro.gif') }}" title="to~to~ro~">
{% endblock %}
```

