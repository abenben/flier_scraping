from datetime import datetime
from logging import (
    getLogger,
    StreamHandler,
    Filter,
    basicConfig,
    DEBUG,
    FileHandler,
)
from selenium import webdriver
import chromedriver_binary
from selenium.webdriver.chrome.options import Options
from abc import abstractmethod

from datetime import datetime
from selenium.webdriver.support.ui import Select
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import os
from typing import List, Dict
from dataclasses import dataclass, field


class Scraping:
    """スクレイピング"""

    def __init__(self):
        self.logger = getLogger(__name__)
        self.logger.setLevel(DEBUG)

        self.handler1 = StreamHandler()
        # self.handler1.addFilter(Filter("__main__"))

        self.handler2 = FileHandler(
            filename="./logs/{:%Y%m%d_%H%M%S}.log".format(datetime.now())
        )  # handler2はファイル出力

        # モジュール全体のログ設定に上記ハンドラを含むリストを渡す
        basicConfig(
            handlers=[self.handler1, self.handler2],
            format="[%(asctime)s] %(levelname)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

    def scraping(self):
        """
        スクレイピングを実行する
        :return:なし
        """
        self.logger.info("[START] scraping")

        self.scraping_logic()

        self.logger.info("[END  ] scraping")

    def open_browser(self):
        """Chromeブラウザを開く"""

        options = Options()
        options.binary_location = (
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        )
        # options.add_argument("--headless")
        driver = webdriver.Chrome(chrome_options=options)
        driver.implicitly_wait(2)

        return driver

    # @abstractmethod
    def scraping_logic(self):
        """スクレイピングを実施する（抽象メソッド）"""
        self.driver = self.open_browser()

        # ログインページからログインする
        self.driver.get("https://www.flierinc.com/")
        self.driver.set_window_size(800, 1200)

        login_button = self.driver.find_element(By.CLASS_NAME, "btn-fl-login")
        login_button.click()

        # ユーザーIDとパスワードは環境変数から取得する
        email = self.driver.find_element(By.ID, "email")
        email.send_keys(os.environ.get("FLIER_EMAIL"))
        pswd = self.driver.find_element(By.ID, "password")
        pswd.send_keys(os.environ.get("FLIER_PASSWORD"))

        # ログインボタンをクリックする
        login = self.driver.find_element(By.NAME, "btn-fl-submi")
        login.click()

        # 画面遷移を待つ
        WebDriverWait(self.driver, 90).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    '//button[@data-action_id="SYLLABUS_SEARCH_KEYWORD_EXECUTE"]',
                )
            )
        )


# ガター内の緑色のボタンを押すとスクリプトを実行します。
if __name__ == "__main__":
    sc = Scraping()
    sc.scraping()
