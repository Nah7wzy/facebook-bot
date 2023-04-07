import sched, time

from selenium.webdriver.chrome.options import Options
from facebook_bot import FacebookBot

OPTIONS = Options()
OPTIONS.headless = False  # set to True to run browser headless
OPTIONS.add_argument("window-size=1366,768")


bot = FacebookBot(email="se.nahom.tamru@gmail.com", password="123field45", options=OPTIONS)
s = sched.scheduler(time.time, time.sleep)


def check_for_post(sc):
    bot.login()
    if bot.check_new_post(page_id="100087292879019"):
        print("New Post!!!!!!!!!!!!!!!")
    else:
        print("No post yet, Retrying in 10min")

    sc.enter(600, 1, check_for_post, (sc,))


s.enter(0, 1, check_for_post, (s,))
s.run()
