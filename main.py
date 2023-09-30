import telebot
from telebot import types
from db import *
from newsapi import NewsApiClient
from config import *

bot = telebot.TeleBot('6689110739:AAH41VUtNzVxDuTZJ6eP3uVG1292h5LyMiI')
newsapi = NewsApiClient(api_key=news_key)

@bot.message_handler(commands=['start'])
def start(message):
  tg_id = message.from_user.id
  markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
  btn1 = types.KeyboardButton("Подписки")
  btn2 = types.KeyboardButton("Новости")
  btn3 = types.KeyboardButton("Категории")
  markup.add(btn1,btn2,btn3)
  if searchUser(tg_id) != None:
      bot.reply_to(message, "Вы уже зарегестрированы", reply_markup=markup)
  else:
    bot.reply_to(message, "Что вы хотите сделать?", reply_markup=markup)
    addCategories()
    reg(tg_id)

@bot.message_handler(content_types=['text'])
def get_text_messages(message):

    if message.text == 'Категории':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        categories = category()
        i = 0
        while i < len(categories):
            btn1 = types.KeyboardButton("Подпишитесь на " + categories[i][0])
            markup.add(btn1)
            i=i+1
        back = types.KeyboardButton('Назад')
        markup.add(back)
        bot.send_message(message.from_user.id, 'Выберите понравившиеся вам категории новостей', reply_markup=markup)

    if message.text.startswith("Подпишитесь"):
        tg_id = message.from_user.id
        user_id = str(searchUserId(tg_id)[0])
        subscribes = searchUserCategory(user_id)
        arr = []
        i = 0
        while i < len(subscribes):
            arr.append(subscribes[i])
            i = i + 1
        i = 0
        count = 0
        text = message.text[15:]
        while i<len(arr):
            if text == arr[i][0]:
                count=count+1
            i=i+1
        if count == 0:
            category_id = searchCategory(text)[0]
            subCategory(user_id,category_id)
            bot.reply_to(message, "Вы успешно подписаны")
        else:
            bot.reply_to(message, "Вы уже подписаны")

    elif message.text == 'Подписки':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        tg_id = message.from_user.id
        user_id = str(searchUserId(tg_id)[0])
        userSub = searchSubUser(user_id)
        i = 0
        while i < len(userSub):
            name = types.KeyboardButton("Отписаться от " + ''.join(userSub[i]))
            markup.add(name)
            i = i + 1
        back = types.KeyboardButton('Назад')
        markup.add(back)
        bot.reply_to(message, "Ваши подписки:", reply_markup=markup)

    elif message.text.startswith("Отписаться"):
        tg_id = message.from_user.id
        user_id = str(searchUserId(tg_id)[0])
        subscribes = searchUserCategory(user_id)
        arr = []
        i = 0
        while i < len(subscribes):
            arr.append(subscribes[i])
            i = i + 1
        i = 0
        count = 0
        text = message.text[14:]
        while i < len(arr):
            if text == arr[i][0]:
                count = count + 1
            i = i + 1
        if count > 0:
            category_id = searchCategory(text)[0]
            unsubCategory(user_id,category_id)
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            userSub = searchSubUser(user_id)
            i = 0
            while i < len(userSub):
                name = types.KeyboardButton("Отписаться от " + ''.join(userSub[i]))
                markup.add(name)
                i = i + 1
            back = types.KeyboardButton('Назад')
            markup.add(back)
            bot.reply_to(message, "Вы успешно отписались", reply_markup=markup)

    elif message.text == 'Новости':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        tg_id = message.from_user.id
        user_id = str(searchUserId(tg_id)[0])
        userSub = searchSubUser(user_id)
        i = 0
        while i < len(userSub):
            name = types.KeyboardButton("Посмотреть новости про " + ''.join(userSub[i]))
            markup.add(name)
            i = i + 1
        back = types.KeyboardButton('Назад')
        markup.add(back)
        bot.reply_to(message, "Новости по вашим подпискам:", reply_markup=markup)

    elif message.text.startswith("Посмотреть"):
        tg_id = message.from_user.id
        user_id = str(searchUserId(tg_id)[0])
        subscribes = searchUserCategory(user_id)
        arr = []
        i = 0
        while i < len(subscribes):
            arr.append(subscribes[i])
            i = i + 1
        i = 0
        count = 0
        text = message.text[23:]
        while i < len(arr):
            if text == arr[i][0]:
                count = count + 1
            i = i + 1
        if count > 0:
            category_id = searchCategory(text)[0]
            category_eng = searchEngCategory(category_id)[0]
            top_headlines = newsapi.get_top_headlines(category=category_eng, language='ru')
            bot.send_message(message.from_user.id, f'{top_headlines["articles"][0]["title"]}\n {top_headlines["articles"][0]["url"]}')

    elif message.text == 'Назад':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Категории")
        btn2 = types.KeyboardButton("Подписки")
        btn3 = types.KeyboardButton("Новости")
        markup.add(btn1, btn2, btn3)
        bot.reply_to(message, "Назад", reply_markup=markup)

bot.polling(none_stop=True, interval=1)
cursor.close()