import requests
import telebot
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from newsapi import NewsApiClient

BOT_TOKEN = os.environ.get('BOT_TOKEN')
BOT_CHATID = os.environ.get('BOT_CHATID')
API_NEWS = os.environ.get('API_NEWS')

bot = telebot.TeleBot(BOT_TOKEN)
newsapi = NewsApiClient(api_key=API_NEWS)


def get_daily_news(news: str):
    news = str(news.text.split('/')[1])

    top_headlines = newsapi.get_top_headlines(language='it',category=news)
    for i in top_headlines['articles']:
        
        message = ' - '.join((i['title'],i['url']))
        bot.send_message(BOT_CHATID,message, parse_mode="HTML",disable_web_page_preview=True,)

    return top_headlines

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")

@bot.message_handler(commands=['business','entertainment','general','health','science','sports','technology'])
def get_news(message):
    get_daily_news(message)
    
bot.infinity_polling()