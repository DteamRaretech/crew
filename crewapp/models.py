# データベースを操作する関数をmodels.pyにまとめる
# from モジュール import クラス で、クラスメソッドを呼び出せる状態にする

import pymysql # pymysqlライブラリを取り込む
from util.DB import DB # util.DB から DBクラスを取り込む

# pymysqlと接続後、各sqlを実行するクラスを宣言
class dbConnect:
        
    #関数：create usersテーブル 
    def createUser(uid, user_name, email, password): #サインアップ処理
        try: 
            connection = DB.getConnection() #DBに接続する
            cursor = connection.cursor() #mysqlからカーソル作成、sqlを実行可能にする
            sql = "INSERT INTO users (uid, user_name, email, password) VALUES (%s, %s, %s, %s);" #カラムuid, user_name, email, passwordをINSERT
            cursor.execute(sql, (uid, user_name, email, password)) #SQLを実行
            connection.commit() #結果の確定
        except Exception as e: #コネクション関係の問題の基底クラスを指定し、例外処理
            print(e + 'が発生しています')
            abort(500)
        finally:
            cursor.close() # コネクタをクローンし全ての処理が完了



    #関数：read usersテーブル
    def getUser(email): #ユーザ参照(email基準)
        try:
            connection = DB.getConnection() #DBに接続する
            cursor = connection.cursor() #mysqlからカーソル作成、sqlを実行可能にする
            sql = "SELECT * FROM users WHERE email=%s;" #usersテーブルからデータ取得(email基準)
            cursor.execute(sql, (email)) #SQLを実行
            user = cursor.fetchone() #抽出データ1件をuserに格納
            return user
        except Exception as e: #コネクション関係の問題の基底クラスを指定し、例外処理
            print(e + 'が発生しています')
            abort(500)
        finally:
            cursor.close() # コネクタをクローンし全ての処理が完了


    #関数：create channelsテーブル


    #関数：read channelsテーブル


    #関数：update channelsテーブル


    #関数：delete channelsテーブル


    #関数：create messagesテーブル


    #関数：read messagesテーブル


    #関数：update messagesテーブル


    #関数：delete messagesテーブル


    #関数：create todoテーブル


    #関数：read todoテーブル


    #関数：update todoテーブル


    #関数：delete todoテーブル

