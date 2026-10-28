import telebot
import time
from telebot import types
import sqlite3
from API import TOKEN

db = sqlite3.connect("data (7).db", check_same_thread=False)
cur = db.cursor()

bot = telebot.TeleBot(TOKEN)

year_list = ['99', '00', '01','هیچکدام']
year_markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=2)
btn0 = types.KeyboardButton("هیچکدام")
btn1 = types.KeyboardButton("99")
btn2 = types.KeyboardButton("00")
btn3 = types.KeyboardButton("01")
year_markup.add(btn1,btn2,btn3,btn0)

field_list = ["مهندسی پزشکی", "مهندسی برق", "مهندسی کامپیوتر", "هیچکدام", "حقوق"]
field_markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=2)
btn00 = types.KeyboardButton("هیچکدام")
btn4 = types.KeyboardButton("مهندسی پزشکی")
btn5 = types.KeyboardButton("مهندسی برق")
btn6 = types.KeyboardButton("مهندسی کامپیوتر")
btn01 = types.KeyboardButton("حقوق")
field_markup.add(btn4,btn5,btn6,btn01,btn00)

gender_list = ["خانم", "آقا"]
gender_markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=2)
btn7 = types.KeyboardButton("خانم")
btn8 = types.KeyboardButton("آقا")
gender_markup.add(btn7,btn8)

levels_list = ["هیچی", "خیلی کم", "کم", "متوسط", "زیاد", "خیلی زیاد"]
level_markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=2)
btn9 = types.KeyboardButton("هیچی")
btn10 = types.KeyboardButton("خیلی کم")
btn11 = types.KeyboardButton("کم")
btn12 = types.KeyboardButton("متوسط")
btn13 = types.KeyboardButton("زیاد")
btn14 = types.KeyboardButton("خیلی زیاد")
level_markup.add(btn9,btn10,btn11,btn12,btn13,btn14)

win_markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=2)
btn15 = types.KeyboardButton("برد")
btn16 = types.KeyboardButton("باخت")
win_markup.add(btn15, btn16)

avg_list = ['کمتر از 15', '15 تا 17', '17 تا 20','جامعه مورد برسی نیستم']
avg_markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=2)
btn000 = types.KeyboardButton("جامعه مورد برسی نیستم")
btn17 = types.KeyboardButton("کمتر از 15")
btn18 = types.KeyboardButton("15 تا 17")
btn19 = types.KeyboardButton("17 تا 20")
avg_markup.add(btn17, btn18, btn19,btn000)

yes_markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
btn20 = types.KeyboardButton("بله")
yes_markup.add(btn20)

remove_reply_keyboard = types.ReplyKeyboardRemove()


players = {}

def update_players_dict(id):
    global players

    count = int(cur.execute(f"SELECT count FROM players WHERE id = {id}").fetchall()[0][0])
    wins = int(cur.execute(f"SELECT wins FROM players WHERE id = {id}").fetchall()[0][0])
    
    players[id] = {'win': wins, 
                   'count': count,
                   'link': '',
                   'time': '',
                   'efficiency': ''}    


@bot.message_handler(commands=["start"])
def start_message(msg):
    known = cur.execute(f"SELECT wins FROM players WHERE id = {msg.chat.id}").fetchall()
    if len(known) == 0:
        cur.execute(f'INSERT INTO players(id) VALUES({msg.chat.id})')
        bot.send_message(msg.chat.id, "مرسی تو این بازی شرکت میکنید!")
        ask_year = bot.send_message(msg.chat.id, "ورودی چه سالی هستید؟", reply_markup=year_markup)
        bot.register_next_step_handler(ask_year, year_message)

    elif known[0][0] == 3:
        bot.send_message(msg.chat.id, "مرسی تو این بازی شرکت کردید!", reply_markup=remove_reply_keyboard)

    elif known[0][0] == None:
        bot.send_message(msg.chat.id, "مرسی تو این بازی شرکت میکنید!")
        ask_year = bot.send_message(msg.chat.id, "ورودی چه سالی هستید؟", reply_markup=year_markup)
        bot.register_next_step_handler(ask_year, year_message)

    elif known[0][0] < 3:
        level_message(msg)

    else:
        bot.send_message(msg.chat.id, "مرسی تو این بازی شرکت میکنید!")
        ask_year = bot.send_message(msg.chat.id, "ورودی چه سالی هستید؟", reply_markup=year_markup)
        bot.register_next_step_handler(ask_year, year_message)

