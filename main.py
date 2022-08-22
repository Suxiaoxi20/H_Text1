from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random


week_list = ["星期一","星期二","星期三","星期四","星期五","星期六","星期日"]

today = datetime.now()
week=week_list[today.weekday()]
t_today = str(date.today())+' '+week
 
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']
bigbirthday= os.environ['BIGBIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]


def get_weather():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  res = requests.get(url).json()
  weather = res['data']['list'][0]
  return weather['weather'], math.floor(weather['temp'])

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return "距离小宝贝的生日还有"+str((next - today).days)+"天"
 
 def get_bigbirthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return "距离大宝贝的生日还有"+str((next - today).days)+"天"



def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']


def get_shi():
  shi=requests.get("https://v2.jinrishici.com/one.json")
  if shi.status_code!=200:
    return get_shi()
  return shi.json()['data']['content']


def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)



client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, temperature = get_weather()
data = {"t_today":{"value":t_today,"color":get_random_color()},
        "weather":{"value":wea,"color":get_random_color()},
        "city":{"value":city,"color":get_random_color()},
        "temperature":{"value":temperature,"color":get_random_color()},
        "love_days":{"value":get_count(),"color":get_random_color()},
        "birthday_left":{"value":get_birthday(),"color":get_random_color()},
        "words":{"value":get_words(), "color":get_random_color()},
        "shi":{"value":get_shi(), "color":get_random_color()},
        "bigbirthday_left":{"value":get_bigbirthday(),"color":get_random_color()}}
res = wm.send_template(user_id, template_id, data)
print(res)
