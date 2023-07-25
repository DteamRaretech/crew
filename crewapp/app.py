from flask import Flask
app = Flask(name)

@app.route('/')
def hello_world():
    return 'Hello, World!'

#サインアップ処理

#ログイン・ログアウト処理

#googleAPI連携
print("hello")

if name == 'main':
    app.run(debug=True)
