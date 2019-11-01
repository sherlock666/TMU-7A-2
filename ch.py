import requests
import re
import configparser
import os
import random
import pandas as pd
import runpy
#叫入並執行其他.py用
import urllib
import time
import tempfile
from bs4 import BeautifulSoup
from flask import Flask, request, abort
#from imgurpython import ImgurClient
from argparse import ArgumentParser
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    SourceUser, SourceGroup, SourceRoom,
    TemplateSendMessage, ConfirmTemplate, MessageAction,
    ButtonsTemplate, ImageCarouselTemplate, ImageCarouselColumn, URIAction, URITemplateAction,PostbackTemplateAction,
    PostbackAction, DatetimePickerAction,
    CameraAction, CameraRollAction, LocationAction,
    CarouselTemplate, CarouselColumn, PostbackEvent,
    StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
    ImageMessage, VideoMessage, AudioMessage, FileMessage,VideoSendMessage, ImageSendMessage,
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent,
    FlexSendMessage, BubbleContainer, ImageComponent, BoxComponent,
    TextComponent, SpacerComponent, IconComponent, ButtonComponent,
    SeparatorComponent, QuickReply, QuickReplyButton,ImagemapSendMessage, BaseSize, URIImagemapAction,
    ImagemapArea, MessageImagemapAction,
    Video, ExternalLink
)

##### Function Import #####

import subprocess

from tools.apple_news import apple_newss
apple_newss_content0, apple_newss_content1, apple_newss_content2 = apple_newss()

''' ###bug
from tools.gfl_article import gfl_articles
gfl_articles_content0, gfl_articles_content1, gfl_articles_content2, gfl_articles_content3, gfl_articles_content4 = gfl_articles()


from tools.tos_article import tos_articles
tos_articles_content0, tos_articles_content1, tos_articles_content2, tos_articles_content3, tos_articles_content4 = tos_articles()

from tools.fgo_article import fgo_articles
fgo_articles_content0, fgo_articles_content1, fgo_articles_content2, fgo_articles_content3, fgo_articles_content4 = fgo_articles()
'''

from tools.weather import weather

from tools.eyny_movie import eyny_movie

from tools.ptt_gossiping import ptt_gossiping
from tools.ptt_beauty import ptt_beauty
from tools.ptt_hot import ptt_hot

from tools.exchange_rate import exchange_rates

#for exchange rate calculation but crash
#content_ratecash,content_ratespot = exchange_rates(L)


from tools.movie import movie
from tools.yande_re import yande_res

from tools.panx import panx
from tools.technews import technews

from imgurpython import ImgurClient
##### Main #####

app = Flask(__name__)
config = configparser.ConfigParser()
config.read("config.ini")

###For Azure Setting
APP_ID = os.environ.get("APP_ID")
APP_PASSWORD = os.environ.get("APP_PASSWORD")
###
line_bot_api = LineBotApi('YOUR_CHANNEL_ACCESS_TOKEN')
handler = WebhookHandler('YOUR_CHANNEL_SECRET')
#line_bot_api = LineBotApi(config['line_bot']['Channel_Access_Token'])
#handler = WebhookHandler(config['line_bot']['Channel_Secret'])
client_id = config['imgur_api']['Client_ID']
client_secret = config['imgur_api']['Client_Secret']
album_id = config['imgur_api']['Album_ID']
access_token = config['imgur_api']['Access_token']
refresh_token = config['imgur_api']['Refresh_token']
API_Get_Image = config['other_api']['API_Get_Image']

static_tmp_path = os.path.join(os.path.dirname(__file__), 'static')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    # print("body:",body)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'ok'

# Routes
@app.route('/')
def root():
  return app.send_static_file('index.html')

@app.route('/<path:path>')
def static_proxy(path):
  # send_static_file will guess the correct MIME type
  return app.send_static_file(path)



