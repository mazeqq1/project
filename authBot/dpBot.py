import telebot
import sqlite3
from telebot import types
import os
from dotenv import load_dotenv
import requests
import json


load_dotenv()

# Инициализация бота

bot = telebot.TeleBot(os.getenv('TOKEN'))

# Создаем базу данных
conn = sqlite3.connect(r'authBot\users.db', check_same_thread=False)
cursor = conn.cursor()

# Создаем таблицу users, если она не существует
cursor.execute('''CREATE TABLE IF NOT EXISTS users
                  (id INTEGER PRIMARY KEY AUTOINCREMENT, id_user INTEGER, login TEXT, password TEXT)''')
conn.commit()

auth_markup = types.ReplyKeyboardMarkup(True, True)
auth = types.KeyboardButton('Регистрация')
log = types.KeyboardButton('Войти')
auth_markup.add(auth,log)



@bot.message_handler(commands=['start'])
def start(message):
    auth_markup = types.ReplyKeyboardMarkup(True, True)
    auth = types.KeyboardButton('Регистрация')
    log = types.KeyboardButton('Войти')
    auth_markup.add(auth,log)
    bot.send_message(message.chat.id, 'Здравствуйте, что бы продолжить пользоваться ботом пройдите регистрацию или войдите в свою учетную запись', 
                     reply_markup=auth_markup)
    bot.register_next_step_handler(message, authORlogin)

# login or auth 
@bot.message_handler(func=lambda message: True) 
def authORlogin(message):
    if message.text == 'Регистрация':
        back_markup = types.ReplyKeyboardMarkup(True, True)
        back = types.KeyboardButton('Вернуться')
        back_markup.add(back)
        
        bot.send_message(message.chat.id, 'Введите логин:', reply_markup=back_markup)
        bot.register_next_step_handler(message, auth_login)
    elif message.text == 'Войти':
        bot.send_message(message.chat.id, 'Введите логин:',reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message,log_login )
    elif message.text == '/start':
        pass
    



# auth state
@bot.message_handler(func=lambda message: True)
def auth_login(message):
    auth_markup = types.InlineKeyboardMarkup()
    auth = types.InlineKeyboardButton('Регистрация', callback_data='back_auth')
    log = types.InlineKeyboardButton('Войти', callback_data='back_login')
    auth_markup.add(auth,log)
    if message.text == 'Вернуться':
        bot.send_message(message.chat.id, 'Регистация/Вход', reply_markup=auth_markup)
    else:
        auth_login = message.text
        bot.send_message(message.chat.id, 'Введите пароль:')
        bot.register_next_step_handler(message, auth_password, auth_login)

def auth_password(message, auth_login):
    auth_markup = types.InlineKeyboardMarkup()
    auth = types.InlineKeyboardButton('Регистрация', callback_data='back_auth')
    log = types.InlineKeyboardButton('Войти', callback_data='back_login')
    auth_markup.add(auth,log)
    auth_password = message.text
    if auth_password == 'Вернуться':
        bot.send_message(message.chat.id, 'Регистация/Вход', reply_markup=auth_markup)
        
    elif auth_password != 'Вернуться':
        auth_password = message.text
        user_id = message.chat.id
        print(user_id)
        login = check_login(auth_login)
        id_check = check_id(user_id)

#0=not in db 1=in db
    if login == 0 and id_check == 0:
        cursor.execute("INSERT INTO users (id_user, login, password) VALUES (?, ?, ?)",
                       (user_id, auth_login, auth_password))
        conn.commit()
        auth_markup = types.ReplyKeyboardMarkup(True, True)
        log = types.KeyboardButton('Войти')
        auth_markup.add(log)
        bot.send_message(message.chat.id, "Вы успешно зарегистрированы!",reply_markup=auth_markup)
        if message.text == 'Войти':
            bot.send_message(message.chat.id, 'Введите логин:')
            bot.register_next_step_handler(message, auth_login)

    elif login == 1 and id_check == 0:
        auth_markup = types.ReplyKeyboardMarkup(True, True)
        auth = types.KeyboardButton('Регистрация')
        auth_markup.add(auth)
        bot.send_message(message.chat.id, 'Логин уже занят!', reply_markup=auth_markup)

        if message.text == 'Регистрация':
            bot.send_message(message.chat.id, 'Введите логин:')
            bot.register_next_step_handler(message, auth_login)

    elif login == 0 and id_check == 1:
        auth_markup = types.ReplyKeyboardMarkup(True, True)
        auth = types.KeyboardButton('Войти')
        auth_markup.add(auth)
        bot.send_message(message.chat.id, 'Ваш id уже зарегестрирован!', reply_markup=auth_markup)
        if message.text == 'Войти':
            bot.send_message(message.chat.id, 'Введите логин:')
            bot.register_next_step_handler(message, log_login)
            
            

    elif login == 1 and id_check == 1:
        auth_markup = types.ReplyKeyboardMarkup(True, True)
        auth = types.KeyboardButton('Войти')
        auth_markup.add(auth)
        bot.send_message(message.chat.id, 'Логин и id уже заняты!',reply_markup=auth_markup)
        
        if message.text == 'Войти:': 
            bot.send_message(message.chat.id, 'Введите логин:')
            bot.register_next_step_handler(message, log_login)
        
        



