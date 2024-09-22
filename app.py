from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.secret_key = 'your_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)

# 存储用户和帖子数据（在内存中）
users = {}
posts = []

class User(UserMixin):
    def __init__(self, username, password):
        self.id = username
        self.username = username
        self.password = password

# 加载用户
@login_manager.user_loader
def load_user(user_id):
    return users.get(user_id)

# 主页面
@app.route('/')
def index():
    return render_template('index.html', posts=posts, current_user=current_user)

# 注册用户
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username in users:
            flash('用户名已被注册！')
        else:
            new_user = User(username=username, password=password)
            users[username] = new_user
            flash('注册成功！')
            return redirect(url_for('login'))
    return render_template('register.html')

# 用户登录
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = users.get(username)
        if user and user.password == password:
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('用户名或密码错误！')
    return render_template('login.html')

# 用户登出
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# 发帖
@app.route('/post', methods=['POST'])
@login_required
def post():
    title = request.form.get('title')
    content = request.form.get('content')
    new_post = {
        'title': title,
        'content': content,
        'author': current_user.username,
        'replies': []  # 初始化为回复列表
    }
    posts.append(new_post)
    return redirect(url_for('index'))

# 回复帖子
@app.route('/reply/<int:post_id>', methods=['POST'])
@login_required
def reply(post_id):
    reply_content = request.form.get('reply_content')
    if post_id < len(posts):
        replies_list = posts[post_id]['replies']
        replies_list.append({'content': reply_content, 'author': current_user.username})
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)  # 设置host和port以在Replit等平台上正确运行