def year_message(msg):
    if msg.text in year_list:
        cur.execute(f"UPDATE players SET year = '{msg.text}' WHERE id = {msg.chat.id}")
        ask_field = bot.send_message(msg.chat.id, "چه رشته ای هستی؟", reply_markup=field_markup)
        bot.register_next_step_handler(ask_field, field_message)
    else:
        Keyboard_Error = 'پاسخ ارسال شده در لیست نبود' + '\n' + 'لطفا فقط و فقط از کلید های تعریف شده ما استفاده کنید.'
        bot.send_message(msg.chat.id, Keyboard_Error, reply_markup=remove_reply_keyboard)
        start_message(msg)

def field_message(msg):
    if msg.text in field_list:
        cur.execute(f"UPDATE players SET field = '{msg.text}' WHERE id = {msg.chat.id}")
        ask_gender = bot.send_message(msg.chat.id, "جنسیت؟", reply_markup=gender_markup)
        bot.register_next_step_handler(ask_gender, gender_message)
    else:
        Keyboard_Error = 'پاسخ ارسال شده در لیست نبود' + '\n' + 'لطفا فقط و فقط از کلید های تعریف شده ما استفاده کنید.'
        bot.send_message(msg.chat.id, Keyboard_Error, reply_markup=remove_reply_keyboard)
        start_message(msg)

def gender_message(msg):
    if msg.text in gender_list:
        cur.execute(f"UPDATE players SET gender = '{msg.text}' WHERE id = {msg.chat.id}")
        ask_avg = bot.send_message(msg.chat.id, "حدود معدل؟", reply_markup=avg_markup)
        bot.register_next_step_handler(ask_avg, avg_message)
    else:
        Keyboard_Error = 'پاسخ ارسال شده در لیست نبود' + '\n' + 'لطفا فقط و فقط از کلید های تعریف شده ما استفاده کنید.'
        bot.send_message(msg.chat.id, Keyboard_Error, reply_markup=remove_reply_keyboard)
        start_message(msg)

#  @bot.message_handler(func=lambda msg: msg.text is not None and '/' not in msg.text)
def avg_message(msg):
    if msg.text in avg_list:
        cur.execute(f"UPDATE players SET avg = '{msg.text}' WHERE id = {msg.chat.id}")
        ask_level = bot.send_message(msg.chat.id, "چقدر در این بازی مسلط هستید؟ !", reply_markup=level_markup)
        bot.register_next_step_handler(ask_level, level_message)
    else:
        Keyboard_Error = 'پاسخ ارسال شده در لیست نبود' + '\n' + 'لطفا فقط و فقط از کلید های تعریف شده ما استفاده کنید.'
        bot.send_message(msg.chat.id, Keyboard_Error, reply_markup=remove_reply_keyboard)
        start_message(msg)


def level_message(msg):
    if msg.text in levels_list:
        cur.execute(f"UPDATE players SET level = '{msg.text}' WHERE id = {msg.chat.id}")
        cur.execute(f"UPDATE players SET wins = 0 WHERE id = {msg.chat.id}")
        cur.execute(f"UPDATE players SET count = 0 WHERE id = {msg.chat.id}")
        db.commit()

    if (cur.execute(f"SELECT wins FROM players WHERE id = {msg.chat.id}").fetchall()[0][0] != None):
        bot.send_message(msg.chat.id,"در صورت نیاز از لینک زیر برای مشاهده نحوه بازی استفاده کنید.")
        bot.send_message(msg.chat.id, "https://www.youtube.com/watch?v=7B85WbEiYf4", disable_web_page_preview=True)
        ask_start = bot.send_message(msg.chat.id, "بازی رو شروع کنیم؟", reply_markup=yes_markup)
        bot.register_next_step_handler(ask_start, start_game_message)

    else:
        level_func_Error = 'مشکلی در روند بازی شما پیش آمده' + '\n' + 'لطفا فقط و فقط از کلید های تعریف شده استفاده کنید. دوباره شروع می کنیم.'
        bot.send_message(msg.chat.id, level_func_Error)
        start_message(msg)


# @bot.message_handler(func=lambda msg: msg.text is not None and '/' not in msg.text)
def start_game_message(msg):
    text_start = 'بازی شروع میشود!' + '\n' + 'لینک زیر را کپی کرده و حتما در مرورگر سایت را باز کنید.'
    bot.send_message(msg.chat.id, text_start, reply_markup=remove_reply_keyboard)
    bot.send_message(msg.chat.id,"https://minesweeper.online/start/1")
    time.sleep(1)
    bot.send_message(msg.chat.id, "وقتی بردید،این  اطلاعات را قصد داریم از شما بپرسیم:")
    bot.send_photo(msg.chat.id, photo=open('/root/Maria/help.png', 'rb'))
    time.sleep(1)
    ask_end = bot.send_message(msg.chat.id,"تمام؟", reply_markup=yes_markup)
    bot.register_next_step_handler(ask_end, end_game_message)

