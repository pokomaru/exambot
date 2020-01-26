import datetime
import json
import logging
import os

from apscheduler.schedulers.blocking import BlockingScheduler
from flask import Flask, request, abort
from function import Function
from getdays import Getdays

from linebot.models import (
    FollowEvent, UnfollowEvent, JoinEvent, LeaveEvent, MessageEvent, TextMessage, TextSendMessage
)

from linebot import (
    LineBotApi, WebhookHandler
)

app = Flask(__name__)

# ログの設定
logger = logging.getLogger(__name__)
logger.setLevel(20)
logger.addHandler(logging.StreamHandler())
logger.addHandler(logging.FileHandler("exambot.log"))

sched = BlockingScheduler()
date_data = datetime.datetime.now().strftime("[%Y/%m/%d %H:%M:%S] ")

# conf.jsonの絶対パスの取得
abs_path = os.path.abspath("conf.json")
with open(abs_path, 'r') as file:
    CONF_DATA = json.load(file)

# log.jsonの絶対パスの取得
abs_path = os.path.abspath("log.json")
with open(abs_path, 'r') as file:
    LOG_DATA = json.load(file)

line_bot_api = LineBotApi(CONF_DATA["CHANNEL_ACCESS_TOKEN"])
handler = WebhookHandler(CONF_DATA["CHANNEL_SECRET"])


@app.route("/")
def say_hello():
    return "Hello World"


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

# Follow Event
@handler.add(FollowEvent)
def on_follow(event):
    try:
        user_id = event.source.user_id
        name = line_bot_api.get_profile(user_id).display_name
        welcome_message = "お友達追加ありがとう🐹\n高校入試まで一緒に頑張ろう！"
        line_bot_api.push_message(
            user_id, TextSendMessage(text=welcome_message))
        Function().insert_user(user_id, name)
        logger.log(20,  LOG_DATA["ON_FOLLOW"] + date_data)

    except:
        logger.log(40, LOG_DATA["ERROR_FOLLOW"] + date_data)


# Unfollow Event
@handler.add(UnfollowEvent)
def un_follow(event):
    try:
        user_id = event.source.user_id
        Function().delete_user(user_id)
        logger.log(20, LOG_DATA["UN_FOLLOW"] + date_data)

    except:
        logger.log(40, LOG_DATA["ERROR_UN_FOLLOW"] + date_data)


# Join Event
@handler.add(JoinEvent)
def join_group(event):
    try:
        group_id = event.source.group_id
        welcome_message = "グループへの追加ありがとう🐶\n高校入試まで一緒に頑張ろう！"
        line_bot_api.push_message(
            group_id, TextSendMessage(text=welcome_message))
        Function().insert_group(group_id)
        logger.log(20, LOG_DATA["JOIN_GROUP"] + date_data)

    except:
        logger.log(40, LOG_DATA["ERROR_JOIN"] + date_data)


# Leave Event
@handler.add(LeaveEvent)
def leave_group(event):
    try:
        group_id = event.source.group_id
        Function().delete_group(group_id)
        logger.log(20, LOG_DATA["LEAVE_GROUP"] + date_data)

    except:
        logger.log(40, LOG_DATA["ERROR_LEAVE"] + date_data)


@sched.scheduled_job('cron', hour=21)
def send_precheck():
    try:
        user_id_all = Function().get_user_id()
        group_id_all = Function().get_group_id()

        for user_id in user_id_all:
            user_id = str(user_id)[2:-3]
            logger.log(20, LOG_DATA["MESSAGE"] + date_data)
            line_bot_api.push_message(user_id, TextSendMessage(
                text=Getdays().return_precheck()))

        for group_id in group_id_all:
            group_id = str(group_id)[2:-3]
            logger.log(20, LOG_DATA["MESSAGE"] + date_data)
            line_bot_api.push_message(group_id, TextSendMessage(
                text=Getdays().return_precheck()))

    except:
        logger.log(40, LOG_DATA["ERROR_MESSAGE"] + date_data)


@sched.scheduled_job('cron', hour=23, minute=59)
def send_check():
    try:
        user_id_all = Function().get_user_id()
        group_id_all = Function().get_group_id()

        for user_id in user_id_all:
            user_id = str(user_id)[2:-3]
            logger.log(20, LOG_DATA["MESSAGE"] + date_data)
            line_bot_api.push_message(
                user_id, TextSendMessage(text=Getdays().return_check()))

        for group_id in group_id_all:
            group_id = str(group_id)[2:-3]
            logger.log(20, LOG_DATA["MESSAGE"] + date_data)
            line_bot_api.push_message(
                group_id, TextSendMessage(text=Getdays().return_check()))

    except:
        logger.log(40, LOG_DATA["ERROR_MESSAGE"] + date_data)


@sched.scheduled_job('cron', hour=7, minute=30)
def send_day():
    try:
        user_id_all = Function().get_user_id()
        group_id_all = Function().get_group_id()

        for user_id in user_id_all:
            user_id = str(user_id)[2:-3]
            logger.log(20, LOG_DATA["MESSAGE"] + date_data)
            line_bot_api.push_message(
                user_id, TextSendMessage(text=Getdays().return_day()))

        for group_id in group_id_all:
            group_id = str(group_id)[2:-3]
            logger.log(20, LOG_DATA["MESSAGE"] + date_data)
            line_bot_api.push_message(
                group_id, TextSendMessage(text=Getdays().return_day()))

    except:
        logger.log(40, LOG_DATA["ERROR_MESSAGE"] + date_data)


if __name__ == "__main__":
    sched.start()
    app.run()