'''



def get_page_number(content):
    start_index = content.find('index')
    end_index = content.find('.html')
    page_number = content[start_index + 5: end_index]
    return int(page_number) + 1

def craw_page(res, push_rate):
    soup_ = BeautifulSoup(res.text, 'html.parser')
    article_seq = []
    for r_ent in soup_.find_all(class_="r-ent"):
        try:
            # 先得到每篇文章的篇url
            link = r_ent.find('a')['href']
            if link:
                # 確定得到url再去抓 標題 以及 推文數
                title = r_ent.find(class_="title").text.strip()
                rate = r_ent.find(class_="nrec").text
                url = 'https://www.ptt.cc' + link
                if rate:
                    rate = 100 if rate.startswith('爆') else rate
                    rate = -1 * int(rate[1]) if rate.startswith('X') else rate
                else:
                    rate = 0
                # 比對推文數
                if int(rate) >= push_rate:
                    article_seq.append({
                        'title': title,
                        'url': url,
                        'rate': rate,
                    })
        except Exception as e:
            # print('crawPage function error:',r_ent.find(class_="title").text.strip())
            print('本文已被刪除', e)
    return article_seq
'''
@handler.add(MessageEvent, message=ImageMessage)
def handle_message(event):
    profile = line_bot_api.get_profile(event.source.user_id)
    print("event.reply_token:", event.reply_token)
    print("event.source.user_name:", profile.display_name)
    print("event.source.user_id:", event.source.user_id)
    print("event.message.text:", event.message.text)
    print("event.source.type:", event.source.type)
    #print("Image Path:", path)

    if isinstance(event.message, ImageMessage):
        ext = 'jpg'
        message_content = line_bot_api.get_message_content(event.message.id)
        with tempfile.NamedTemporaryFile(dir=static_tmp_path, prefix=ext + '-', delete=False) as tf:
            for chunk in message_content.iter_content():
                tf.write(chunk)
            tempfile_path = tf.name

        dist_path = tempfile_path + '.' + ext
        dist_name = os.path.basename(dist_path)
        os.rename(tempfile_path, dist_path)
        client = ImgurClient(client_id, client_secret, access_token, refresh_token)
        client.set_user_auth(access_token, refresh_token)
        config = {
            'album': album_id
            #'name': 'Catastrophe!',
            #'title': 'Catastrophe!',
            #'description': 'Cute kitten being cute on '
        }
        path = os.path.join('static', dist_name)
        client.upload_from_path(path, config=config, anon=False)
        os.remove(path)
        print(path)
        #imgur_image_id=cilent
        #line_bot_api.reply_message(
        #    event.reply_token,
        #    TextSendMessage(text='上傳成功'))
        #except:
        #    line_bot_api.reply_message(
        #        event.reply_token,
        #        TextSendMessage(text='上傳失敗'))
        return 0



@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    profile = line_bot_api.get_profile(event.source.user_id)
    print("event.reply_token:", event.reply_token)
    print("event.source.user_name:", profile.display_name)
    print("event.source.user_id:", event.source.user_id)
    print("event.message.text:", event.message.text)
    print("event.source.type:", event.source.type)

    text = event.message.text
    print("user_text:", text)
    
##########*****功能字庫區*****#########    
 
    keywords_cm_apple_news = ['!蘋果即時新聞','!蘋果即時','！蘋果即時新聞','！蘋果即時','蘋果即時新聞','蘋果即時']
    keywords_technews = ['!科技新報','！科技新報']
    keywords_panx = ['!PanX泛科技','！PanX泛科技']
    keywords_movie = ['!近期上映電影','！近期上映電影']
    keywords_eyny_movie = ['!eyny','！eyny']
    keywords_gfl_articles = ['!少女前線','！少女前線']
    keywords_tos_articles = ['!神魔之塔','！神魔之塔']
    keywords_fgo_articles = ['!fgo','！fgo']
    keywords_ptt_hot = ['!近期熱門廢文','！近期熱門廢文']
    keywords_ptt_gossiping = ['!即時廢文','！即時廢文']
    keywords_yande_re = ['!yande.re','!抽圖','！yande.re','！抽圖','抽圖','抽']
    keywords_ptt_beauty = ['!PTT表特版','！PTT表特版']
    keywords_imgur_beauty = ['!imgur正妹','！imgur正妹']
   # keywords_fgo_articles = ['!fgo']
   # keywords_fgo_articles = ['!fgo']
    
##########*****廢話字庫區*****#########      
    keywords_test_a = ['喵喵喵','測試測試']
    content_test_a = "我是小喵喵"
 
    keywords_test_b = ['喵~','喵喵~']
    content_test_b = "喵~喵~"
    
    keywords_test_c = ['喵?','喵喵?']
    content_test_c = "喵~~ (////)"
    
    if text in keywords_test_a:
        content = content_test_a
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0



##########*****休閒娛樂*****#########

