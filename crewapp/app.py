from flask import Flask, request, redirect, render_template, session, flash, abort
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'


# サインアップページの表示
@app.route('/signup')
def signup():
    return render_template('registation/signup.html')

#サインアップ処理

#ログイン・ログアウト処理

#googleAPI連携

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