def check_id(user_id):
    cursor.execute("SELECT * FROM users WHERE id_user=?", (user_id,))
    if cursor.fetchone():
        return 1
    else:
        return 0

def check_login(auth_login):
    cursor.execute("SELECT * FROM users WHERE login=?", (auth_login,))
    if cursor.fetchone(): 
        return 1
    else:
        return 0  




# login state
@bot.message_handler(func=lambda message: True)
def log_login(message):
    login_user = message.text
    bot.send_message(message.chat.id, 'Введите пароль:')
    bot.register_next_step_handler(message, log_password, login_user)

# log password
def log_password(message, login_user):
    password = message.text
    user_id = message.from_user.id

    cursor.execute("SELECT * FROM users WHERE id_user=? AND login=? AND password=?",
                   (user_id, login_user, password))
    if cursor.fetchone():
        weath_markup = types.ReplyKeyboardMarkup(True, True)
        weat_btn =types.KeyboardButton('Узнать погоду')
        weath_markup.add(weat_btn)
        bot.send_message(message.chat.id, "Вы вошли!", reply_markup=types.ReplyKeyboardRemove())
        photo_file = open('authBot\monkey.jpg', 'rb')
        bot.send_photo(message.chat.id, photo_file)
        bot.register_next_step_handler(message, main)
        bot.send_message(message.chat.id, "Тестовый функционал", reply_markup=weath_markup)
    else:
        auth_markup = types.ReplyKeyboardMarkup(True, True)
        auth = types.KeyboardButton('Войти')
        auth_markup.add(auth)
        bot.send_message(message.chat.id, 'Пароль или логин не верен!',reply_markup=auth_markup)
        if message.text == 'Войти':
            
            bot.send_message(message.chat.id, 'Введите логин:') 
            bot.register_next_step_handler(message, log_login)
    

@bot.message_handler(func=lambda message: True )
def main(message):
    if message.text == 'Узнать погоду':
        bot.send_message(message.chat.id, 'Напишите город', reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, weather)

def weather(message):
    city = message.text.strip().lower()
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={os.getenv('API')}&units=metric')
    if res.status_code == 200:
        data = json.loads(res.text)
        temp = round(data["main"]["temp"])
        feels_like = json.loads(res.text)
        feel = round(data["main"]["feels_like"])
        bot.reply_to(message, f'Погода сейчас: {temp} °C\nОщущается как: {feel} °C')
        image = '☀️' if temp > 15.0 else '❄️'
        bot.send_message(message.chat.id, image)
        ans_mark = types.InlineKeyboardMarkup()
        ans1 = types.InlineKeyboardButton('Да', callback_data='yes')
        ans2 = types.InlineKeyboardButton('Нет', callback_data='no')
        ans_mark.add(ans1, ans2)
        bot.send_message(message.chat.id, 'Повторить?', reply_markup=ans_mark)
    else: 
        bot.reply_to(message, 'Город указан неверный, напишите заново')
        bot.register_next_step_handler(message, weather)
    
    
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data == 'yes':
        bot.send_message(call.message.chat.id, 'Напишите город')
        bot.answer_callback_query(callback_query_id=call.id, text='Да')
        bot.register_next_step_handler(call.message, weather)
    elif call.data == 'no':
        bot.send_message(call.message.chat.id, 'Ну нет так нет')
        bot.answer_callback_query(callback_query_id=call.id, text='Нет')
    elif call.data == 'back_auth':
        bot.send_message(call.message.chat.id, 'Введите логин:')
        bot.answer_callback_query(callback_query_id=call.id, text='Регистрация')
        bot.register_next_step_handler(call.message, auth_login)
    elif call.data == 'back_login':
        bot.send_message(call.message.chat.id, 'Введите логин:')
        bot.answer_callback_query(callback_query_id=call.id, text='Вход')
        bot.register_next_step_handler(call.message, log_login)


    
# Запуск бота
bot.polling(none_stop=True)



