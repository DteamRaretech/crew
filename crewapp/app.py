from flask import Flask, request, redirect, render_template, session, flash, abort
from util.DB import DB
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


#[サインアップページの表示]
@app.route('/signup')
def signup():
    return render_template('registation/signup.html')


#[サインアップ処理]

@app.route('/signup' , methods=['POST'])

def UserSignup()
    
    # フォームからサインアップ情報を取得
    username = request.form.get('name')
    email = request.form.get('email')
    password1 = request.form.get('password1')
    password2 = request.form.get('password2')

    # email正規表現
    regex = '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

    # 入力内容エラーチェック
    if username == '' or email == '' or password1 == '' or password2 == '' :
        flash('入力は必須です')
    elif re.match(regex, email) is None :
        flash('you@example.com の形式で入力してください')
    elif password1 != password2 :
        flash('パスワードが一致しません')
    else :
        uid = uuid.uuid4()
        password = hashlib.sha256(password1.encode('utf-8')).hexdigest()

    # usersテーブル重複チェック準備

    def GetUser(email)
        try:
            connection = DB.getConnection()
            cursor = connection.cursor()
            sql = 'SELECT * FROM users WHERE email=%s;'
            cursor.execute(sql, (email))
            user = cursor.fetchone()
            return user 
        except Exception as e:
            print(e + 'が発生しています')
            return render_template('registation/error.html')
        finally:
            cursor.close()
    
    # usersテーブルINSERT準備

    def InsertUser(uid, username, email, password1)
        try:
            connection = DB.getConnection()
            cursor = connection.cursor()
            sql = 'INSERT INTO users (uid, username, email, password1) VALUES (%S, %S, %S, %S);'
            cursor.execute(sql, (uid, username, email, password1))
            connection.commit() 
        except Exception as e:
            print(e + 'が発生しています')
            return render_template('registation/error.html')
        finally:
            cursor.close()

        DBuser = GetUser(email)

        if DBuser != None:
            flash('同一ユーザが登録されています')
        else :
            InsertUser(uid, username, email, password1) 
            UserID = str(uid)
            session['uid'] = UserID
            return redirect('/')
        
    return redirect('/signup')


#ログイン・ログアウト処理

#googleAPI連携

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
