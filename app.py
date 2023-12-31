from flask import Flask, jsonify
from flask import render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required, current_user
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from create.createimg import createimg
import datetime

# パスワードの非表示化と確認機能のインポート
from werkzeug.security import generate_password_hash, check_password_hash
import os

# 画像の保存のためのライブラリ
from PIL import Image
import io
import base64

# インスタンス化
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///admin.db'
# ランダムなシークレットキーの作成
app.config['SECRET_KEY'] = os.urandom(24)
# アプリにデータベースを紐づけ
db = SQLAlchemy(app)

# ログインマネージャのインスタンス化
login_manager = LoginManager()
# アプリにログイン機能を紐づけ
login_manager.init_app(app)

#databaseの作成

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(30), nullable=True)
    title = db.Column(db.String(50), nullable=True)
    body = db.Column(db.String(500), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    image = db.Column(db.String(1000), nullable=True) # 追加したカラム、生成した画像を保存する


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=True)
    password = db.Column(db.String(12), nullable=True)

# 下記にデコレーターによるセキュリティ強化があるが、その実施に必要なコード    
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ゲストページ
@app.route('/', methods=['GET','POST'])
def guest():
    if request.method == 'GET':
        # Postに保存されている全てのデータの取得
        posts = Post.query.all()
        return render_template('guest.html', posts=posts)

@app.route('/home', methods=['GET','POST'])
@login_required
def home():
    if request.method == 'GET':

        name=current_user.username
        #Post/Userに保存されている全てのデータの取得
        posts = Post.query.all()
        users = User.query.all() 
        myposts = Post.query.filter_by(author=name) 
        
        # Postの著者名を取得してhomeに転送
        return render_template('home.html', posts=posts, users=users, name=name, myposts=myposts )
 
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        signupname = request.form.get('username')
        signuppassword = request.form.get('password')
        error = ""
        users = User.query.all()  # Userテーブルの全ての行を取得
        usernames = [user.username for user in users]  # 各行のusername,password属性の値をリストとして取得
        passwords = [user.password for user in users]

        # ユーザー名かパスワードが誰かと被ってしまった場合は、サインインが出来ないようにする
        # パスワードに関しては自動で生成しているので、UI側では被っても大丈夫
        if (signuppassword in passwords) or (signupname in usernames) :
            # エラー文
            error = "ユーザー名,又はパスワードが被ってしまいました。別の物を入力してください。"
            return render_template('signup.html', error=error)

        else:
            user = User(username=signupname, password=generate_password_hash(signuppassword, method='sha256')) 
            #入れたデータを保存
            db.session.add(user)
            #保存されたデータに変更
            db.session.commit()
            #login.htmlに移動
            return redirect('/login')
    
    else:
        return render_template('signup.html')
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        error = ""
        # Userのデータベースから合致する名前を探す。
        user = User.query.filter_by(username=username).first() 

        # 存在しないユーザーであればエラーを返す
        if user is None or not check_password_hash(user.password, password):
            # usernameまたはpasswordが誤っている旨のflashを表示
            error = 'Invalid username or password'
            # loginページへリダイレクト
            return render_template('login.html', error=error)
        
        # 探し出されたユーザー名のパスワードと入力されたパスワードが同じならば
        if check_password_hash(user.password, password):
             # importしたlogin_userを用いてログインする
            login_user(user)
            # トップページに移動する
            return redirect('/home')

    else:
        return render_template('login.html')
    
@app.route('/logout')
# デコレーターの設定により、ログインしているユーザーのみアクセス出来るようにセキュリティ
@login_required
def logout():
    logout_user()
    return redirect('/login')

@app.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    #新しい投稿がされたなら、createのform内のname=title,bodyを取得する
    if request.method == 'POST':
        author = current_user.username
        title = request.form.get('title')
        body = request.form.get('body')

        # 画像を生成
        createimg(body)

        # PNG画像を読み込む,createimg.pyとほぼ同時刻で作成されるの
        def imageread():
            late_time_min = 0
            now = datetime.datetime.now()
            # 画像生成と読み込みのラグをPC間で共通して修正
            while True:
                late_time_min += 1
                try:
                    now = datetime.datetime.now() - datetime.timedelta(seconds=late_time_min)
                    image = Image.open(f"create/createimg/create_image_{now.strftime('%Y%m%d%H%M%S')}.png")
                except FileNotFoundError:
                    continue
                
                break

            return image

        # 画像をバイナリデータに変換
        byte_array = io.BytesIO()
        imageread().save(byte_array, format="PNG")
        image_binary = byte_array.getvalue()

        # 画像をBase64形式に変換
        base64_data = base64.b64encode(image_binary).decode('utf-8')


        #取得したデータをデータベースに入れる
        post = Post(author=author, title=title, body=body, image=base64_data) 
        #入れたデータを保存
        db.session.add(post)
        #保存されたデータに変更
        db.session.commit()
        #変更されたらトップページに戻る
        return redirect('/home')
    else:
        return render_template('create.html')

@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    if request.method == 'GET':
        name = current_user.username
        posts = Post.query.all()
        return render_template('search.html', name=name, posts=posts)

    if request.method == 'POST':
        search_query = request.form.get('search_query')
        name = current_user.username
        if search_query:
            search_results = Post.query.filter(
                db.or_(Post.title.ilike(f'%{search_query}%'), Post.body.ilike(f'%{search_query}%'))
            ).all()
            return render_template('search.html', name=name, search_query=search_query, search_results=search_results)
        else:
            posts = Post.query.all()
            return render_template('search.html', name=name, posts=posts)

# index.htmlのa href="/{{post.id}}/update"からidを受取り、可変型のルーティングで取得する
@app.route('/<int:id>/update', methods=['GET','POST'])
@login_required
def update(id):
    # postのインスタンス化 idをURLに入れておく
    post = Post.query.get(id)
    if request.method == 'GET':
        return render_template('update.html', post=post)
    else:
        # インスタンス化されたpostに上書きする
        post.title = request.form.get('title')
        post.body = request.form.get('body')

        # 更新
        db.session.commit()
        return redirect('/home')

@app.route('/<int:id>/delete', methods=['GET'])
@login_required
def delete(id):
    # postのインスタンス化
    post = Post.query.get(id)
    
    db.session.delete(post)
    db.session.commit()
    return redirect('/home')

@app.route('/<int:id>/zoom', methods=['POST','GET'])
def zoom(id):
    if request.method == 'GET':
        post = Post.query.get(id)
        return render_template('zoom.html', post=post)
    else:
        post = Post.query.get(id)
        data = request.get_json()
        if 'count' in data:
            count = data['count']
            if post:
                post.goodcount += count + 1  # カウントの値を加算
                db.session.commit()  # データベースに変更を保存
            else:
                return jsonify({"message": f"Post with ID {id} not found."}), 404
        else:
            return jsonify({"message": "Invalid request data: count not provided."}), 400
        return render_template('home.html', post=post)

@app.cli.command('initdb')
def initdb_command():
    db.create_all()
    
if __name__ == "__main__":
    app.run()

# アドミン画面の実装（データベース操作の簡素化）
class MicroadminModelView(ModelView):
    can_view_details = True
    page_size = 50  # the number of entries to display on the list view
    can_export = True
    create_modal = True
    edit_modal = True

admin = Admin(app, name='microadmin', template_mode='bootstrap3')
admin.add_view(MicroadminModelView(Post, db.session))
admin.add_view(MicroadminModelView(User, db.session))