def end_game_message(msg):
    ### if msg.text == "بله":
    update_players_dict(msg.chat.id)
    # counter = int(cur.execute(f"SELECT count FROM players WHERE id = {msg.chat.id}").fetchall()[0][0])
    # cur.execute(f"UPDATE players SET count = {counter+1} WHERE id = {msg.chat.id}")
    # db.commit()
    ask_win = bot.send_message(msg.chat.id, "وضعیت بازی؟", reply_markup=win_markup)
    bot.register_next_step_handler(ask_win, win_message)

def win_message(msg):
    if msg.text == "برد":
        ask_link = bot.send_message(msg.chat.id, "لینک بازی که بردید را از مرورگر کپی کرده و وارد کنید", reply_markup=remove_reply_keyboard)
        bot.register_next_step_handler(ask_link, link_message)

    elif msg.text == "باخت":
        # counter = int(cur.execute(f"SELECT count FROM players WHERE id = {msg.chat.id}").fetchall()[0][0])
        cur.execute(f"UPDATE players SET count = {players[msg.chat.id]['count'] + 1} WHERE id = {msg.chat.id}")
        db.commit()
        bot.send_message(msg.chat.id, "لطفا دوباره بازی کنید.", reply_markup=remove_reply_keyboard)
        time.sleep(1)
        start_game_message(msg)

    else:
        Keyboard_Error = 'لطفا فقط و فقط از کلید های تعریف شده ما استفاده کنید.'
        bot.send_message(msg.chat.id, Keyboard_Error)
        end_game_message(msg)

def link_message(msg):
    # win_counter = players[msg.chat.id].get('win') + 1
    # link_var = 'link'+str(win_counter)
    # cur.execute(f"UPDATE players SET {link_var} = '{msg.text}' WHERE id = {msg.chat.id}")
    # db.commit()
    players[msg.chat.id]['link'] = msg.text
    ask_time_result = bot.send_message(msg.chat.id,"عددی که سایت از نتیجه زمان بازی نشان میدهد را وارد کنید.")
    bot.register_next_step_handler(ask_time_result, time_result_message)

def time_result_message(msg):
    # win_counter = int(cur.execute(f"SELECT wins FROM players WHERE id = {msg.chat.id}").fetchall()[0][0]) + 1
    # time_var = 'time'+str(win_counter)
    # cur.execute(f"UPDATE players SET {time_var} = '{msg.text}' WHERE id = {msg.chat.id}")
    # db.commit()
    players[msg.chat.id]['time'] = msg.text
    ask_efficiency_result = bot.send_message(msg.chat.id, "عددی که سایت از نتیجه Efficiency بازی نشان میدهدرا وارد کنید.")
    bot.register_next_step_handler(ask_efficiency_result, efficiency_result_message)

def  efficiency_result_message(msg):
    players[msg.chat.id]['efficiency'] = msg.text
    
    # win_counter = players[msg.chat.id]['win'] + 1
    # link_var = 'link'+str(players[msg.chat.id]['win'] + 1)
    # time_var = 'time'+str(players[msg.chat.id]['win'] + 1)
    # efficiency_var = 'efficiency'+str(players[msg.chat.id]['win'] + 1)

    cur.execute(f"UPDATE players SET {'link'+str(players[msg.chat.id]['win'] + 1)} = '{players[msg.chat.id]['link']}' \
                 WHERE id = {msg.chat.id}")
    
    cur.execute(f"UPDATE players SET {'time'+str(players[msg.chat.id]['win'] + 1)} = '{players[msg.chat.id]['time']}' \
                 WHERE id = {msg.chat.id}")
    
    cur.execute(f"UPDATE players SET {'efficiency'+str(players[msg.chat.id]['win'] + 1)} = '{players[msg.chat.id]['efficiency']}' \
                 WHERE id = {msg.chat.id}")
    
    cur.execute(f"UPDATE players SET wins = {players[msg.chat.id]['win'] + 1} \
                WHERE id = {msg.chat.id}")
    
    cur.execute(f"UPDATE players SET count = {players[msg.chat.id]['count'] + 1} \
                 WHERE id = {msg.chat.id}")

    db.commit()

    if int(players[msg.chat.id]['win'] + 1) < 3:
        bot.send_message(msg.chat.id, "لطفا دوباره بازی کنید.")
        start_game_message(msg)
    elif int(players[msg.chat.id]['win'] + 1) == 3:
        bot.send_message(msg.chat.id, "مرسی تو این بازی شرکت کردید!", reply_markup=remove_reply_keyboard)


bot.polling()

