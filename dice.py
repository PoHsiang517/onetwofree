import json
import logging
import os
import random

import cachetools.func
import gspread
from linebot.models import FlexSendMessage, BubbleContainer, BoxComponent, \
    ImageComponent, TextComponent

from app.utils.gspread_util import auth_gss_client
from constants import HUGE_GROUP_IDS, TEACHER_HO, PAN_SENTENCES, GSPREAD_KEY_CAT, GOOGLE_AUTH_JSON_PATH, \
    GSPREAD_KEY_SCHUMI, GSPREAD_KEY_SINOALICE

tarot_cards = json.load(open('app/tarot.json', encoding='utf8'))


def draw_card(msg_info, robot_settings):
    random.seed(os.urandom(5))
    msg = random.choice(TEACHER_HO)
    return msg.format(name=msg_info.user_name)


def pan_pan(msg_info, robot_settings):
    random.seed(os.urandom(5))
    msg = random.choice(PAN_SENTENCES)
    return msg


def tarot(msg_info, robot_settings):
    random.seed(os.urandom(5))
    card = random.choice(tarot_cards)
    logging.info('%s: %s', card['nameCN'], card['url'])
    replies = []
    if msg_info.source_id not in HUGE_GROUP_IDS:
        # skip card picture for large groups
        replies.append(('image', card['url']))
    replies.append(('text', f'{card["nameCN"]}: {card["conclusion"]}'))
    return replies


def fortune(msg_info, robot_settings):
    random.seed(os.urandom(5))
    dice = random.randint(1, 1000)  # 1 <= N <= 1000
    ans = [
        '／(˃ᆺ˂)＼大吉だよ！\nやったね⭐︎',
        '／(^ x ^=)＼大吉……騙你的，差一點呢！\n只是吉而已呦',
        '／(^ x ^)＼吉。🎉\n很棒呢！',
        '／(･ × ･)＼中吉。\n朽咪覺得還不錯吧。(ゝ∀･)',
        '／(･ × ･)＼小吉。\n就是小吉，平淡過日子，願世界和平。☮',
        '／(･ × ･)＼半吉。\n㊗️朽咪祝福你！',
        '／(･ × ･)＼末吉。\n嗯～勉勉強強吧！',
        '／(･ × ･)＼末小吉。\n至少不壞呢！',
        '／(=´x`=)＼凶。\n往好處想，至少還有很多更糟的！',
        '／(=´x`=)＼小凶。\n運氣不是很好呢，怎麼辦？',
        '／(=´x`=)＼半凶。\n有點糟糕～',
        '／(=´x`=)＼末凶。\n運氣真差阿...幫QQ',
        '／人◕ ‿‿ ◕人＼ 大凶⁉️僕と契約して、魔法少女になってよ！'
    ]
    if dice <= 20:
        return ans[0]
    elif dice <= 100:
        return ans[1]
    elif dice <= 200:
        return ans[2]
    elif dice <= 300:
        return ans[3]
    elif dice <= 400:
        return ans[4]
    elif dice <= 500:
        return ans[5]
    elif dice <= 600:
        return ans[6]
    elif dice <= 700:
        return ans[7]
    elif dice <= 800:
        return ans[8]
    elif dice <= 850:
        return ans[9]
    elif dice <= 900:
        return ans[10]
    elif dice <= 950:
        return ans[11]
    elif dice <= 1000:
        return ans[12]
    else:
        raise ValueError