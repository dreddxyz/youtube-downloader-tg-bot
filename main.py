from __future__ import unicode_literals
from contextlib import suppress
import youtube_dl
import os
import telebot

def download_sound_from_youtube(url):
  ydl_opts = {
      'format': 'bestaudio/best',
      'postprocessors': [{
          'key': 'FFmpegExtractAudio',
          'preferredcodec': 'mp3',
          'preferredquality': '192',
      }]
  }
  with youtube_dl.YoutubeDL(ydl_opts) as ydl:
      ydl.download([url])

def download_song(message, song_url):
    outtmpl = str(message.chat.id) + '.mp3'
    if os.path.exists(outtmpl):
        os.remove(outtmpl)
    def cb(d):
        if d['status'] == 'finished':
            bot.send_audio(chat_id=message.chat.id, audio=open(str(message.chat.id) + '.mp3', 'rb'))
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': outtmpl,
        'postprocessors': [
            {'key': 'FFmpegExtractAudio','preferredcodec': 'mp3',
             'preferredquality': '192',
            },
            {'key': 'FFmpegMetadata'},
        ],
        'progress_hooks': [cb]
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        with suppress(Exception):
            info_dict = ydl.extract_info(song_url, download=True)

def download_video(message, url):
    outtmpl = str(message.chat.id) + '.mp4'
    if os.path.exists(outtmpl):
        os.remove(outtmpl)
    def cb(d):
        if d['status'] == 'finished':
            bot.send_video(chat_id=message.chat.id, video=open(str(message.chat.id) + '.mp4', 'rb'))
    ydl_opts = {'outtmpl': outtmpl, 'progress_hooks': [cb], 'format': 'mp4'}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        with suppress(Exception):
            ydl.download([url])

def extract_arg(arg):
    return arg.split()[1:]


bot = telebot.TeleBot('lmao')
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "/video [url] - скачать видео \n/song [url] - скачать аудио")

@bot.message_handler(commands=['song'])
def send_song(message):
    bot.reply_to(message, 'Скачиваем аудио...')
    url = extract_arg(message.text)
    download_song(message,url[0])

@bot.message_handler(commands=['video'])
def send_video(message):
    bot.reply_to(message, 'Скачиваем видео...')
    url = extract_arg(message.text)
    download_video(message,url[0])

bot.polling()
