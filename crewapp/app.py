from flask import Flask, request, redirect, render_template, session, flash, abort
from models import dbConnect
from datetime import timedelta
import hashlib
import uuid
import re


app = Flask(__name__)
app.secret_key = uuid.uuid4().hex
app.permanent_session_lifetime = timedelta(days=30)


#TODO一覧画面表示
@app.route('/todo')
def show_todo():
    uid = uuid.uuid4()
    #print("show_uid",uid,type(uid))
    todos = dbConnect.getTodoIds(str(uid))
    print(todos[0])
    return render_template('registation/todolist_sample.html',todo_list = todos[0])
    #return render_template('registation/todolist_sample.html')

#TODO受け取り
@app.route('/todo', methods=['POST'])
def write_todo():

    todo_list = []

    uid = uuid.uuid4()
    # todoの内容をhtmlより取得する
    title = request.form.get('title')
    detail = request.form.get('detail')
    fixed_date = request.form.get('fixed_date')
    
    todo_list.append([title,title,fixed_date])
    # todoの内容をデータベースに書き込む
    ## ダミーデータ
    dbConnect.createTodo(uid,title,detail,fixed_date,1) 
    #print("todo_list",todo_list)
    #return render_template('registation/todolist_sample.html',todo_list = todo_list)
    return render_template('registation/todolist_sample.html')



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
                return redirect('/')
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
#POST(Webサーバに送る値を見えないところにくっつけて送るやり方、「このデータをやるから追加して」のお願い)
#GET(Webサーバに送る値をURLにくっつけて送るやり方、「このページをくれ」のお願い) 両方を許可
@app.route('/addchannel', methods=['POST','GET'])
def createChannels():

    uid = session.get('uid')

    if uid is None:
        return redirect('/login') #セッション切れの場合、再ログイン
    if request.method == 'GET':
        return render_template('modal/add-channel.html') #GETメソッドの場合、add-channel.html表示


    # add-channelフォームから入力情報取得
    name = request.form.get('channelTitle')
    abstract = request.form.get('channelDescription')
    dbChannelsName = dbConnect.getChannelsName(name) #channelTitleと一致するchannelsデータをDBから取得

    if dbChannelsName != None: # add-channelフォームで入力したチャンネル名と、一致するチャンネルが既にある時
            error_message = '同名のチャンネルが作成されています'
            return render_template('error/error.html', error_message=error_message)
    else:
        dbConnect.createChannels(uid, name, abstract)
        return redirect('/') #成功時にホーム画面を呼び出す


#チャンネル更新
#POST(Webサーバに送る値を見えないところにくっつけて送るやり方、「このデータをやるから追加して」のお願い)
#GET(Webサーバに送る値をURLにくっつけて送るやり方、「このページをくれ」のお願い) 両方を許可


@app.route('/updatechannel/<cid>', methods=['POST','GET'])
def updateChannels(cid):

    uid = session.get('uid')

    if uid is None:
        return redirect('/login') #セッション切れの場合、再ログイン
    if request.method == 'GET':
        return render_template('modal/update-channel.html', cid = cid) #GETメソッドの場合、update-channel.html表示

    # update-channelフォームから入力情報取得
    name = request.form.get('channelTitle')
    abstract = request.form.get('channelDescription')
    id = request.form.get('cid')

    #更新中のchannelsのnameを基準に、DBデータを取得
    dbChannelsId = dbConnect.getChannelsId(id)
    dbChannelsName = dbConnect.getChannelsName(name) 

    #エラーチェック
    if dbChannelsId['uid'] != uid: #channels作成者≠ログインユーザの時        
        error_message = 'チャンネルは作成者のみ編集可能です'
        return render_template('error/error.html', error_message=error_message)
    elif dbChannelsName != None:  # update-channelフォームで入力したチャンネル名と、一致するチャンネルが既にある時
        error_message = '同名のチャンネルが作成されています'
        return render_template('error/error.html', error_message=error_message)
    else:
        dbConnect.updateChannels(uid, name, abstract, id)
        return redirect('/detail/{cid}'.format(cid = id))
    

#チャンネル削除 URLの部分に<>で囲む変数を表記することで、ユーザーから引数をもらうことができる。
@app.route('/delete/<cid>') #フロントから送られてきたURLの<cid>部分を引数として使う
def deleteChannels(cid): #URLの<cid>をdeleteChannels関数に引数として渡す

    uid = session.get('uid')

    if uid is None:
        return redirect('/login') #セッション切れの場合、再ログイン

    # delete-channelフォームから削除対象チャンネル取得
    id = cid 

    #削除対象のchannelsのidを基準に、DBデータを取得
    dbChannelsId = dbConnect.getChannelsId(id)

    #エラーチェック
    if dbChannelsId['uid'] != uid: #channels作成者≠ログインユーザの時
        error_message = 'チャンネルは作成者のみ削除可能です'
        return render_template('error/error.html', error_message=error_message)
    else:
        dbConnect.deleteChannels(id)
        return redirect('/')


#メッセージ投稿画面表示
@app.route('/detail/<cid>')
def detail(cid):

    uid = session.get("uid")    
    if uid is None:
        return redirect('/login')

    cid = cid   
    channel = dbConnect.getChannelsId(cid)
    messages = dbConnect.getMessageALL(cid)

    return render_template('registation/detail.html', messages=messages, channel=channel, uid=uid)
        
#メッセージ投稿
@app.route('/message', methods=['POST'])
def add_message():

    uid = session.get("uid")
    if uid is None:
        return redirect('/login')
    
    message = request.form.get('message')
    cid = request.form.get('cid')

    if message:
        dbConnect.createMessages(uid,cid,message)

    return redirect('/detail/{cid}'.format(cid = cid))


#メッセージ更新(サンプル＋α)


#メッセージ削除
@app.route('/delete_message', methods=['POST'])
def delete_message():

    uid = session.get("uid")
    if uid is None:
        return redirect('/login')
    
    message_id = request.form.get('message_id')
    cid = request.form.get('cid')

    if message_id:
        dbConnect.deleteMessage(message_id)

    return redirect('/delete/{cid}'.format(cid = cid)) 





#TODO作成


#TODO更新


#TODO削除


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
