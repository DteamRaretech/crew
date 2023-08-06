from flask import Flask, request, redirect, render_template, session, flash, abort
from models import dbConnect
from datetime import timedelta
import hashlib
import uuid
import re


app = Flask(__name__)
app.secret_key = uuid.uuid4().hex
app.permanent_session_lifetime = timedelta(days=30)


@app.route('/')
def hello_world():
    return 'Hello, World!'


#サインアップページの表示
@app.route('/signup')
def signup():
    return render_template('registation/signup.html')


#サインアップ処理

@app.route('/signup' , methods=['POST'])

def UserSignup():
    
    #フォームからサインアップ情報を取得
    user_name = request.form.get('name')
    email = request.form.get('email')
    password1 = request.form.get('password1')
    password2 = request.form.get('password2')

    """
    print(user_name, email, password1, password2)
    """
    
    #email正規表現
    regex = '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

    #入力内容エラーチェック
    if user_name == '' or email == '' or password1 == '' or password2 == '' :
        flash('入力は必須です')
    elif password1 != password2 :
        flash('パスワードが一致しません')
    elif re.match(regex, email) is None :
        flash('you@example.com の形式で入力してください')
    else :
        uid = uuid.uuid4()
        password = hashlib.sha256(password1.encode('utf-8')).hexdigest()
        DBuser = dbConnect.getUser(email)

        if DBuser != None:
            flash('同一ユーザーが登録されています')
        else : #usersテーブルにINSERT
            dbConnect.createUser(uid, user_name, email, password) 
            UserID = str(uid)
            session['uid'] = UserID
            return redirect('/') #成功時にホーム画面を呼び出す
    return redirect('/signup') #ログイン失敗時、/signupにリダイレクト


#ログイン・ログアウト処理

# ログインページの表示
@app.route('/login')
def login():
    return render_template('registation/login.html')

# ログイン処理
@app.route('/login', methods=['POST'])

#フォームからログインのために入力された情報を取得
def userLogin():
    email = request.form.get('email')
    password = request.form.get('password')
#ログイン不成立のパターンが書かれている
    if email == '' or password == '':
        flash('空のフォームがあります')
    else:
        user = dbConnect.getUser(email)
        if user is None:
            flash('このユーザーは登録されていません')
        else:
            hashPassword = hashlib.sha256(password.encode('utf-8')).hexdigest()
            if hashPassword != user["password"]: #[]…userオブジェクトに格納されたpasswordを呼び出す辞書の文法 ()…user関数に引数を渡すの意味
                flash('パスワードが間違っています！')
#ログイン成立時、sessionにuser情報を格納し、ホーム画面を呼び出す
            else:
                session['uid'] = user["uid"]
                return render_template('registation/index.html')
##仮にログインに失敗した際、入力した値がフォームに残るようにしたい。
    return redirect('/login')         

# ログアウト
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')


#googleAPI連携


#チャンネル一覧画面表示(ホーム画面)


#チャンネル作成


#チャンネル更新


#チャンネル削除


#メッセージ投稿画面表示


#メッセージ投稿


#メッセージ更新(サンプル＋α)


#メッセージ削除


#TODO一覧画面表示


#TODO作成


#TODO更新


#TODO削除


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
