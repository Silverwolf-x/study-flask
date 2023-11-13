# flask学习记录

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