##########***新聞***#########

    if text in keywords_cm_apple_news:
        content0 = apple_newss_content0
        content1 = apple_newss_content1
        content2 = apple_newss_content2
        print (content0)
        print (content1)
        print (content2)
        a=TextSendMessage(text=content0)
        b=TextSendMessage(text=content1)
        c=TextSendMessage(text=content2)
        reply_data=[a,b,c]
        line_bot_api.reply_message(
            event.reply_token,
            reply_data)
        return 0

    if text in keywords_technews:
        content = technews()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0

    if text in keywords_panx:
        content = panx()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0

##########***電影***#########
    if text in keywords_movie:
        content = movie()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0
    if text in keywords_eyny_movie:
        content = eyny_movie()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0

##########***遊戲資訊***#########
    if text in keywords_gfl_articles:
        content0 = gfl_articles_content0
        content1 = gfl_articles_content1
        content2 = gfl_articles_content2
        content3 = gfl_articles_content3
        content4 = gfl_articles_content4
        print (content0)
        print (content1)
        print (content2)
        print (content3)
        print (content4)
        a=TextSendMessage(text=content0)
        b=TextSendMessage(text=content1)
        c=TextSendMessage(text=content2)
        d=TextSendMessage(text=content3)
        e=TextSendMessage(text=content4)
        reply_data=[a,b,c,d,e]
        line_bot_api.reply_message(
            event.reply_token,
            reply_data)
        return 0

    if text in keywords_tos_articles:
        content0 = tos_articles_content0
        content1 = tos_articles_content1
        content2 = tos_articles_content2
        content3 = tos_articles_content3
        content4 = tos_articles_content4
        print (content0)
        print (content1)
        print (content2)
        print (content3)
        print (content4)
        a=TextSendMessage(text=content0)
        b=TextSendMessage(text=content1)
        c=TextSendMessage(text=content2)
        d=TextSendMessage(text=content3)
        e=TextSendMessage(text=content4)
        reply_data=[a,b,c,d,e]
        line_bot_api.reply_message(
            event.reply_token,
            reply_data)
        return 0

    if text in keywords_fgo_articles:
        content0 = fgo_articles_content0
        content1 = fgo_articles_content1
        content2 = fgo_articles_content2
        content3 = fgo_articles_content3
        content4 = fgo_articles_content4
        print (content0)
        print (content1)
        print (content2)
        print (content3)
        print (content4)
        a=TextSendMessage(text=content0)
        b=TextSendMessage(text=content1)
        c=TextSendMessage(text=content2)
        d=TextSendMessage(text=content3)
        e=TextSendMessage(text=content4)
        reply_data=[a,b,c,d,e]
        line_bot_api.reply_message(
            event.reply_token,
            reply_data)
        return 0

##########***看廢文***#########        
    if text in keywords_ptt_hot:
        content = ptt_hot()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0
    if text in keywords_ptt_gossiping:
        content = ptt_gossiping()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0

##########***圖片***#########  
    if text in keywords_yande_re:
        num=random.randint(100000,500000)
        yande_link=yande_res(num=int(num))
        image_message = ImageSendMessage(
            original_content_url=yande_link,
            preview_image_url=yande_link
        )        
        line_bot_api.reply_message(
            event.reply_token, image_message)
        return 0

    if text in keywords_ptt_beauty:
        content = ptt_beauty()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0
    if text in keywords_imgur_beauty:
        client = ImgurClient(client_id, client_secret)
        images = client.get_album_images(album_id)
        index = random.randint(0, len(images) - 1)
        url = images[index].link
        image_message = ImageSendMessage(
            original_content_url=url,
            preview_image_url=url
        )
        line_bot_api.reply_message(
            event.reply_token, image_message)
        return 0
    if event.message.text == "!抽抽樂":
        image = requests.get(API_Get_Image)
        url = image.json().get('Url')
        image_message = ImageSendMessage(
            original_content_url=url,
            preview_image_url=url
        )
        line_bot_api.reply_message(
            event.reply_token, image_message)
        return 0

