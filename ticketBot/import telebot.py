import telebot
from telebot import types


#bot = telebot.TeleBot('', skip_pending=True)



#Keyboards
markup = types.InlineKeyboardMarkup()
it_teor = types.InlineKeyboardButton('ИТ теория', callback_data='it_teor')
it_prac = types.InlineKeyboardButton('ИТ практика', callback_data='it_prac')
oa_teor = types.InlineKeyboardButton('ОАИП теория', callback_data='oa_teor')
oa_prac = types.InlineKeyboardButton('ОАИП практика', callback_data='oa_prac')
markup.add(it_teor, it_prac, oa_teor, oa_prac)

menu_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
menu = types.KeyboardButton('Меню📋')
menu_markup.add(menu)

files_oa_teor = {
    '29': 'ticketBot\oa_teor\oa_teor1.txt',
    '30': 'ticketBot\oa_teor\oa_teor2.txt',
    '31': 'ticketBot\oa_teor\oa_teor3.txt',
    '32': 'ticketBot\oa_teor\oa_teor4.txt',
    '33': 'ticketBot\oa_teor\oa_teor5.txt',   
    '34': 'ticketBot\oa_teor\oa_teor6.txt',
    '35': 'ticketBot\oa_teor\oa_teor7.txt',
    '36': 'ticketBot\oa_teor\oa_teor8.txt',
    '37': 'ticketBot\oa_teor\oa_teor9.txt',
    '38': 'ticketBot\oa_teor\oa_teor10.txt',
    '39': 'ticketBot\oa_teor\oa_teor11.txt',
    '40': 'ticketBot\oa_teor\oa_teor12.txt',
    '41': 'ticketBot\oa_teor\oa_teor13.txt',
    '42': 'ticketBot\oa_teor\oa_teor14.txt',
    '43': 'ticketBot\oa_teor\oa_teor15.txt',
    '44': 'ticketBot\oa_teor\oa_teor16.txt',
    '45': 'ticketBot\oa_teor\oa_teor17.txt',
    '46': 'ticketBot\oa_teor\oa_teor18.txt',
    '47': 'ticketBot\oa_teor\oa_teor19.txt',
    '48': 'ticketBot\oa_teor\oa_teor20.txt',
    '49': 'ticketBot\oa_teor\oa_teor21.txt',
    '50': 'ticketBot\oa_teor\oa_teor22.txt',
    '51': 'ticketBot\oa_teor\oa_teor23.txt',
    '52': 'ticketBot\oa_teor\oa_teor24.txt',
    '53': 'ticketBot\oa_teor\oa_teor25.txt',
    '54': 'ticketBot\oa_teor\oa_teor26.txt'
    

}

files_it_teor = {
    '1': 'ticketBot\oa_teor.txt',
    '2': 'ticketBot\it_teor.txt' 
    

}

# files_it_prac = {
#     '1': 'ticketBot\oa_teor.txt',
#     '2': 'ticketBot\it_teor.txt' 
    

# }


# files_it_prac = {
#     '1': 'ticketBot\oa_teor.txt',
#     '2': 'ticketBot\it_teor.txt' 
    
# }

@bot.message_handler(commands=['start'])
def start(message):
    
    bot.send_message(message.chat.id, 'Выберете билеты🎫', reply_markup=markup)
    


    

#Ловля callback

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data == 'it_teor':
        bot.answer_callback_query(callback_query_id=call.id, text='Теория по ИТ')
        bot.register_next_step_handler(call.message, it_teor)
        bot.send_message(call.message.chat.id, 'Введите номер задания (1-28)', reply_markup=menu_markup)
        
    elif call.data == 'it_prac':
        bot.answer_callback_query(callback_query_id=call.id, text='Практика по ИТ')
        bot.register_next_step_handler(call.message, it_prac)
        bot.send_message(call.message.chat.id,'Работаем над этим',reply_markup=menu_markup)

    elif call.data == 'oa_teor':
        bot.answer_callback_query(callback_query_id=call.id, text='Теория по ОАИП')
        bot.register_next_step_handler(call.message, oa_teor)
        bot.send_message(call.message.chat.id, 'Введите номер задания (29-54)', reply_markup=menu_markup)
        
    elif call.data == 'oa_prac':
        bot.answer_callback_query(callback_query_id=call.id, text='Практика по ОАИП')
        bot.register_next_step_handler(call.message, oa_prac)
        bot.send_message(call.message.chat.id,'Работаем над этим',reply_markup=menu_markup)



@bot.message_handler(func=lambda message: True)
def oa_teor(message):
        
    if message.text == 'Меню📋':
        bot.send_message(message.chat.id, "Выберете билеты🎫", reply_markup=markup)
        return
    if message.text in files_oa_teor:
        file = open(files_oa_teor[message.text], 'rb')
        bot.send_message(message.chat.id, file.read())
        bot.send_message(message.chat.id, 'Вы можете ввести номер задания снова или выйти в меню.')

    if message.text not in files_oa_teor:
        bot.reply_to(message, "Такого задания нет, введите другое.")
    

@bot.message_handler(func=lambda message: True)
def it_teor(message):
        
    if message.text == 'Меню📋':
        bot.send_message(message.chat.id, "Выберете билеты🎫", reply_markup=markup)
        return
    if message.text in files_it_teor:
        file_it = open(files_it_teor[message.text], 'rb')
        bot.send_message(message.chat.id, file_it.read())
        bot.send_message(message.chat.id, 'Вы можете ввести номер задания снова или выйти в меню.')

    if message.text not in files_it_teor:
        bot.reply_to(message, "Такого задания нет, введите другое.")

@bot.message_handler(func=lambda message: True)
def it_prac(message):
    if message.text == 'Меню📋':
        bot.send_message(message.chat.id, "Выберете билеты🎫", reply_markup=markup)
        return
    else: bot.send_message(message.chat.id, 'Работаем над этим')
    
    

    
@bot.message_handler(func=lambda message: True)
def oa_prac(message):
    if message.text == 'Меню📋':
        bot.send_message(message.chat.id, "Выберете билеты🎫", reply_markup=markup)
        return
    else: bot.send_message(message.chat.id, 'Работаем над этим')
    
        



bot.polling(non_stop=True)
