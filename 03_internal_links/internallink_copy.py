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


def main():
    """
    メインの実行部分:調べたいURLはanl_urlに入力する
    """

    pages = set()  # 空のセットを用意
    anl_url = "https://hashikake.com/RegEx"  # 内部リンクを調べたいURL

    parsed_url = urlparse(anl_url)
    scheme = parsed_url.scheme
    base_domain = parsed_url.netloc

    # scheme（https）と netloc（hashikake.com）を結合してベースURLを作成
    base_url = f"{scheme}://{base_domain}/"

    # 内部リンクの取得

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
    pattern = rf"^({base_url}.*)|^(/[^/].*?)|^(//{base_domain}.*)"
    # re.compileによる正規表現パターンの生成
    # URLにGETリクエストを送る
    response = requests.get(anl_url)
    # BeautifulSoupによるsoupの作成
    soup = BeautifulSoup(response.content, "html.parser")
    # URLがパターンに一致するaタグを取得
    for link in soup.find_all("a", href=re.compile(pattern)):
        # aタグの中からURLを取得
        link.get("href")
        # セットの中にリンクが入っていないことを確認
        if link.get("href") not in pages:
            # セットの中に内部リンクとして追加
            pages.add(link.get("href"))

    """
    調査URLを中心としたネットワーク図の作成
    """

    # セットをリストにする
    pages = list(pages)
    # indexの0に文字列"start_url"を追加
    pages.insert(0, "start_url")
    # 空のグラフの作成　有向グラフ
    G = nx.DiGraph()
    # リストの最初の要素を中心として放射状に頂点と辺の追加
    nx.add_star(G, pages)
    # レイアウトを決める スプリングレイアウト
    pos = nx.spring_layout(G, k=0.3)
    # ノードの様式の決定

    # ラベル文字の様式の決定

    # エッジの様式の決定

    nx.draw_networkx(G, pos)

    # matplotlibの座標軸の非表示
    plt.axis("off")
    # matplotlibによる図の描画
    plt.show()
    """
    URLのhttp://を省略してネットワーク図を見やすくするための調整
    privacyページやcontactページなどの無駄な内部リンクページの除去
    """

    # 内部リンクのURLから効果の薄い内部リンクをre.sub()で消していく base_url https://hashikake.com //hashikake.com

    # short_links（空のリスト）に追加

    # short_linksをセットに変更(重複の削除)

    # ""を削除　# discardだとキーがなくてもエラーにはならない。removeだとエラーになる


if __name__ == "__main__":
    main()