##########***財經專區***#########  
    if event.message.text == "!每日匯率":
        res = requests.get("http://rate.bot.com.tw/xrt?Lang=zh-TW")
        soup = BeautifulSoup(res.text,'html.parser')
        dailydate=soup.select("span[class='time']")[0].text
        content1 = "本匯率資訊取自 台灣銀行告牌匯率\n提供 台幣對:\n美金 日幣 人民幣 港幣\n英鎊 韓元 歐元\n僅供使用者參考 謝謝!!\n\n請直接輸入欲查詢幣別(例如: !日幣)\n"+"最新掛牌時間 : "+dailydate
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content1))

    if event.message.text == "!美金":
        content = exchange_rates(L=1)
        print(content)
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
        return 0

    if event.message.text == "!日幣":
        content = exchange_rates(L=15)
        print(content)
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
        return 0
    if event.message.text == "!人民幣":
        content = exchange_rates(L=37)
        print(content)
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
        return 0
    if event.message.text == "!港幣":
        content = exchange_rates(L=3)
        print(content)
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
        return 0
    if event.message.text == "!英鎊":
        content = exchange_rates(L=5)
        print(content)
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
        return 0
    if event.message.text == "!韓元":
        content = exchange_rates(L=31)
        print(content)
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
        return 0
    if event.message.text == "!歐元":
        content = exchange_rates(L=29)
        print(content)
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
        return 0     








### 美金1 日幣15 人民幣37 港幣3 英鎊5 韓元31 歐元29


##########***自製小品***#########  
    if event.message.text == "!猜數字":
        content = guess_play()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0
##########***其他功能***#########  





##########***天氣預報***#########  

    if event.message.text == "!天氣預報":
        content = "請輸入欲查詢地點\n(目前限台灣本島+離島)\n\n使用方式如下(已設有防呆):\n!台北市\n!臺北市\n!台北\n!臺北\n!taipei"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0

    if event.message.text == "!台北市" or event.message.text == "!臺北市" or event.message.text == "!台北" or event.message.text == "!臺北" or event.message.text == "!taipei":
        content = weather(L=0)
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
        return 0
    if event.message.text == "!新北市" or event.message.text == "!新北" or event.message.text == "!new taipei":
        content = weather(L=1)
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
        return 0
    if event.message.text == "!桃園市" or event.message.text == "!taoyuan":
        content = weather(L=2)
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
        return 0
    if event.message.text == "!台中市" or event.message.text == "!臺中市" or event.message.text == "!台中" or event.message.text == "!臺中" or event.message.text == "!taichung":
        content = weather(L=3)
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
        return 0
    if event.message.text == "!台南市" or event.message.text == "!臺南市" or event.message.text == "!台南" or event.message.text == "!臺南" or event.message.text == "!tainan":
        content = weather(L=4)
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
        return 0
    if event.message.text == "!高雄市" or event.message.text == "!高雄" or event.message.text == "!kaohsiung":
        content = weather(L=5)
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
        return 0
    if event.message.text == "!基隆市" or event.message.text == "!基隆" or event.message.text == "!keelung":
        content = weather(L=6)
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
        return 0
    if event.message.text == "!新竹縣" or event.message.text == "!hsinchu county":
        content = weather(L=7)
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
        return 0
    if event.message.text == "!新竹市" or event.message.text == "!hsinchu city":
        content = weather(L=8)
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
        return 0
    if event.message.text == "!苗栗縣" or event.message.text == "!苗栗" or event.message.text == "!miaoli":
        content = weather(L=9)
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
        return 0
    if event.message.text == "!彰化縣" or event.message.text == "!彰化" or event.message.text == "!changhua":
        content = weather(L=10)
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
        return 0
    if event.message.text == "!南投縣" or event.message.text == "!南投" or event.message.text == "!nantou":
        content = weather(L=11)
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
        return 0
    if event.message.text == "!雲林縣" or event.message.text == "!雲林" or event.message.text == "!yunlin":
        content = weather(L=12)
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
        return 0
    if event.message.text == "!嘉義縣" or event.message.text == "!chiayi county":
        content = weather(L=13)
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
        return 0
    if event.message.text == "!嘉義市" or event.message.text == "!chiayi city":
        content = weather(L=14)
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
        return 0
    if event.message.text == "!屏東縣" or event.message.text == "!屏東" or event.message.text == "!pingtung":
        content = weather(L=15)
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
        return 0
    if event.message.text == "!宜蘭縣" or event.message.text == "!宜蘭" or event.message.text == "!ilan":
        content = weather(L=16)
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
        return 0
    if event.message.text == "!花蓮縣" or event.message.text == "!花蓮" or event.message.text == "!hualien":
        content = weather(L=17)
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
        return 0
    if event.message.text == "!臺東縣" or event.message.text == "!台東" or event.message.text == "!taitung":
        content = weather(L=18)
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
        return 0
    if event.message.text == "!澎湖縣" or event.message.text == "!澎湖" or event.message.text == "!penghu":
        content = weather(L=19)
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
        return 0
    if event.message.text == "!金門縣" or event.message.text == "!金門" or event.message.text == "!jinmen":
        content = weather(L=20)
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
        return 0
    if event.message.text == "!連江縣" or event.message.text == "!連江" or event.message.text == "!lianjiang":
        content = weather(L=21)
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
        return 0


