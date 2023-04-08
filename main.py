import sched
import time
import pushbullet
# import vonage

from selenium.webdriver.chrome.options import Options
from facebook_bot import FacebookBot

OPTIONS = Options()
OPTIONS.headless = True  # set to True to run browser headless
OPTIONS.add_argument("window-size=1366,768")

PUSHBULLET_API_KEY = ""
pb = pushbullet.Pushbullet(PUSHBULLET_API_KEY)
PUSHBULLET_API_KEY2 = ""
pb2 = pushbullet.Pushbullet(PUSHBULLET_API_KEY2)

bot = FacebookBot(
    email="", password="", options=OPTIONS
)
s = sched.scheduler(time.time, time.sleep)

first = True


# def notify():
#     phones = ['251977198732', '251925267263']
#     client = vonage.Client(key="35d469ae", secret="whODEBIZqlTNjM9f")
#     sms = vonage.Sms(client)

#     for phone in phones:
#         responseData = sms.send_message(
#             {
#                 "from": "Vonage APIs",
#                 "to": phone,
#                 "text": "Time to make your football field reservation.",
#             }
#         )


def check_for_post(sc):
    global first
    if first:
        bot.login()
        first = False

    if bot.check_new_post(page_id="100087292879019"):
        print("New Post!!!!!!!!!!!!!!!")

        pb.push_note("!!!!!New Post!!!!",
                     "There has been a new post on Facebook!!!")
        pb2.push_note("!!!!!New Post!!!!",
                      "There has been a new post on Facebook!!!")

    else:
        print("No post yet, Retrying in 3 min")
        # pb.push_note("No New Post",
        #              "There is no new post on Facebook!!!")
        # pb2.push_note("No New Post",
        #               "There is no new post on Facebook!!!")

    sc.enter(180, 1, check_for_post, (sc,))


s.enter(0, 1, check_for_post, (s,))
s.run()
