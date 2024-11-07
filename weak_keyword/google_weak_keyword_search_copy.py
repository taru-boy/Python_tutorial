# ブラウザを自動操作するためseleniumをimport
from selenium import webdriver

# seleniumでEnterキーを送信する際に使用するのでimport
from selenium.webdriver.common.keys import Keys

# web画面の要素を取得するのに使うのでimport
from selenium.webdriver.common.by import By

# seleniumでヘッドレスモードを指定するためにimport
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService

# 待ち時間を指定するためにtimeをimport
import time

# 正規表現にマッチする文字列を探すためにreをimport
import re

# Googleのトップページ
URL = "https://www.google.co.jp"


def main():
    """
    メインの処理
    Googleの検索エンジンでキーワードを検索
    指定されたドメインが検索結果の１ページ目に含まれていないキーワードをテキストファイルに出力
    """

    # 'search_keyword_list.txt'ファイルを読み込み、リストにする
    with open("search_keyword_list.txt") as f:
        # １行ずつ読み込んで改行コードを削除してリストにする
        keywords = [keyword.rstrip() for keyword in f.readlines()]

    # 'ドメインリスト.txt'ファイルを読み込み、リストにする
    with open("domain_list.txt") as f:
        # １行ずつ読み込んで改行コードを削除してリストにする
        domains = [domain.rstrip() for domain in f.readlines()]

    # seleniumで自動操作するブラウザはGoogleChrome
    options = Options()  # Optionsオブジェクトを作成

    # ヘッドレスモードを有効にする
    options.add_argument("--headless")

    # ChromeのWebDriverオブジェクトを作成
    service = ChromeService("/usr/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(URL)  # Googleのトップページを開く
    time.sleep(1)  # 2秒待機（読み込みのため）

    ok_keyword_list = []
    for keyword in keywords:  # 検索キーワードを１つずつ取り出す
        search(driver=driver, keyword=keyword)  # search関数実行
        urls = get_url(driver=driver)  # get_url関数を実行し、戻り値をurlsに代入
        weak_keyword_list = domain_checked(
            urls=urls, domains=domains, keyword=keyword, ok_keyword_list=ok_keyword_list
        )  # domain_checked関数を実行し、戻り値をok_keywordlistに代入

    # '結果.txt'という名前を付けて、ドメインチェックしたキーワードをファイルに書き込む
    with open("result.txt", "w") as f:
        f.write(
            "\n".join(weak_keyword_list)
        )  # ドメインチェック済みのキーワードを１行ずつ保存

    driver.quit()  # ブラウザーを閉じる


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


def get_url(driver) -> list:
    """
    検索結果ページの1位から10位までのURLを取得
    """

    # 各ページのURLを入れるためのリストを指定
    urls = []
    # a要素（各ページの1位から10位までのURL）取得
    objects = driver.find_elements(
        By.CSS_SELECTOR, "div.kb0PBd.A9Y9g.jGGQ5e > div > div > span > a"
    )

    if objects:
        for object in objects:
            temp_url = object.get_attribute("href")
            urls.append(temp_url)  # 各ページのURLをリストに追加
    else:
        print(
            "URLを取得できませんでした。"
        )  # 各ページのURLが取得できなかった場合は警告を出す
    return urls  # 各ページのURLを戻り値に指定


def domain_checked(urls, domains, keyword, ok_keyword_list) -> list:
    """
    URLリストからドメインを取得し、指定ドメインに含まれているかチェック
    """
    # URLリストから各ページのURLを１つずつ取り出す
    for url in urls:
        m = re.search(r"//(.*?)/", url)  # '//〇〇/'に一致する箇所（ドメイン）を抜き出す
        domain = m.group(1)  # '//〇〇/'の'〇〇'に一致する箇所を抜き出し、domainに代入
        if r"www." in domain:  # ドメインに'www.'が含まれているかチェック
            domain = domain[4:]  # 含まれているなら'www.'を除去
        if (
            domain in domains
        ):  # 各ページのドメインが指定ドメインに含まれているかチェック
            # 含まれているなら警告を出す
            print(
                f"キーワード「{keyword}」の検索結果には大手ドメインが含まれていたので除外します。"
            )
            break  # １つでも含まれているなら他はチェックする必要がないので関数を終了
    else:
        # 指定ドメインに含まれていないならキーワードをok_keywordlistに追加
        ok_keyword_list.append(keyword)
    return ok_keyword_list  # ドメインチェック済みのキーワードを戻り値に指定


if __name__ == "__main__":
    # main関数を実行
    main()
