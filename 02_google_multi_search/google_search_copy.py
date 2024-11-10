# ブラウザを自動操作するためseleniumをimport
from selenium import webdriver

# seleniumでヘッドレスモードを指定するためにimport
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By

# seleniumでEnterキーを送信する際に使用するのでimport
from selenium.webdriver.common.keys import Keys

# HTTPリクエストを送る為にrequestsをimport
import requests

# HTMLから必要な情報を得る為にBeautifulSoupをimport
from bs4 import BeautifulSoup

# グーグルスプレッドシートを操作する為にimport
import gspread

# グーグルスプレッドシートの認証情報設定の為にimport
from oauth2client.service_account import ServiceAccountCredentials
import time


# グーグルのURL
URL = "https://google.co.jp"
# グーグルのURLタイトルの確認のため
URL_TITLE = "Google"

# 2つのAPIを記述しないとリフレッシュトークンを3600秒毎に発行し続けなければならない
scope = ["https://spreadsheets.google.com.feeds", "https://googleapis.com/auth/drive"]

# 認証情報設定
# ダウンロードしたjsonファイル名をクレデンシャル変数に設定（秘密鍵、Pythonファイルから読み込みしやすい位置に置く）
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    "02_google_multi_search/starlit-water-441012-p8-cfc85334a56d.json"
)

# 共有設定したスプレッドシートキーを格納
SPREADSHEET_KEY = "1oTalR4C7N9V7lhsZhaktbda8fkz4hbzJkaKbam3ykpQ"


