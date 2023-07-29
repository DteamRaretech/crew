# モジュールを読み込む
import pymysql

# pymysqlと接続するクラスを宣言
class DB:

    # pymysqlと接続する関数を作成…クラス内で作成した関数をmethodと呼ぶ

    def getConnection():
        try: # connect()関数でpymysqlに接続する。以下、接続開始のために使用する引数を指定
            connection = pymysql.connect(
                host="db" , # MySQL サーバーのホスト名または IP アドレス
                database="crewapp" , # MySQL サーバーに接続するときに使用するデータベース名
                user="testuser" , # MySQL サーバーでの認証に使用されるユーザー名
                password="testuser" , # MySQL サーバーでユーザーを認証するためのパスワード
                charset="utf8" , # 使用する MySQL 文字セット

                # Select結果をtupleではなくdictionary(連想配列)で受け取れるように指定
                # デフォルトではクエリの結果がtupleで返る…どんな順番で列が返ってくるのかわからず扱いづらいため
                cursorclass=pymysql.cursors.DictCursor
            )
            return connection
        
        except (ConnectionError): # コネクション関係の問題の基底クラスを指定し、例外処理
            print("データベース:crewappとの接続に失敗しました")
            connection.close() # ファイルを閉じる
