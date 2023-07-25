# データベースを操作する関数をmodels.pyにまとめる
# from モジュール import クラス で、クラスメソッドを呼び出せる状態にする

import pymysql.cursors # pymysqlライブラリを取り込む
from util.DB import DB # util.DB から DBクラスを取り込む

# pymysqlと接続後、各sqlを実行するクラスを宣言
class dbConnect:

        # 各sqlを実行する関数を作成…クラス内で作成した関数をmethodと呼ぶ