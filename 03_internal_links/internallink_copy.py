# プログラム終了のためのsysのimport
import sys
# 正規表現を使うためのreをimport
import re
# HTTPリクエストを送るためのrequestsをimport
import requests
# BeautifulSoupをimport
from bs4 import BeautifulSoup
# URLからドメインを取得する為にurlparseをimport
from urllib.parse import urlparse
# ネットワーク図を作成する為にnetworkxをimport
import networkx as nx
# ネットワーク図を描画する為にmatplotlibをimport
import matplotlib.pyplot as plt

    """
    メインの実行部分:調べたいURLはanl_urlに入力する
    """

    # 空のセットを用意

    # 内部リンクを調べたいURL

    # https://またはhttp://からはじまる基準のホームページのURL

    # match_urlはマッチオブジェクトなので、そこからURLだけを取り出す

    # 正規表現で使うためにドメイン名の取得

    #　内部リンクの取得

    # 内部リンクが存在するなら

    # 内部リンクの数を表示

    # 内部リンクの表示

    # 関数内で使われるshort_linksを定義

    # 内部リンクとして価値の薄いものの除外

    # 内部リンクとして価値が高いものの数を表示

    # 内部リンクが存在しない場合はプログラムの終了



    """
    /で始まるものと、base_urlから始まるもの//ドメインから始まるもの
    全ての内部リンクを取得して、重複を除去してpagesに収集する＋
    内部リンク数を出力
    """
        
    # 正規表現の中で変数を使う時はf文字列またはformatを使う
    # /で始まって//を含まないURLと、https://ドメインから始まるもの、//ドメインから始まるもの

    # URLにGETリクエストを送る

    # BeautifulSoupによるsoupの作成

    # URLがパターンに一致するaタグを取得

    # re.compileによる正規表現パターンの生成

    # aタグの中からURLを取得

    # セットの中にリンクが入っていないことを確認

    # セットの中に内部リンクとして追加


    """
    調査URLを中心としたネットワーク図の作成
    """

    # セットをリストにする

    # indexの0に文字列"start_url"を追加

    #　空のグラフの作成　有向グラフ

    # リストの最初の要素を中心として放射状に頂点と辺の追加

    # レイアウトを決める スプリングレイアウト

    # ノードの様式の決定

    # ラベル文字の様式の決定

    # エッジの様式の決定

    # nx.draw_networkx(G, pos)

    # matplotlibの座標軸の非表示

    # matplotlibによる図の描画

    """
    URLのhttp://を省略してネットワーク図を見やすくするための調整
    privacyページやcontactページなどの無駄な内部リンクページの除去
    """    

    # 内部リンクのURLから効果の薄い内部リンクをre.sub()で消していく base_url https://hashikake.com //hashikake.com

    # short_links（空のリスト）に追加

    # short_linksをセットに変更(重複の削除)

    # ""を削除　# discardだとキーがなくてもエラーにはならない。removeだとエラーになる