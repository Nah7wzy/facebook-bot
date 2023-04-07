from time import sleep
import logging
import re


from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.remote_connection import LOGGER
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium import webdriver


LOGGER.setLevel(logging.ERROR)


# TODO better pattern match
# TODO check post content
# TODO better error handling


class FacebookBot:
    def __init__(self, email: str, password: str, options: Options) -> None:
        self.bot = webdriver.Chrome(
            options=options, service=Service(ChromeDriverManager().install())
        )

        self.email = email
        self.password = password
        self.loggedin = False

    def login(self):
        bot = self.bot
        bot.get("https://www.facebook.com/login.php/")

        try:

            if bot.find_element(By.CSS_SELECTOR, "div#cookie_banner_title"):
                self.__close_cookie_consent(bot=bot)
                sleep(5)

            email_feild = bot.find_element(By.CSS_SELECTOR, "input#email")
            password_feild = bot.find_element(By.CSS_SELECTOR, "input#pass")
            login_btn = bot.find_element(By.CSS_SELECTOR, "button#loginbutton")

            email_feild.send_keys(self.email)
            password_feild.send_keys(self.password)
            ActionChains(bot).click(login_btn).perform()

            self.loggedin = True
            print("Login complete!")

            sleep(5)

        except Exception as e:
            print("In login")
            print(e)

    def __close_cookie_consent(self, bot):

        try:
            reject_button = bot.find_elements(By.CSS_SELECTOR, "div._9xo5 button")[1]
            ActionChains(bot).click(reject_button).perform()

        except Exception as e:
            print("In __close_cookie_consent")
            print(e)

    def __check_if_latest_post(self, date: str):
        regx_pattern = r"[a-zA-Z]+\s[0-9]+\sat\s[0-9]+:[0-9]+\s[AMPM]+"
        match = re.search(pattern=regx_pattern, string=date)

        prev_date = "March 20 at 2:31 PM"

        if match and match[0] != prev_date:
            return True

        return False

    def check_new_post(self, page_id: str):
        if self.loggedin:

            bot = self.bot
            bot.get(f"https://www.facebook.com/profile.php?id={page_id}")

            sleep(5)

            post_date = bot.find_elements(
                By.CSS_SELECTOR,
                "a",
            )

            for link in post_date:
                clean_link = link.text.strip()
                if clean_link and self.__check_if_latest_post(date=clean_link):
                    return True

        else:
            self.login()
            self.get_post(page_id=page_id)

        return False
