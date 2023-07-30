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
            flash('同一ユーザが登録されています')
        else : #usersテーブルにINSERT
            dbConnect.createUser(uid, user_name, email, password) 
            UserID = str(uid)
            session['uid'] = UserID
            return redirect('/')
    return redirect('/signup')


#ログイン・ログアウト処理

#googleAPI連携

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