def main():
    """
    メインの処理
    Googleでキーワードを検索
    １ページ目の情報を取得し、Googleスプレッドシートに出力
    """

    # 検索キーワードが入力されたテキストファイルを読み込む
    with open("02_google_multi_search/keyword.txt") as f:
        keywords = [s.rstrip() for s in f.readlines()]

    # Options()オブジェクトの生成
    options = Options()
    # options.add_argument('--headless') # ヘッドレスモードを有効にする

    # ChromeのWebDriverオブジェクトを作成
    # executable need to be in pathというエラーが出た場合
    # chromedriverをpythonファイルと同じフォルダに置き、記述を下記のように変更
    # driver = webdriver.Chrome(options=options, executable_path="chromedriverのpathを書く")
    service = ChromeService("/usr/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=options)
    # Googleのトップページを開く
    driver.get(URL)
    # 2秒待機
    time.sleep(2)

    # Google検索処理
    for keyword in keywords:
        print(f"検索キーワード：{keyword}")
        search(driver=driver, keyword=keyword)
        items = get_info(driver=driver, keyword=keyword)

        for key in items:
            print(key)
            print(items[key])

        time.sleep(1200)
    # 情報取得処理

    # Googleスプレッドシート出力処理

    # ブラウザーを閉じる


def search(driver: webdriver.Chrome, keyword: str):
    """
    検索テキストボックスに検索キーワードを入力し、検索する。

    Parameters
    ----------
    driver : webdriver.Chrome
        Google ChromeのWebDriverインスタンス。
    keyword : str
        検索ボックスに入力するキーワード。

    Returns
    -------
    None
    """

    # 検索テキストボックスの要素をname属性から取得
    input_element = driver.find_element(By.NAME, "q")
    # 検索テキストボックスに入力されている文字列を消去
    input_element.clear()
    # 検索テキストボックスにキーワードを入力
    input_element.send_keys(keyword)
    # Enterキーを送信
    input_element.send_keys(Keys.RETURN)
    # 2秒待機
    time.sleep(1)


def get_info(driver: webdriver.Chrome, keyword: str) -> dict:
    """
    タイトル、URL、説明文、H1からH5までの情報を取得

    Parameters
    ----------
    driver : webdriver.Chrome
        Google ChromeのWebDriverインスタンス。
    keyword : str
        検索ボックスに入力するキーワード。

    Returns
    -------
    items : dict
        検索結果から取得した情報を格納した辞書。キーには以下の項目が含まれます:
        - "keyword" : 検索に使用したキーワード
        - "title" : 各ページのタイトルのリスト
        - "url" : 各ページのURLのリスト
        - "description" : 各ページの説明文のリスト
        - "h1", "h2", "h3", "h4", "h5" : 各ページの見出しタグ（H1～H5）のリスト
    """
    # 辞書を使って複数のアイテムを整理 -> 引数が減る＋返り値が減る
    items = {
        "keyword": str(keyword),
        "title": ["title"],
        "url": [],
        "description": ["説明文"],
        "h1": [],
        "h2": [],
        "h3": [],
        "h4": [],
        "h5": [],
    }
    # seleniumによる検索結果のurlの取得
    urls = driver.find_elements(
        By.CSS_SELECTOR,
        "div.kb0PBd.A9Y9g.jGGQ5e > div > div > span > a",
    )
    if urls:
        for url in urls:
            items["url"].append(str(url.get_attribute("href")).strip())

    # seleniumによるtitleの取得
    titles = driver.find_elements(
        By.CSS_SELECTOR, "div.kb0PBd.A9Y9g.jGGQ5e > div > div > span > a > h3"
    )
    if titles:
        for title in titles:
            items["title"].append(title.text.strip())

    # seleniumによるdescription（説明文）の取得
    descriptions = driver.find_elements(
        By.CSS_SELECTOR,
        "div.kb0PBd.A9Y9g > div.VwiC3b.yXK7lf.p4wth.r025kc.hJNv6b.Hdw6tb > span",
    )

    if descriptions:
        for description in descriptions:
            if "LEwnzc" not in description.get_attribute("class"):  # 日付タグを除外
                items["description"].append(description.text.strip())

    # h1?h5見出しの取得
    for url in items["url"]:
        try:
            # URLにGETリクエストを送る
            response = requests.get(url=url)  # GETリクエスト

        except requests.exceptions.SSLError:  # SSlエラーが起こった時の処理を記入
            response = requests.get(url=url, verify=False)

        soup = BeautifulSoup(
            response.text, "html.parser"
        )  # HTMLから情報を取り出す為にBeautifulSoupオブジェクトを得る
        time.sleep(1)  # 1秒待機

        heading_tags = ["h1", "h2", "h3", "h4", "h5"]
        for tag in heading_tags:
            # 指定された見出しタグの中身をheading_elemensとして取得
            heading_elements = soup.find_all(tag)
            heading_texts = []
            for element in heading_elements:
                if element.get_text().strip():
                    # heading_elementsからテキストを取得してheading_textsに追加
                    heading_texts.append(element.get_text().strip())
            items[tag].append(heading_texts)

    return items


"""
Googleスプレッドシートに情報を出力
"""

# 制限
# ①ユーザーごとに100秒あたり100件のリクエスト
# ②1秒あたり10件まで

# OAuth2の資格情報を使用してGoogleAPIにログイン

# シートが作成されているか確認するためのフラグ

# 共有設定したスプレッドシートのシート1を開く

# ワークシートを作成（タイトルがkeywordで、50行、50列）

# シートが作成されたらフラグを立てる

# スプレッドシート書き込み処理

# キーワードの書き込み

# 1秒待機

# 順位の書き込み

# 3秒待機

# 「タイトル」の書き込み

# 3秒待機

# 「URL」の書き込み

# 3秒待機

# 「ディスクリプション」の書き込み

# 3秒待機

# 「h1」の書き込み

# 3秒待機


# 「h2」の書き込み

# 3秒待機


# 「h3」の書き込み

# 3秒待機


# 「h4」の書き込み

# 3秒待機


# 「h5」の書き込み

# 3秒待機


# エラー処理

# グーグルスプレッドシートのAPIの制限に達した場合

# 100秒待機

# スプレッドシートに既にデータが存在している場合

if __name__ == "__main__":
    main()
