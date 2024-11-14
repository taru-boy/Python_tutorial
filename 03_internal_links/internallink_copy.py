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

    internal_links = set()  # 空のセットを用意
    anl_url = "https://hashikake.com/RegEx"  # 内部リンクを調べたいURL

    parsed_url = urlparse(anl_url)
    scheme = parsed_url.scheme
    base_domain = parsed_url.netloc

    # scheme（https）と netloc（hashikake.com）を結合してベースURLを作成
    base_url = f"{scheme}://{base_domain}/"

    # 内部リンクの取得
    internal_links = get_links(
        anl_url=anl_url,
        internal_links=internal_links,
        base_url=base_url,
        base_domain=base_domain,
    )

    if internal_links:  # 内部リンクが存在するなら
        print(f"全内部リンク数：{len(internal_links)}個")  # 内部リンクの数を表示
        print(internal_links)  # 内部リンクの表示
        # 関数内で使われるshort_linksを定義
        short_links = shape_url(
            internal_links=internal_links, base_url=base_url, base_domain=base_domain
        )  # 内部リンクとして価値の薄いものの除外
        print(
            f"高価値内部リンク数：{len(short_links)}個"
        )  # 内部リンクとして価値が高いものの数を表示
        show_network(links=short_links)
    else:
        print("内部リンクはありませんでした。")
        sys.exit()  # 内部リンクが存在しない場合はプログラムの終了


def get_links(
    anl_url: str,
    internal_links: set,
    base_url: str,
    base_domain: str,
) -> set:
    """
    /で始まるものと、base_urlから始まるもの//ドメインから始まるもの
    全ての内部リンクを取得して、重複を除去してpagesに収集する+内部リンク数を出力

    Parameters
    ----------
    anl_url : str
        調べたいURL
    internal_links : set
        内部リンクの集合
    base_url : str
        ベースのURL
    base_domain : str
        ベースのドメイン

    Returns
    -------
    set
        調べたいURL内のリンクが追加された集合
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
        if link.get("href") not in internal_links:
            # セットの中に内部リンクとして追加
            internal_links.add(link.get("href"))
    return internal_links


def show_network(links: set) -> None:
    """
    調査URLを中心としたネットワーク図の作成

    Parameters
    ----------
    links : set
        内部リンクの集合
    """

    # セットをリストにする
    links = list(links)
    # indexの0に文字列"start_url"を追加
    links.insert(0, "start_url")
    # 空のグラフの作成　有向グラフ
    G = nx.DiGraph()
    # リストの最初の要素を中心として放射状に頂点と辺の追加
    nx.add_star(G, links)
    # レイアウトを決める スプリングレイアウト
    pos = nx.spring_layout(G, k=0.3)
    # ノードの様式の決定
    nx.draw_networkx_nodes(G, pos, node_size=300, node_color="c", alpha=0.6)
    # ラベル文字の様式の決定
    nx.draw_networkx_labels(G, pos, font_size=10, font_family="DejaVu Sans")
    # エッジの様式の決定
    nx.draw_networkx_edges(G, pos, alpha=0.4, edge_color="c")

    # matplotlibの座標軸の非表示
    plt.axis("off")
    # matplotlibによる図の描画
    plt.show()


def shape_url(internal_links: set, base_url: str, base_domain: str) -> set:
    """
    URLのhttp://を省略してネットワーク図を見やすくするための調整
    privacyページやcontactページなどの無駄な内部リンクページの除去

    Parameters
    ----------
    internal_links : set
        内部リンクの集合
    base_url : str
        ベースのURL
    base_domain : str
        ベースのドメイン

    Returns
    -------
    set
        整形されたURLの集合
    """
    temp_links = []
    # 内部リンクのURLから効果の薄い内部リンクをre.sub()で消していく base_url https://hashikake.com //hashikake.com
    for url in internal_links:
        rel_path = re.sub(
            rf"^{base_url}|^//{base_domain}|.*tag.*|.*feed.*|.*about.*", "", url
        )
        # short_links（空のリスト）に追加
        temp_links.append(rel_path)
        # short_linksをセットに変更(重複の削除)
        short_links = set(temp_links)
        # ""を削除　# discardだとキーがなくてもエラーにはならない。removeだとエラーになる
        short_links.discard("")
    return short_links


if __name__ == "__main__":
    main()
