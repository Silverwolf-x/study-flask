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

## 表单

### 典型表单

```html
<form method="post">  <!-- 指定提交方法为 POST -->
    <label for="name">名字</label>
    <input type="text" name="name" id="name"><br>  <!-- 文本输入框 -->
    <label for="occupation">职业</label>
    <input type="text" name="occupation" id="occupation"><br>  <!-- 文本输入框 -->
    <input type="submit" name="submit" value="登录">  <!-- 提交按钮 -->
</form>
```

- 在 `<form>` 标签里使用 `method` 属性将提交表单数据的 HTTP 请求方法指定为 POST。如果不指定，则会默认使用 GET 方法，这会将表单数据通过 URL 提交，容易导致数据泄露，而且不适用于包含大量数据的情况。
- `<input>` 元素必须要指定 `name` 属性，否则无法提交数据，在服务器端，我们也需要通过这个 `name` 属性值来获取对应字段的数据。

- 填写输入框标签文字的 `<label>` 元素不是必须的，只是为了辅助鼠标用户。当使用鼠标点击标签文字时，会自动激活对应的输入框，这对复选框来说比较有用。`for` 属性填入要绑定的 `<input>` 元素的 `id` 属性值。

- `autocomplete` 属性设为 `off` 来关闭自动完成（按下输入框不显示历史输入记录）

- `required` 标志属性，如果用户没有输入内容就按下了提交按钮，浏览器会显示错误提示

### 表单处理

修改一下视图函数

```
@app.route('/', methods=['GET', 'POST'])
```

两种方法的请求有不同的处理逻辑：对于 GET 请求，返回渲染后的页面；对于 POST 请求，则获取提交的表单数据并保存

### 添加表单数据

```python
if request.method == 'POST':  # 判断是否是 POST 请求
    # 获取表单数据
    title = request.form.get('title')  # 传入表单对应输入字段的 name 值
    year = request.form.get('year')
    # 验证数据
    if not title or not year or len(year) > 4 or len(title) > 60:
        flash('Invalid input.')  # 显示错误提示
        return redirect(url_for('index'))  # 重定向回主页
    # 保存表单数据到数据库
    movie = Movie(title=title, year=year)  # 创建记录
    db.session.add(movie)  # 添加到数据库会话
    db.session.commit()  # 提交数据库会话
    flash('Item created.')  # 显示成功创建的提示
    return redirect(url_for('index'))  # 重定向回主页
```

1. 请求对象

在请求触发时才会包含数据，所以你只能在视图函数内部调用它。它包含请求相关的所有信息，比如请求的路径（`request.path`）、请求的方法（`request.method`）、表单数据（`request.form`）、查询字符串（`request.args`）等等

`request.form` 是一个特殊的字典，用表单字段的 `name` 属性值可以获取用户填入的对应数据：

2. flash消息

`flash()` 函数用来在视图函数里向模板传递提示消息，`get_flashed_messages()` 函数则用来在模板中获取提示消息。

`flash()` 函数在内部会把消息存储到 Flask 提供的 `session` 对象里。`session` 用来在请求间存储数据，它会把数据签名后存储到浏览器的 Cookie 中，所以我们需要设置签名所需的密钥

3. 重定向

根据验证情况，我们发送不同的提示消息，最后都把页面重定向到主页，这里的主页 URL 均使用 `url_for()` 函数生成：

### 编辑现有数据

```python
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
```

1. 单开一个页面查询

我们要编辑某个条目，那么必然要在输入框里提前把对应的数据放进去，以便于进行更新。在模板里，通过表单 `<input>` 元素的 `value` 属性即可将它们提前写到输入框里

*templates/edit.html：编辑页面模板*

```html
{% extends 'base.html' %}

{% block content %}
<h3>Edit item</h3>
<form method="post">
    Name <input type="text" name="title" autocomplete="off" required value="{{ movie.title }}">
    Year <input type="text" name="year" autocomplete="off" required value="{{ movie.year }}">
    <input class="btn" type="submit" name="submit" value="Update">
</form>
{% endblock %}
```

*index.html：编辑电影条目的链接*

```html
<span class="float-right">
    <a class="btn" href="{{ url_for('edit', movie_id=movie.id) }}">Edit</a>
    ...
</span>
```

2. 查询现有数据

`movie_id` 变量是电影条目记录在数据库中的主键值，这个值用来在视图函数里查询到对应的电影记录。查询的时候，我们使用了 `get_or_404()` 方法，它会返回对应主键的记录，如果没有找到，则返回 404 错误响应。

### 编辑现有数据——传参逻辑

在`index.html`的按钮中，在url中传入movie_id

在`app.py`对应的视图函数`edit(movie_id)`中，通过url的传入movie_id，设定参数`movie = Movie.query.get_or_404(movie_id)`，最后返回`render_template('edit.html', movie=movie)`

将movie传入`edit.html`，从而可以在输入框中默认显示原来的表单值`value="{{ movie.year }}">`

> 由此可以知道，app.py的视图函数负责了网页的处理与网页的传参。起到了传递和处理作用

### 删除

*app.py：删除电影条目*

```
@app.route('/movie/delete/<int:movie_id>', methods=['POST'])  # 限定只接受 POST 请求
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)  # 获取电影记录
    db.session.delete(movie)  # 删除对应的记录
    db.session.commit()  # 提交数据库会话
    flash('Item deleted.')
    return redirect(url_for('index'))  # 重定向回主页
```

为了安全的考虑，我们一般会使用 POST 请求来提交删除请求，也就是使用表单来实现（而不是创建删除链接）：

*index.html：删除电影条目表单*

```html
<span class="float-right">
    ...
    <form class="inline-form" method="post" action="{{ url_for('delete', movie_id=movie.id) }}">
        <input class="btn" type="submit" name="delete" value="Delete" onclick="return confirm('Are you sure?')">
    </form>
    ...
</span>
```

为了让表单中的删除按钮和旁边的编辑链接排成一行，我们为表单元素添加了下面的 CSS 定义：

```css
.inline-form {
    display: inline;
}
```