##########***隱藏專區(需權限)***#########  

##########***測試區***#########  
    if event.message.text == "群組資訊":
        groupid = event.source.group_id
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=groupid))
        return 0

    if event.message.text == "個資":
        content = event.source.user_id
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0
#       print()
#               print(profile.user_id)
#               print(profile.picture_url)


##########***個人限定功能***#########  

    if event.source.type == "user" and event.message.text == "你好嗎?":
        content = "我很好~~"
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
        return 0

    if event.source.type == "user" and event.message.text == "選診協助":
        content="您好，歡迎來到台北醫學大學附設醫院，請問您今年幾歲?"
        user_id = event.source.user_id
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
        return 0
        if event.source.user_id == "user_id":
                usertext = event.message.text
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text=usertext))
                return 0



##########***隱藏專區(需權限)***#########  
#    if event.message.text == "測試":
#       if isinstance(event.source, SourceUser)
#               profile = line_bot_api.get_profile(event.source.user_id)
#               line_bot_api.reply_message(
#                               event.reply_token,
#               TextSendMessage(text=profile.user_id))       
#               else:
#            line_bot_api.reply_message(
#                event.reply_token,
#                TextMessage(text="Bot can't use profile API without user ID"))


##########***系統區***#########  
    if event.message.text == "!幫助":
        content = "指令輸入請使用 半形驚嘆號!\n若有任何使用問題\n請於本帳號主頁留言詢問\n謝謝!!"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0


#################### 主目錄 #####################
    if event.message.text == "!開始玩":
        fun="\n\n*****休閒娛樂*****\n新聞\n電影\n遊戲資訊\n看廢文\n圖片(施工中)"
        academic="\n\n*****學術專區*****\n施工中"
        medical="\n\n*****醫療新知*****\n施工中"
        financial="\n\n*****財經專區*****\n每日匯率"
        diy="\n\n*****自製小品*****\n猜數字(施工中)"
        other="\n\n*****其他功能*****\n天氣預報"
        SelfReplyOnly="\n\n*****私聊限定*****\n!本區功能無法於群組使用!\n!請點選本帳號的聊天以使用!\n施工中"
        content = ("請輸入功能指令:"+fun+academic+medical+financial+diy+SelfReplyOnly+other+"\n\n幫助")
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0
    if event.message.text == "!新聞":
        content = "請選擇新聞類型:\n\n蘋果即時新聞\n科技新報\nPanX泛科技\n陸續增加...."
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0

    if event.message.text == "!電影":
        content = "請選擇來源:\n\n近期上映電影\neyny\n陸續增加...."
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0

    if event.message.text == "!遊戲資訊":
        content = "請選擇遊戲:\n\n神魔之塔\n少女前線\nfgo\n陸續增加...."
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0

    if event.message.text == "!看廢文":
        content = "請選擇來源:\n\n近期熱門廢文\n即時廢文"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0

    if event.message.text == "!圖片":
        content = "請輸入功能指令:\n\n***動漫區(施工中)***\nyande.re (抓圖)\n\n***其他***\nPTT表特版 (近期大於 10 推的文章)\nimgur正妹(施工中) (imgur 正妹圖片)\n抽抽樂(施工中) (隨便來張正妹圖片)\n陸續增加...."
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0

    if event.message.text == "!猜數字":
        content = "施工中~"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0

#################### bot群組相關設定 #####################

### 入群問候 (維護中) ###

@handler.add(JoinEvent)
def handle_join(event):
    msg = '大家好~~輸入 !開始玩 以叫出功能表\n麻煩於每則指令前輸入小驚嘆號\n例如: !新聞'.format(event.source.type)
    line_bot_api.reply_message(event.reply_token, TextSendMessage(msg))

if __name__ == '__main__':
    app.run()

