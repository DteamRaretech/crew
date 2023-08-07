from flask import Flask, request, redirect, render_template, session, flash, abort
from models import dbConnect
from datetime import timedelta
import hashlib
import uuid
import re


app = Flask(__name__)
app.secret_key = uuid.uuid4().hex
app.permanent_session_lifetime = timedelta(days=30)

"""
@app.route('/')
def hello_world():
    return 'Hello, World!'
"""

#TODO一覧画面表示
@app.route('/todo')
def show_todo():
    return render_template('registation/todolist.html')


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
@app.route('/')
def index():
    uid = session.get('uid')
    if uid is None:
        return redirect('/login') #セッション切れの場合、再ログイン
    else:
        channels = dbConnect.getChannelsAll() #channels全件取得
        channels.reverse() #リストを逆順で取り出す…リスト型メソッドのためリストオブジェクト.reverse()と記述
    return render_template('registation/index.html', channels=channels, uid=uid) 
    #render_template()…値を渡して動的にテンプレートの表示を変更する
    #フロント.index.htmlの変数channelsに、バック.def index()のchannelsを渡す
    #フロント.index.htmlの変数uidに、バック.def index()のuidを渡す
    #フロント.constは再代入ができない変数、該当の変数は{}内の処理でのみ呼び出し可能
    #フロント. const y = {{x|tojson}} …x:Python側から受け取った変数 y:受け取ったxをJavaScript側で置き換えた後の変数


#チャンネル作成
@app.route('/', methods=['POST'])
def createChannels():

    uid = session.get('uid')
    if uid is None:
        return redirect('/login') #セッション切れの場合、再ログイン
    
    # add-channelフォームから入力情報取得
    name = request.form.get('channelTitle')
    abstract = request.form.get('channelDescription')
    dbChannelsName = dbConnect.getChannelsName(name) #channelTitleと一致するchannelsデータをDBから取得
    
    if dbChannelsName != None:
            error_message = '同名のチャンネルが作成されています'
            return render_template('error/error.html', error_message=error_message)
    else:
        dbConnect.createChannels(uid, name, abstract)
        return redirect('/') #成功時にホーム画面を呼び出す


#チャンネル更新
@app.route('/update_channel', methods=['POST'])

def updateChannels(uid, name, abstract, id):

    # update-channelフォームから入力情報取得
    uid = session.get('uid')
    name = request.form.get('channelTitle')
    abstract = request.form.get('channelDescription')
    id = request.form.get('cid')

    if uid is None:
        return redirect('/login') #セッション切れの場合、再ログイン
    else:
        dbChannelsId = dbConnect.getChannelsId(id) #更新中のchannelsのidを取得
        dbChannelsName = dbConnect.getChannelsName(name) #更新中のchannelsのnameを取得

        #エラーチェック
        if dbChannelsId['uid'] != uid:
            flash('チャンネルは作成者のみ編集可能です')
            return redirect ('/')
        elif dbChannelsName['name'] != None: 
            flash('同名のチャンネルが作成されています')
        else:
            dbConnect.updateChannels(uid, name, abstract, id)
            return redirect('/detail/{cid}'.format(cid = id))
    return redirect('/') #更新失敗時、ホーム画面にリダイレクト
    

#チャンネル削除


#メッセージ投稿画面表示


#メッセージ投稿


#メッセージ更新(サンプル＋α)


#メッセージ削除





#TODO作成


#TODO更新


#TODO削除


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
